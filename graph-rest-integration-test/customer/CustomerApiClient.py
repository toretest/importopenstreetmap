# python
from typing import Dict, Any, Optional
import json
import httpx


class CustomerApiClient:
    """
    Simple HTTP client for customer operations.
    """

    def __init__(
            self,
            base_url: str = "http://localhost:8080/customers/customer",
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

    def create_or_update(self, customer_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/{customer_id}/customerid"
        try:
            resp = self._client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"Request failed with {e.response.status_code}: {e.response.text}") from e
        except httpx.HTTPError as e:
            raise RuntimeError(f"HTTP error: {e}") from e

    def create_or_update_from_file(self, json_path: str) -> Dict[str, Any]:
        """
        Load JSON shaped as:
        {
          "customerId": <id>,
          "payload": {
            "orgnr": "...",
            "name": "..."
            ... other fields ignored ...
          }
        }

        Only "payload.orgnr" and "payload.name" are sent in the request body.
        """
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError as e:
            raise RuntimeError(f"JSON file not found: {json_path}") from e
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON in {json_path}: {e}") from e

        if not isinstance(data, dict):
            raise RuntimeError("Root JSON must be an object")

        if "customerId" not in data:
            raise RuntimeError("Missing 'customerId' in JSON file")

        payload_obj = data.get("payload")
        if not isinstance(payload_obj, dict):
            raise RuntimeError("Missing or invalid 'payload' object in JSON file")

        # Extract only the required fields
        body: Dict[str, Any] = {}
        if "orgnr" in payload_obj:
            body["orgnr"] = payload_obj["orgnr"]
        if "name" in payload_obj:
            body["name"] = payload_obj["name"]

        if not body:
            raise RuntimeError("Neither 'payload.orgnr' nor 'payload.name' found in JSON file")

        customer_id = str(data["customerId"])
        return self.create_or_update(customer_id=customer_id, payload=body)