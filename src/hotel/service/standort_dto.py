"""DTO-Klasse für den Standort."""

from dataclasses import dataclass

import strawberry

from hotel.entity import Standort


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class StandortDTO:
    """DTO-Klasse für den Standort, insbesondere ohne Decorators für SQLAlchemy."""

    strasse: str
    hausnummer: str
    plz: str
    ort: str
    land: str

    def __init__(self, standort: Standort) -> None:
        """Initialisierung von StandortDTO durch ein Entity-Objekt von Standort.

        :param standort: Standort-Objekt mit Decorators für SQLAlchemy
        """
        self.strasse = standort.strasse
        self.hausnummer = standort.hausnummer
        self.plz = standort.plz
        self.ort = standort.ort
        self.land = standort.land
