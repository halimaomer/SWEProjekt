"""Geschäftslogik zum Lesen von Hoteldaten."""

from typing import Final

from loguru import logger

from hotel.repository import HotelRepository, Session
from hotel.service.exceptions import NotFoundError
from hotel.service.hotel_dto import HotelDTO

__all__ = ["HotelService"]


class HotelService:
    """Service-Klasse mit Geschäftslogik für Hotels."""

    def __init__(self, repo: HotelRepository) -> None:
        """Konstruktor mit abhängigem HotelRepository."""
        self.repo: HotelRepository = repo

    def find_by_id(self, hotel_id: int) -> HotelDTO:
        """Sucht Hotels anhand der ID.

        :param hotel_id: ID für die Suche
        :return: Das gefundene Hotel
        :rtype: HotelDTO
        :raises NotFoundError: Falls kein Hotel gefunden wurde
        """
        logger.debug("hotel_id={}", hotel_id)

        with Session() as session:
            if (
                hotel := self.repo.find_by_id(hotel_id=hotel_id, session=session)
            ) is None:
                message: Final = f"Kein Hotel mit der ID {hotel_id}"
                logger.debug("NotFoundError: {}", message)
                raise NotFoundError(hotel_id=hotel_id)
            hotel_dto: Final = HotelDTO(hotel)
            session.commit()

        logger.debug("{}", hotel_dto)
        return hotel_dto
