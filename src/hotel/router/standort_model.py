"""Pydantic-Model für den Standort."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from hotel.entity import Standort

__all__: list[str] = ["StandortModel"]


class StandortModel(BaseModel):
    """Pydantic-Model für den Standort."""

    strasse: Annotated[str, StringConstraints(max_length=64)]
    """Straße"""
    hausnummer: Annotated[str, StringConstraints(max_length=10)]
    """Hausnummer"""
    plz: Annotated[str, StringConstraints(pattern=r"^\d{5}$")]
    """Postleitzahl"""
    ort: Annotated[str, StringConstraints(max_length=64)]
    """Ort"""
    land: Annotated[str, StringConstraints(max_length=64)]
    """Land"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "strasse": "Muster Str.",
                "hausnummer": "1a",
                "plz": "12345",
                "ort": "Musterstadt",
                "land": "Deutschland",
            }
        }
    )

    def to_standort(self) -> Standort:
        """Konvertierung in ein Standort-Objekt für SQLAlchemy.

        :return: Standort-Objekt für SQLAlchemy
        :rtype: Standort
        """
        standort_dict = self.model_dump()
        standort_dict["id"] = None
        standort_dict["hotel_id"] = None
        standort_dict["hotel"] = None

        return Standort(**standort_dict)
