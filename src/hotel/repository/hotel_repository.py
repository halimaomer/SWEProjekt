"""Repository fuer persistente Hoteldaten."""

from typing import Final

from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from hotel.entity.hotel import Hotel


class HotelRepository:
    """Repository-Klasse mit CRUD-Methoden für die Entity-Klasse Hotel."""

    def find_by_id(self, hotel_id: int | None, session: Session) -> Hotel | None:
        """Suche mit der Hotel-ID.

        :param hotel_id: ID des gesuchten Hotels
        :param session: Session für SQLAlchemy
        :return: Das gefundene Hotel oder None
        :rtype: Hotel | None
        """
        logger.debug("hotel_id={}", hotel_id)  # NOSONAR

        if hotel_id is None:
            return None

        statement: Final = (
            select(Hotel)
            .options(joinedload(Hotel.standort))
            .where(Hotel.id == hotel_id)
        )
        hotel: Final = session.scalar(statement)

        logger.debug("{}", hotel)
        return hotel

    def create(self, hotel: Hotel, session: Session) -> Hotel:
        """Ein neues Hotel speichern.

        :param hotel: Die Daten des neuen Hotels
        :param session: Session für SQLAlchemy
        :return: Das neu angelegte Hotel mit generierter ID
        :rtype: Hotel
        """
        logger.debug(
            "hotel={}, hotel.standort={}, hotel.zimmer={}",
            hotel,
            hotel.standort,
            hotel.zimmer,
        )

        session.add(instance=hotel)

        session.flush(objects=[hotel])
        logger.debug("hotel_id={}", hotel.id)
        return hotel

    def update(self, hotel: Hotel, session: Session) -> Hotel | None:
        """Ein Hotel aktualisieren.

        :param hotel: Die neuen Hoteldaten
        :param session: Session für SQLAlchemy
        :return: Das aktualisierte Hotel oder None, falls kein Hotel mit der ID
        existiert
        :rtype: Hotel | None
        """
        logger.debug("{}", hotel)

        if (
            hotel_db := self.find_by_id(hotel_id=hotel.id, session=session)
        ) is None:
            return None

        logger.debug("{}", hotel_db)
        return hotel_db

    def delete_by_id(self, hotel_id: int, session: Session) -> None:
        """Die Daten zu einem Hotel löschen.

        :param hotel_id: Die ID des zu löschenden Hotels
        :param session: Session für SQLAlchemy
        """
        logger.debug("hotel_id={}", hotel_id)

        if (hotel := self.find_by_id(hotel_id=hotel_id, session=session)) is None:
            return
        session.delete(hotel)
        logger.debug("ok")
