"""Pydantic-Model für das Zimmer."""

from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from hotel.entity import Zimmer

__all__ = ["ZimmerModel"]


class ZimmerModel(BaseModel):
    """Pydantic-Model für das Zimmer."""

    preis: Decimal
    """Der Preis."""
    zimmernummer: Annotated[str, StringConstraints(max_length=10)]
    """Die Zimmernummer."""

    model_config = ConfigDict(
        json_schema_extra={"example": {"preis": "100", "zimmernummer": "1"}}
    )

    def to_zimmer(self) -> Zimmer:
        """Konvertierung in ein Zimmer-Objekt für SQLAlchemy.

        :return: Zimmer-Objekt für SQLAlchemy
        :rtype: Zimmer
        """
        zimmer_dict = self.model_dump()
        zimmer_dict["id"] = None
        zimmer_dict["hotel_id"] = None
        zimmer_dict["hotel"] = None

        return Zimmer(**zimmer_dict)
