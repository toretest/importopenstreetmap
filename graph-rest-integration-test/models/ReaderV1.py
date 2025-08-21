# python
from __future__ import annotations

from pathlib import Path
from typing import Union, Any, Dict
from pydantic import ValidationError

from .DataEnchangeFormatV1 import RootModel_


def load_customer_document(file_path: Union[str, Path]) -> RootModel_:
    """
    Read a customer JSON file and return a validated RootModel_ instance.

    :param file_path: Path to the JSON file (str or pathlib.Path)
    :return: RootModel_ (Pydantic v2 model) representing the document
    :raises FileNotFoundError: if the file can't be read
    :raises ValueError: if JSON is invalid or fails schema validation
    """
    path = Path(file_path)
    try:
        # Read as text; model_validate_json expects a JSON string
        json_text = path.read_text(encoding="utf-8")
    except Exception as e:
        raise FileNotFoundError(f"Unable to read file: {path}") from e

    try:
        # Let Pydantic parse+validate directly from JSON string
        return RootModel_.model_validate_json(json_text)
    except ValidationError as ve:
        # Surface a concise error with full Pydantic details
        raise ValueError(
            f"Schema validation failed for file: {path}\n{ve}"
        ) from ve
    except Exception as e:
        # Catch non-Validation errors (e.g., malformed JSON)
        raise ValueError(
            f"Failed to parse JSON in file: {path}. {e}"
        ) from e


def parse_customer_document_json(json_text: str) -> RootModel_:
    """
    Parse from a JSON string into RootModel_ with validation.

    :raises ValueError: if JSON is invalid or fails schema validation
    """
    try:
        return RootModel_.model_validate_json(json_text)
    except ValidationError as ve:
        raise ValueError(f"Schema validation failed\n{ve}") from ve
    except Exception as e:
        raise ValueError(f"Failed to parse JSON text. {e}") from e


def parse_customer_document_obj(obj: Dict[str, Any]) -> RootModel_:
    """
    Parse from an already-loaded Python object (dict) into RootModel_ with validation.

    :raises ValueError: if the object fails schema validation
    """
    try:
        return RootModel_.model_validate(obj)
    except ValidationError as ve:
        raise ValueError(f"Schema validation failed\n{ve}") from ve


def generate_customer_json_schema() -> Dict[str, Any]:
    """
    Generate the JSON Schema for the RootModel_.
    """
    return RootModel_.model_json_schema()


def write_customer_json_schema(path: Union[str, Path]) -> Path:
    """
    Write the JSON Schema to a file (pretty-printed).

    :return: The path written
    """
    import json

    schema = generate_customer_json_schema()
    out = Path(path)
    out.write_text(json.dumps(schema, indent=2), encoding="utf-8")
    return out