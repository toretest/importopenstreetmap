# python
from typing import Dict, Any, Optional
import httpx

# For create_or_update_from_file
from models.ReaderV1 import load_customer_document  # noqa: F401


class CustomerApiClient:
    """
    Simple HTTP client for customer operations.
    """

    def __init__(
            self,
            customer_base_url: str = "http://localhost:8080/customers/customer",
            project_base_url: str = "http://localhost:8080/projects/project",
            dataset_base_url: str = "http://localhost:8080/datasets/dataset",
            timeout: float = 10.0,
            default_headers: Optional[Dict[str, str]] = None,
    ):
        self.customer_base_url = customer_base_url.rstrip("/")
        self.project_base_url = project_base_url.rstrip("/")
        self.dataset_base_url = dataset_base_url.rstrip("/")

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

    # Updated signature: now accepts the validated document instead of id+payload
    def create_or_update(self, doc) -> bool:
        self._post_customer(doc)
        return True

    # Internal: keep the low-level POST logic centralized
    def _post_customer(self, doc) -> Dict[str, Any]:
        base_url = self.customer_base_url
        url = f"{base_url}/{doc.customerId}/customerId"

        body: Dict[str, Any] = {}
        if getattr(doc, "orgnr", None) is not None:
            body["orgnr"] = doc.orgnr

        try:
            resp = self._client.post(url, json=body)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"Request failed with {e.response.status_code}: {e.response.text}") from e
        except httpx.HTTPError as e:
            raise RuntimeError(f"HTTP error: {e}") from e

