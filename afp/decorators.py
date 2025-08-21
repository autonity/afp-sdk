from collections.abc import Callable
from itertools import chain
from typing import Any

import inflection
from decorator import decorator
from eth_typing.abi import ABI
from eth_utils import abi
from hexbytes import HexBytes
from web3.exceptions import (
    ContractLogicError,
    ContractCustomError,
    Web3Exception,
    Web3RPCError,
)

from .api.base import ExchangeAPI
from .exceptions import ClearingSystemError, AuthenticationError


@decorator
def refresh_token_on_expiry(
    f: Callable[..., Any], *args: Any, **kwargs: Any
) -> Callable[..., Any]:
    exchange_api = args[0]
    assert isinstance(exchange_api, ExchangeAPI)
    try:
        return f(*args, **kwargs)
    except AuthenticationError:
        exchange_api._login()  # type: ignore
        return f(*args, **kwargs)


def convert_web3_error(*contract_abis: ABI) -> Callable[..., Any]:
    def caller(f: Callable[..., Any], *args: Any, **kwargs: Any) -> Callable[..., Any]:
        try:
            return f(*args, **kwargs)
        except ContractLogicError as contract_error:
            reason = None
            if contract_error.data:
                reason = str(contract_error.data)
                if isinstance(contract_error, ContractCustomError):
                    reason = _decode_custom_error(
                        str(contract_error.data), *contract_abis
                    )
                if reason == "no data":
                    reason = "Unspecified reason"
            raise ClearingSystemError(
                "Contract call reverted" + f": {reason}" if reason else ""
            ) from contract_error
        except Web3RPCError as rpc_error:
            reason = None
            if rpc_error.rpc_response:
                reason = rpc_error.rpc_response.get("error", {}).get("message")
            raise ClearingSystemError(
                "Blockchain returned error" + f": {reason}" if reason else ""
            ) from rpc_error
        except Web3Exception as web3_exception:
            raise ClearingSystemError(str(web3_exception)) from web3_exception

    return decorator(caller)


def _decode_custom_error(data: str, *contract_abis: ABI) -> str | None:
    selector = HexBytes(data)[:4]
    combined_abi = list(chain(*contract_abis))
    for error_candidate in abi.filter_abi_by_type("error", combined_abi):
        signature = abi.abi_to_signature(error_candidate)
        selector_candidate = abi.function_signature_to_4byte_selector(signature)
        if selector == selector_candidate:
            error = error_candidate["name"]
            # Convert 'ErrorType' to 'Error type'
            return inflection.humanize(inflection.underscore(error))
    return None
