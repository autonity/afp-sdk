from datetime import date, datetime, UTC
from functools import partial
from typing import Annotated, Any, ClassVar, Self

import inflection
import multiformats
import rfc8785
from pydantic import (
    AfterValidator,
    AliasGenerator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    PlainSerializer,
    model_validator,
)

from . import validators

CID_MODEL_MAP: dict[str, type["PinnedModel"]] = {}


# Conversions


def ensure_py_datetime(value: datetime | int | float | str) -> datetime:
    if isinstance(value, datetime):
        return value.astimezone(UTC)
    if isinstance(value, int) or isinstance(value, float):
        return datetime.fromtimestamp(value, UTC)
    return datetime.fromisoformat(value).astimezone(UTC)


def ensure_py_date(value: date | str) -> date:
    if isinstance(value, date):
        return value
    return date.fromisoformat(value)


def ensure_timestamp(value: datetime) -> int:
    return int(value.timestamp())


def ensure_iso_datetime(value: datetime) -> str:
    assert value.tzinfo is UTC, f"{value} should be in UTC timezone"
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_iso_date(value: date) -> str:
    return value.isoformat()


# Custom types


URL = Annotated[
    str,
    Field(min_length=1, max_length=2083),
    BeforeValidator(validators.validate_url),
    AfterValidator(validators.verify_url),
]

CID = Annotated[str, Field(pattern=validators.CID_PATTERN)]

# Convert CIDs into IPLD link objects for dag-cbor/dag-json encoding and back
IPLD_LINK = Annotated[
    CID,
    BeforeValidator(str),
    PlainSerializer(multiformats.CID.decode, return_type=multiformats.CID),
]

# Use datetime internally but UNIX timestamp in serialized format
Timestamp = Annotated[
    datetime,
    BeforeValidator(ensure_py_datetime),
    AfterValidator(validators.validate_non_negative_timestamp),
    PlainSerializer(ensure_timestamp, return_type=int),
]

# Use datetime internally but ISO string in serialized format
ISODateTime = Annotated[
    datetime,
    BeforeValidator(ensure_py_datetime),
    AfterValidator(validators.validate_non_negative_timestamp),
    PlainSerializer(ensure_iso_datetime, return_type=str),
]

# Use date internally but ISO string in serialized format
ISODate = Annotated[
    date,
    BeforeValidator(ensure_py_date),
    PlainSerializer(ensure_iso_date, return_type=str),
]


# Base models


class Model(BaseModel):
    """Base immutable schema."""

    model_config = ConfigDict(frozen=True)

    # Always serialize/deserialize by alias

    def model_dump(self, by_alias: bool = True, **kwargs: Any) -> dict[Any, Any]:
        return super().model_dump(by_alias=by_alias, **kwargs)

    def model_dump_json(self, by_alias: bool = True, **kwargs: Any) -> str:
        return super().model_dump_json(by_alias=by_alias, **kwargs)

    def model_dump_canonical_json(self, **kwargs: Any) -> str:
        obj = self.model_dump(mode="json", **kwargs)
        return rfc8785.dumps(obj).decode("utf-8")

    @classmethod
    def model_validate(cls, *args: Any, by_alias: bool = True, **kwargs: Any) -> Self:
        return super().model_validate(*args, by_alias=by_alias, **kwargs)

    @classmethod
    def model_validate_json(
        cls, *args: Any, by_alias: bool = True, **kwargs: Any
    ) -> Self:
        return super().model_validate_json(*args, by_alias=by_alias, **kwargs)


class AliasedModel(Model):
    """Schema that converts property names from snake case to camel case for
    serialization.
    """

    model_config = Model.model_config | ConfigDict(
        alias_generator=AliasGenerator(
            alias=partial(inflection.camelize, uppercase_first_letter=False),
        ),
        populate_by_name=True,
    )


class PinnedModel(Model):
    """Extended metadata schema that has an IPFS CID."""

    SCHEMA_CID: ClassVar[CID]

    def __init_subclass__(cls, **kwargs: Any):
        super().__init_subclass__(**kwargs)
        if "SCHEMA_CID" in cls.__dict__:
            assert cls.SCHEMA_CID not in CID_MODEL_MAP, (
                f"{cls.__name__} model does not have unique CID"
            )
        CID_MODEL_MAP[cls.SCHEMA_CID] = cls

    @model_validator(mode="after")
    def _ensure_schema_cid(self) -> Self:
        assert "SCHEMA_CID" in self.__class__.__dict__, (
            f"SCHEMA_CID is missing from {self.__class__.__name__} schema"
        )
        return self
