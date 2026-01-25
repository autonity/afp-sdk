from .dtos import ComponentLink, ExtendedMetadata, ExtendedMetadataDAG


class IPFSClient:
    _api_url: str
    _api_key: str | None

    def __init__(self, api_url: str, api_key: str | None = None):
        self._api_url = api_url
        self._api_key = api_key

    def upload_extended_metadata(self, extended_metadata: ExtendedMetadata) -> str:
        return ""  # TODO

    def download_extended_metadata(self, cid: str) -> ExtendedMetadata:
        return ExtendedMetadata()  # TODO
