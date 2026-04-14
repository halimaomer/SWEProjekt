# ruff: noqa: S101, D103

"""Tests für Queries mit GraphQL."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, graphql_url, login_graphql
from httpx import post
from pytest import mark

GRAPHQL_PATH: Final = "/graphql"


@mark.graphql
@mark.query
def test_query_id() -> None:
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                hotel(hotelId: "20") {
                    id
                    version
                    name
                    standort {
                        strasse
                        hausnummer
                        plz
                        ort
                        land
                    }
                }
            }
        """,
    }

    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    data: Final = response_body["data"]
    assert data is not None
    hotel: Final = data["hotel"]
    assert isinstance(hotel, dict)
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_id_not_found() -> None:
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                hotel(hotelId: "999999") {
                    name
                }
            }
        """,
    }

    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    assert response_body["data"]["hotel"] is None
    assert response_body.get("errors") is None
