# python
from typing import Dict, Any, Optional
import json
import httpx

class AdminApiClient:
    """
    Simple HTTP client for admin operations.
    """

    def __init__(
            self,
            base_url: str = "http://localhost:8080/admin/graphdb",
            timeout: float = 10.0,
            default_headers: Optional[Dict[str, str]] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers: Dict[str, str] = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        if default_headers:
            self.headers.update(default_headers)

        # Reuse a single client for connection pooling
        self._client = httpx.Client(timeout=self.timeout, headers=self.headers)

    def close(self) -> None:
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def drop_database(self) -> str:
        """
        Calls DELETE {base_url}/dropDatabase.
        Mirrors:
          curl -X DELETE '{base_url}/dropDatabase' -H 'accept: */*'
        Returns response text (may be empty).
        """
        url = f"{self.base_url}/dropDatabase"
        try:
            resp = self._client.delete(url, headers={"accept": "*/*"})
            resp.raise_for_status()
            return resp.text or ""
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"Request failed with {e.response.status_code}: {e.response.text}") from e
        except httpx.HTTPError as e:
            raise RuntimeError(f"HTTP error: {e}") from e