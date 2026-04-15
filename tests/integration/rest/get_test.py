# ruff: noqa: S101, D103

"""Tests für GET mit Query-Parameter."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_url
from httpx import get
from pytest import mark


@mark.rest
@mark.get_request
@mark.parametrize("name", ["Hotel", "Hilton", "Marriott"])
def test_get_by_name(name: str) -> None:
    # arrange
    params = {"name": name}
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(rest_url, params=params, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)

    content: Final = response_body["content"]
    assert isinstance(content, list)
    assert len(content) > 0

    for hotel in content:
        hotel_name = hotel.get("name")
        assert hotel_name is not None and isinstance(hotel_name, str)
        assert name.lower() in hotel_name.lower()
        assert hotel.get("id") is not None

        standort = hotel.get("standort")
        assert isinstance(standort, dict)
        assert standort.get("plz") is not None
        assert standort.get("ort") is not None


@mark.rest
@mark.get_request
@mark.parametrize("name", ["Nichtvorhanden", "ImmerNochNichtVorhanden"])
def test_get_by_name_not_found(name: str) -> None:
    # arrange
    params = {"name": name}
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(rest_url, params=params, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.get_request
@mark.parametrize("teil", ["h", "ma"])
def test_get_namen(teil: str) -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/name/{teil}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    namen: Final = response.json()
    assert isinstance(namen, list)
    assert len(namen) > 0

    for name in namen:
        assert isinstance(name, str)
        assert teil in name.lower()


@mark.rest
@mark.get_request
@mark.parametrize("teil", ["zzz", "nichtda"])
def test_get_namen_not_found(teil: str) -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/name/{teil}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND
