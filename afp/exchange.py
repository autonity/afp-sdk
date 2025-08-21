import json
from typing import Any, Generator

import requests
from requests import Response, Session

from . import config
from .exceptions import (
    AuthenticationError,
    AuthorizationError,
    ExchangeError,
    NotFoundError,
    ValidationError,
)
from .schemas import (
    ExchangeParameters,
    ExchangeProduct,
    ExchangeProductSubmission,
    LoginSubmission,
    MarketDepthData,
    Order,
    OrderFill,
    OrderFillFilter,
    OrderSubmission,
)


class ExchangeClient:
    _session: Session

    def __init__(self):
        self._session = Session()

    # POST /nonce
    def generate_login_nonce(self) -> str:
        response = self._send_request("GET", "/nonce")
        return response.json()["message"]

    # POST /login
    def login(self, login_submission: LoginSubmission) -> ExchangeParameters:
        response = self._send_request(
            "POST", "/login", data=login_submission.model_dump_json()
        )
        return ExchangeParameters(**response.json())

    # GET /products
    def get_approved_products(self) -> list[ExchangeProduct]:
        response = self._send_request("GET", "/products")
        return [ExchangeProduct(**item) for item in response.json()["products"]]

    # GET /products/{product_id}
    def get_product_by_id(self, product_id: str) -> ExchangeProduct:
        response = self._send_request("GET", f"/products/{product_id}")
        return ExchangeProduct(**response.json())

    # POST /products
    def approve_product(self, product_submission: ExchangeProductSubmission) -> None:
        self._send_request(
            "POST", "/products", data=product_submission.model_dump_json()
        )

    # DELETE /products
    def delist_product(self, product_id: str) -> None:
        self._send_request("DELETE", f"/products/{product_id}")

    # POST /orders
    def submit_order(self, order_submission: OrderSubmission) -> Order:
        response = self._send_request(
            "POST", "/orders", data=order_submission.model_dump_json()
        )
        return Order(**response.json())

    # GET /orders
    def get_open_orders(self) -> list[Order]:
        response = self._send_request("GET", "/orders")
        return [Order(**item) for item in response.json()["orders"]]

    # GET /orders/{order_id}
    def get_order_by_id(self, order_id: str) -> Order:
        response = self._send_request("GET", f"/orders/{order_id}")
        return Order(**response.json())

    # GET /order-fills
    def get_order_fills(self, filter: OrderFillFilter) -> list[OrderFill]:
        response = self._send_request(
            "GET", "/order-fills", params=filter.model_dump(exclude_none=True)
        )
        return [OrderFill(**item) for item in response.json()["orderFills"]]

    # GET /stream/order-fills
    def iter_order_fills(
        self, filter: OrderFillFilter
    ) -> Generator[OrderFill, None, None]:
        response = self._send_request(
            "GET",
            "/stream/order-fills",
            params=filter.model_dump(exclude_none=True),
            stream=True,
        )
        for line in response.iter_lines():
            yield OrderFill.model_validate_json(line)

    # GET /market-depth/{product_id}
    def get_market_depth_data(self, product_id: str) -> MarketDepthData:
        response = self._send_request("GET", f"/market-depth/{product_id}")
        return MarketDepthData(**response.json())

    # GET /stream/market-depth/{product_id}
    def iter_market_depth_data(
        self, product_id: str
    ) -> Generator[MarketDepthData, None, None]:
        response = self._send_request(
            "GET", f"/stream/market-depth/{product_id}", stream=True
        )
        for line in response.iter_lines():
            yield MarketDepthData.model_validate_json(line)

    def _send_request(
        self, method: str, endpoint: str, stream: bool = False, **kwargs: Any
    ) -> Response:
        kwargs["headers"] = {
            "Content-Type": "application/json",
            "Accept": "application/x-ndjson" if stream else "application/json",
            "User-Agent": config.USER_AGENT,
        }

        try:
            response = self._session.request(
                method, f"{config.EXCHANGE_URL}{endpoint}", stream=stream, **kwargs
            )
        except requests.exceptions.RequestException as request_exception:
            raise ExchangeError(
                "Failed to send request to the exchange"
            ) from request_exception
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            if http_error.response.status_code == requests.codes.UNAUTHORIZED:
                raise AuthenticationError(http_error) from http_error
            if http_error.response.status_code == requests.codes.FORBIDDEN:
                raise AuthorizationError(http_error) from http_error
            if http_error.response.status_code == requests.codes.NOT_FOUND:
                raise NotFoundError(http_error) from http_error

            try:
                reason = response.json()["detail"]
            except (json.JSONDecodeError, KeyError):
                reason = response.text
            raise ValidationError(reason) from http_error

        return response
