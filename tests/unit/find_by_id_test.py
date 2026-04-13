# ruff: noqa: S101, D103, ARG005

"""Unit-Tests für find_by_id() von HotelService."""

from dataclasses import asdict
from datetime import datetime
from typing import TYPE_CHECKING

from pytest import fixture, mark, raises

from hotel.entity import Hotel, Standort
from hotel.service import HotelDTO, NotFoundError

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


@fixture
def session_mock(mocker: MockerFixture):
    session = mocker.Mock()
    mocker.patch(
        "hotel.service.hotel_service.Session",
        return_value=mocker.MagicMock(
            __enter__=lambda self: session,
            __exit__=lambda self, exc_type, exc, tb: None,
        ),
    )
    return session


@mark.unit
@mark.unit_find_by_id
def test_find_by_id(hotel_service, session_mock) -> None:
    hotel_id = 1
    standort_mock = Standort(
        id=11,
        strasse="Hauptstrasse",
        hausnummer="1",
        plz="76133",
        ort="Karlsruhe",
        land="Deutschland",
        hotel_id=hotel_id,
        hotel=None,
    )
    hotel_mock = Hotel(
        id=hotel_id,
        name="Mockhotel",
        standort=standort_mock,
        zimmer=[],
        version=0,
        erzeugt=datetime(2025, 1, 31, 0, 0, 0),
        aktualisiert=datetime(2025, 1, 31, 0, 0, 0),
    )
    standort_mock.hotel = hotel_mock
    hotel_dto_mock = HotelDTO(hotel_mock)
    session_mock.scalar.return_value = hotel_mock

    hotel_dto = hotel_service.find_by_id(hotel_id=hotel_id)

    assert asdict(hotel_dto) == asdict(hotel_dto_mock)


@mark.unit
@mark.unit_find_by_id
def test_find_by_id_not_found(hotel_service, session_mock) -> None:
    hotel_id = 999

    session_mock.scalar.return_value = None

    with raises(NotFoundError) as err:
        hotel_service.find_by_id(hotel_id=hotel_id)

    assert err.type == NotFoundError
    assert str(err.value) == "Not Found"
    assert err.value.patient_id == hotel_id
