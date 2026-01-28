import io
import json
import os
from typing import Any, cast

import dag_cbor
import ipld_car  # type: ignore (untyped library)
import multiformats
import requests
from requests import Response

from . import constants, types
from .dtos import ComponentLink, ExtendedMetadata, ExtendedMetadataDAG
from .exceptions import IPFSError, ValidationError
from .schemas import OracleConfig, OracleFallback, OutcomePoint, OutcomeSpace
from .types import Model, PinnedModel


class IPFSClient:
    _api_url: str
    _api_key: str | None

    def __init__(self, api_url: str, api_key: str | None = None):
        self._api_url = api_url
        self._api_key = api_key

    def upload_extended_metadata(
        self, extended_metadata: ExtendedMetadata
    ) -> types.CID:
        """Uploads extended metadata as a single CAR file."""

        # Use mode="json" to convert Decimal & datetime types to strings
        outcome_space_cid, outcome_space_data = _encode(
            extended_metadata.outcome_space.model_dump(mode="json")
        )
        outcome_point_cid, outcome_point_data = _encode(
            extended_metadata.outcome_point.model_dump(mode="json")
        )
        oracle_config_cid, oracle_config_data = _encode(
            extended_metadata.oracle_config.model_dump(mode="json")
        )
        oracle_fallback_cid, oracle_fallback_data = _encode(
            extended_metadata.oracle_fallback.model_dump(mode="json")
        )
        outcome_space_schema_cid, outcome_space_schema_data = _encode(
            _load_schema_json(extended_metadata.outcome_space.SCHEMA_CID)
        )
        outcome_point_schema_cid, outcome_point_schema_data = _encode(
            _load_schema_json(extended_metadata.outcome_space.SCHEMA_CID)
        )
        oracle_config_schema_cid, oracle_config_schema_data = _encode(
            _load_schema_json(extended_metadata.outcome_space.SCHEMA_CID)
        )
        oracle_fallback_schema_cid, oracle_fallback_schema_data = _encode(
            _load_schema_json(extended_metadata.outcome_space.SCHEMA_CID)
        )

        _ensure_cids_match(
            outcome_space_schema_cid, extended_metadata.outcome_space.SCHEMA_CID
        )
        _ensure_cids_match(
            outcome_point_schema_cid, extended_metadata.outcome_point.SCHEMA_CID
        )
        _ensure_cids_match(
            oracle_config_schema_cid, extended_metadata.oracle_config.SCHEMA_CID
        )
        _ensure_cids_match(
            oracle_fallback_schema_cid, extended_metadata.oracle_fallback.SCHEMA_CID
        )

        extended_metadata_dag = ExtendedMetadataDAG(
            outcome_space=ComponentLink(
                data=str(outcome_space_cid),
                schema_=str(outcome_space_schema_cid),
            ),
            outcome_point=ComponentLink(
                data=str(outcome_point_cid),
                schema_=str(outcome_point_schema_cid),
            ),
            oracle_config=ComponentLink(
                data=str(oracle_config_cid),
                schema_=str(oracle_config_schema_cid),
            ),
            oracle_fallback=ComponentLink(
                data=str(oracle_fallback_cid),
                schema_=str(oracle_fallback_schema_cid),
            ),
        )
        # Use mode="python" to preserve multiformats.CID types so that the DAG-CBOR
        # encoder will convert them into IPLD Link format
        extended_metadata_dag_cid, extended_metadata_dag_data = _encode(
            extended_metadata_dag.model_dump(mode="python")
        )

        blocks: list[ipld_car.Block] = [
            (extended_metadata_dag_cid, extended_metadata_dag_data),
            (outcome_space_cid, outcome_space_data),
            (outcome_point_cid, outcome_point_data),
            (oracle_config_cid, oracle_config_data),
            (oracle_fallback_cid, oracle_fallback_data),
            (outcome_space_schema_cid, outcome_space_schema_data),
            (outcome_point_schema_cid, outcome_point_schema_data),
            (oracle_config_schema_cid, oracle_config_schema_data),
            (oracle_fallback_schema_cid, oracle_fallback_schema_data),
        ]
        car_data = ipld_car.encode([extended_metadata_dag_cid], blocks).tobytes()

        root_cid = self._upload_car(car_data)
        _ensure_cids_match(root_cid, extended_metadata_dag_cid)
        return root_cid

    def download_extended_metadata(self, cid: types.CID) -> ExtendedMetadata:
        """Downloads and assembles extended metadata objects."""

        extended_metadata_dag = self._download_and_validate_block(
            cid, ExtendedMetadataDAG
        )

        outcome_space_model = cast(
            type[OutcomeSpace],
            _find_model_by_schema_cid(extended_metadata_dag.outcome_space.schema_),
        )
        outcome_point_model = cast(
            type[OutcomePoint],
            _find_model_by_schema_cid(extended_metadata_dag.outcome_point.schema_),
        )
        oracle_config_model = cast(
            type[OracleConfig],
            _find_model_by_schema_cid(extended_metadata_dag.oracle_config.schema_),
        )
        oracle_fallback_model = cast(
            type[OracleFallback],
            _find_model_by_schema_cid(extended_metadata_dag.oracle_fallback.schema_),
        )

        return ExtendedMetadata(
            outcome_space=self._download_and_validate_block(
                extended_metadata_dag.outcome_space.data, outcome_space_model
            ),
            outcome_point=self._download_and_validate_block(
                extended_metadata_dag.outcome_point.data, outcome_point_model
            ),
            oracle_config=self._download_and_validate_block(
                extended_metadata_dag.oracle_config.data, oracle_config_model
            ),
            oracle_fallback=self._download_and_validate_block(
                extended_metadata_dag.oracle_fallback.data, oracle_fallback_model
            ),
        )

    def _upload_car(self, data: bytes) -> types.CID:
        response = self._send_client_request(
            "/api/v0/dag/import",
            params={"pin-roots": "true"},
            files={"file": ("data.car", io.BytesIO(data), "application/vnd.ipld.car")},
        )

        try:
            response_data = response.json()
        except json.JSONDecodeError as json_error:
            raise IPFSError(
                f"Error decoding IPFS response: {response.text}"
            ) from json_error

        try:
            return response_data["Root"]["Cid"]["/"]
        except (TypeError, KeyError):
            raise IPFSError(f"Unexpected IPFS response format: {response_data}")

    def _download_and_validate_block[T: Model](
        self, cid: types.CID, model: type[T]
    ) -> T:
        codec_name = multiformats.CID.decode(cid).codec.name
        response = self._send_client_request("/api/v0/block/get", params={"arg": cid})

        if codec_name == "dag-cbor":
            return model.model_validate(dag_cbor.decode(response.content))
        elif codec_name == "dag-json":
            return model.model_validate_json(response.content)
        else:
            raise IPFSError(f"Unsupported codec: {codec_name}")

    def _send_client_request(self, endpoint: str, **kwargs: Any) -> Response:
        headers: dict[str, str] = {}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        url = f"{self._api_url}{endpoint}"
        try:
            response = requests.post(
                url,
                headers=headers,
                timeout=constants.IPFS_REQUEST_TIMEOUT,
                **kwargs,
            )
        except requests.exceptions.Timeout as timeout_error:
            raise IPFSError(
                f"Request to IPFS client timed out after "
                f"{constants.IPFS_REQUEST_TIMEOUT}s: {url}"
            ) from timeout_error
        except requests.exceptions.RequestException as request_exception:
            raise IPFSError(
                f"Failed to send request to IPFS client: {url}"
            ) from request_exception

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            raise IPFSError(
                f"IPFS client returned HTTP {response.status_code}: {url}"
            ) from http_error

        return response


def _find_model_by_schema_cid(cid: types.CID) -> type[PinnedModel]:
    if cid not in types.CID_MODEL_MAP:
        raise ValidationError(f"Unsupported schema CID: {cid}")
    return types.CID_MODEL_MAP[cid]


def _encode(value: Any) -> tuple[multiformats.CID, bytes]:
    cbor_data = dag_cbor.encode(value)
    digest = multiformats.multihash.digest(cbor_data, "sha2-256")
    cid = multiformats.CID("base32", 1, "dag-cbor", digest)
    return (cid, cbor_data)


def _load_schema_json(cid: types.CID) -> dict[Any, Any]:
    with open(os.path.join(constants.SCHEMAS_DIRECTORY, f"{cid}.json")) as f:
        return json.load(f)


def _ensure_cids_match(
    actual_cid: types.CID | multiformats.CID, computed_cid: types.CID | multiformats.CID
) -> None:
    if str(computed_cid) != str(actual_cid):
        raise IPFSError(
            f"Mismatch between computed CID '{computed_cid}' "
            f"and actual CID '{actual_cid}'"
        )
