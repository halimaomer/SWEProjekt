"""Fixture für pytest: Repository und Hotel(Write)Service."""

from pytest import fixture

from hotel.repository import HotelRepository
from hotel.service import HotelService, HotelWriteService


@fixture()
def hotel_repository() -> HotelRepository:
    """Fixture für HotelRepository."""
    return HotelRepository()


@fixture
def hotel_service(hotel_repository: HotelRepository) -> HotelService:
    """Fixture für HotelService."""
    return HotelService(hotel_repository)


@fixture
def hotel_write_service(
    hotel_repository: HotelRepository,
) -> HotelWriteService:
    """Fixture für HotelWriteService."""
    return HotelWriteService(hotel_repository)
