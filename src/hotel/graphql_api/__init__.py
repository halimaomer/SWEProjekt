"""Modul für die GraphQL-Schnittstelle."""

from hotel.graphql_api.graphql_types import (
    CreatePayload,
    HotelInput,
    StandortInput,
    Suchparameter,
    ZimmerInput,
)
from hotel.graphql_api.schema import Query, graphql_router

__all__ = [
    "CreatePayload",
    "HotelInput",
    "Query",
    "StandortInput",
    "Suchparameter",
    "ZimmerInput",
    "graphql_router",
]
