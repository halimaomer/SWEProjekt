"""Schema für GraphQL."""

from decimal import Decimal

import strawberry

__all__ = [
    "CreatePayload",
    "HotelInput",
    "StandortInput",
    "Suchparameter",
    "ZimmerInput",
]


@strawberry.input
class Suchparameter:
    """Suchparameter für die Suche nach Hotels."""

    name: str | None = None
    """Hotelname als Suchkriterium."""


@strawberry.input
class StandortInput:
    """Standort eines neuen Hotels."""

    strasse: str
    hausnummer: str
    plz: str
    ort: str
    land: str


@strawberry.input
class ZimmerInput:
    """Zimmer eines neuen Hotels."""

    preis: Decimal
    zimmernummer: str


@strawberry.input
class HotelInput:
    """Daten für ein neues Hotel."""

    name: str
    standort: StandortInput
    zimmer: list[ZimmerInput]


@strawberry.type
class CreatePayload:
    """Resultat-Typ, wenn ein neues Hotel angelegt wurde."""

    id: int
    """ID des neu angelegten Hotels."""


@strawberry.type
class LoginResult:
    """Resultat-Typ, wenn ein Login erfolgreich war."""

    token: str
    """Token des eingeloggten Users."""
    expiresIn: str  # noqa: N815  # NOSONAR
    """Gültigkeitsdauer des Tokens."""
    roles: list[str]
    """Rollen des eingeloggten Users."""
