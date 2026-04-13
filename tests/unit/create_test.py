# ruff: noqa: S101, D103, ARG005

"""Unit-Tests für create_test() von HotelService."""

from copy import deepcopy
from datetime import datetime
from typing import TYPE_CHECKING

from pytest import fixture, mark

from hotel.entity import Hotel, Standort

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


@fixture
def session_mock(mocker: MockerFixture):
    session = mocker.Mock()
    mocker.patch(
        "hotel.service.hotel_write_service.Session",
        return_value=mocker.MagicMock(
            __enter__=lambda self: session,
            __exit__=lambda self, exc_type, exc, tb: None,
        ),
    )
    return session


@mark.unit
@mark.unit_create
def test_create(hotel_write_service, session_mock, mocker) -> None:
    standort = Standort(
        id=999,
        strasse="Hauptstrasse",
        hausnummer="1",
        plz="76133",
        ort="Karlsruhe",
        land="Deutschland",
        hotel_id=None,
        hotel=None,
    )
    hotel = Hotel(
        id=None,
        name="Mockhotel",
        standort=standort,
        zimmer=[],
        version=0,
        erzeugt=datetime(2025, 1, 31, 0, 0, 0),
        aktualisiert=datetime(2025, 1, 31, 0, 0, 0),
    )
    standort.hotel = hotel
    hotel_db_mock = deepcopy(hotel)
    generierte_id = 1
    hotel_db_mock.id = generierte_id
    hotel_db_mock.standort.id = generierte_id

    session_mock.scalar.return_value = 0
    session_mock.add.return_value = None

    def flush_side_effect(objects=None):
        for obj in objects or []:
            obj.id = generierte_id

    session_mock.flush.side_effect = flush_side_effect

    mocker.patch("hotel.service.hotel_write_service.send_mail", return_value=None)

    hotel_dto = hotel_write_service.create(hotel=hotel)

    assert hotel_dto.id == generierte_id
