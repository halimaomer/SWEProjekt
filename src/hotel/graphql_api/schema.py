"""Schema für GraphQL durch Strawberry."""

from typing import Final

import strawberry
from fastapi import Request
from loguru import logger
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from hotel.graphql_api.graphql_types import (
    CreatePayload,
    HotelInput,
    LoginResult,
)
from hotel.repository import HotelRepository
from hotel.router.hotel_model import HotelModel
from hotel.security import TokenService, UserService
from hotel.service import (
    HotelDTO,
    HotelService,
    HotelWriteService,
    NotFoundError,
)

__all__ = ["graphql_router"]


_repo: Final = HotelRepository()
_service: HotelService = HotelService(repo=_repo)
_user_service: UserService = UserService()
_write_service: HotelWriteService = HotelWriteService(repo=_repo)
_token_service: Final = TokenService()


@strawberry.type
class Query:
    """Queries, um Hoteldaten zu lesen."""

    @strawberry.field
    def hotel(self, hotel_id: strawberry.ID, info: Info) -> HotelDTO | None:
        """Daten zu einem Hotel lesen.

        :param hotel_id: ID des gesuchten Hotel
        :return: Gesuchter Hotel
        :rtype: Hotel
        :raises NotFoundError: Falls kein Hotel gefunden wurde, wird zu GraphQLError
        """
        logger.debug("hotel_id={}", hotel_id)

        request: Final[Request] = info.context.get("request")
        user: Final = _token_service.get_user_from_request(request=request)
        if user is None:
            return None

        try:
            hotel_dto: Final = _service.find_by_id(hotel_id=int(hotel_id))
        except NotFoundError:
            return None
        logger.debug("{}", hotel_dto)
        return hotel_dto


@strawberry.type
class Mutation:
    """Mutations, um Hoteldaten anzulegen, zu ändern oder zu löschen."""

    @strawberry.mutation
    def create(self, hotel_input: HotelInput) -> CreatePayload:
        """Ein neues Hotel anlegen.

        :param hotel_input: Daten des neuen Hotels
        :return: ID des neuen Hotels
        :rtype: CreatePayload
        """
        logger.debug("hotel_input={}", hotel_input)

        hotel_dict = hotel_input.__dict__
        hotel_dict["standort"] = hotel_input.standort.__dict__
        hotel_dict["zimmer"] = [rechnung.__dict__ for rechnung in hotel_input.zimmer]

        # Dictonary mit Pydantic validieren
        hotel_model: Final = HotelModel.model_validate(hotel_dict)

        hotel_dto: Final = _write_service.create(hotel=hotel_model.to_hotel())
        payload: Final = CreatePayload(id=hotel_dto.id)  # pyright: ignore[reportArgumentType ]

        logger.debug("{}", payload)
        return payload

    @strawberry.mutation
    def login(self, username: str, password: str) -> LoginResult:
        """Einen Token zu Benutzername und Passwort ermitteln.

        :param username: Benutzername
        :param password: Passwort
        :rtype: LoginResult
        """
        logger.debug("username={}, password={}", username, password)
        token_mapping = _token_service.token(username=username, password=password)

        token = token_mapping["access_token"]
        user = _token_service.get_user_from_token(token)
        # List Comprehension ab Python 2.0 (2000) https://peps.python.org/pep-0202
        roles: Final = [role.value for role in user.roles]
        return LoginResult(token=token, expiresIn="1d", roles=roles)


schema = strawberry.Schema(query=Query, mutation=Mutation)


Context = dict[str, Request]


def get_context(request: Request) -> Context:
    return {"request": request}


graphql_router: Final = GraphQLRouter[Context](
    schema,
    context_getter=get_context,
    graphql_ide="graphiql",
)
