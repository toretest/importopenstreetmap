# python
from __future__ import annotations

from typing import List, Annotated, Literal
from enum import Enum
from pydantic import BaseModel, Field, RootModel, ConfigDict


# ---------- Dataset type Enum (optional) ----------
class DatasetType(str, Enum):
    ROUTE = "route"
    ZONE = "zone"
    NOT_DEFINED = "not_defined"


# ---------- Common primitives ----------
class Location(BaseModel):
    """A single coordinate pair."""
    model_config = ConfigDict(extra='forbid')
    longitude: float
    latitude: float


class LocationMap(RootModel[dict[str, Location]]):
    """Map from arbitrary location key to Location."""
    # For Pydantic v2, don't set model_config on RootModel subclasses
    pass


# ---------- Dataset variants ----------
class Route(BaseModel):
    model_config = ConfigDict(extra='forbid')
    routeId: int
    name: str
    locations: List[LocationMap]


class RouteDataset(BaseModel):
    model_config = ConfigDict(extra='forbid')
    # Discriminator must be Literal for Pydantic's discriminated unions
    type: Literal["route"] = "route"
    name: str
    data: List[Route]


class ZoneDataset(BaseModel):
    model_config = ConfigDict(extra='forbid')
    type: Literal["zone"] = "zone"
    name: str
    data: List[Location]


class NotDefinedDataset(BaseModel):
    model_config = ConfigDict(extra='forbid')
    type: Literal["not_defined"] = "not_defined"
    name: str
    data: List[dict]  # unknown structure, kept raw


# ---------- Discriminated union ----------
Dataset = Annotated[
    RouteDataset | ZoneDataset | NotDefinedDataset,
    Field(discriminator='type')
]


# ---------- Upper levels ----------
class Project(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str
    description: str
    datasets: List[Dataset]


class Payload(BaseModel):
    model_config = ConfigDict(extra='forbid')
    # customerId moved into payload per new JSON structure
    customerId: int
    organisation_nr: str
    name: str
    projects: List[Project]


class RootModel_(BaseModel):
    """Top-level document."""
    model_config = ConfigDict(extra='forbid')
    SchemaVersion: str
    payload: Payload