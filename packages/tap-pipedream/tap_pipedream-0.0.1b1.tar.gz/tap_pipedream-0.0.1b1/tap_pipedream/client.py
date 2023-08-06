"""REST client handling, including PipedreamStream base class."""

from __future__ import annotations

from typing import Any

from singer_sdk import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator


class PipedreamStream(RESTStream):
    """Pipedream stream class."""

    url_base = "https://api.pipedream.com/v1"
    records_jsonpath = "$.data[*]"
    next_page_token_jsonpath = "$.page_info.end_cursor"

    page_size = 100

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Get an authenticator object.

        Returns:
            The authenticator instance for this REST stream.
        """
        token: str = self.config["token"]
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=token,
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        headers["User-Agent"] = f"{self.tap_name}/{self._tap.plugin_version}"
        return headers

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Next offset.

        Returns:
            Mapping of URL query parameters.
        """
        return {
            "limit": self.page_size,
            "after": next_page_token,
        }
