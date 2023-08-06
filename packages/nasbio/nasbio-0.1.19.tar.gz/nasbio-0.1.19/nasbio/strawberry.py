import os
from typing import Generic, Optional, Tuple, TypedDict, TypeVar, Union
from enum import Enum
from datetime import datetime
from dateutil.parser import parse
from base64 import b64encode, b64decode

import json
from fastapi import Depends, HTTPException
import strawberry
from strawberry.extensions import Extension
from strawberry.fastapi.router import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from nasbio import settings
from nasbio.db import get_async_session, get_session

from .sqlalchemy import Pagination

class Group(Enum):
    pass


class Role(Enum):
    user = 'user'
    admin = 'admin'


class Permission(Enum):
    pass


class Authorization(TypedDict):
    groups: list[Group]
    roles: list[Role]
    permissions: list[Permission]


class UserPayloadDict(TypedDict):
    authorization: Authorization
    iss: str
    sub: str
    aud: list[str]
    iat: int
    exp: int


class AuthExtension(Extension):
    def on_request_start(self):
        current_user: UserPayloadDict = self.execution_context.context.get('current_user')
        if (
            # Valid auth credentials.
            (current_user and current_user['sub'])
            or (
            # Development environment.
            (os.environ.get('FASTAPI_ENV') == 'development' or os.environ.get('FASTAPI_ENV') == 'dev_inmemory')
            and (
                # Subgraph introspection by apollo gateway.
                self.execution_context.query == 'query __ApolloGetServiceDefinition__ { _service { sdl } }'
                or
                # Subgraph introspection by rover.
                self.execution_context.query == 'query SubgraphIntrospectQuery {\n    # eslint-disable-next-line'
                                                '\n    _service {\n        sdl\n    }\n}'
                or
                # GraphiQL request.
                self.execution_context.context.get('request').headers.get('referer')
                == f'https://localhost/api/{settings.SERVER_ID}/graphql'
            )
        )
            or
            # Test environment.
            os.environ.get('FASTAPI_ENV') == 'testing'
        ):
            return
        else:
            raise HTTPException(status_code=401, detail='Invalid credentials provided.')


class Context(TypedDict):
    request: Request
    current_user: Optional[UserPayloadDict]
    db: Session
    async_db: AsyncSession


async def get_context(
    request: Request,
    db=Depends(get_session),
    async_db=Depends(get_async_session),
) -> Context:
    current_user_header: str = request.headers.get('current-user')
    user_payload: Optional[UserPayloadDict] = json.loads(current_user_header) \
        if (current_user_header and current_user_header != 'undefined') else None

    return {
        'current_user': user_payload,
        'db': db,
        'async_db': async_db,
    }


# class IsAdmin(BasePermission):
#     message = 'Admin required.'
#
#     def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
#         return info.context['current_user']['admin']


DateTime = strawberry.scalar(
    datetime,
    serialize=lambda value: value.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
    parse_value=lambda value: datetime.fromisoformat(value.rstrip('Z')),
)


@strawberry.interface
class MutationResponse:
    success: bool
    message: str


T = TypeVar('T')


@strawberry.type(description='A list of edges.')
class Edge(Generic[T]):
    node: T
    cursor: str


@strawberry.federation.type(description='Information about pagination in a connection.', shareable=True)
class PageInfo:
    start_cursor: Optional[str] = \
        strawberry.field(description='The cursor to continue from when paginating backward.')
    end_cursor: Optional[str] = strawberry.field(description='The cursor to continue from when paginating forward.')
    has_next_page: bool = strawberry.field(description='Whether there are more items when paginating forward.')
    has_previous_page: bool = strawberry.field(description='Whether there are more items when paginating backward.')


@strawberry.type(description='A list of edges with pagination information.')
class Connection(Generic[T]):
    edges: list[Edge[T]]
    page_info: PageInfo
    total_count: int
    filtered_count: int
    page_count: int
    current_page: int

    @classmethod
    def load(cls, data: Pagination, counts: Tuple[int, int]):
        total_count, filtered_count = counts

        return Connection(
            edges=[Edge(node=item, cursor=to_cursor_hash(item.created_at if hasattr(item, 'created_at') else item.id))
                   for item in data.items],
            page_info=PageInfo(
                start_cursor=to_cursor_hash(
                    data.items[0].created_at if hasattr(data.items[0], 'created_at')
                    else data.items[0].id) if data.items else None,
                end_cursor=to_cursor_hash(
                    data.items[len(data.items) - 1].created_at if hasattr(data.items[len(data.items) - 1], 'created_at')
                    else data.items[len(data.items) - 1].id) if data.items else None,
                has_next_page=data.has_next,
                has_previous_page=data.has_prev,
            ),
            total_count=total_count,  # total_count.
            filtered_count=filtered_count,  # filtered_count.
            page_count=data.pages,  # page_count.
            current_page=data.page,  # current_page.
        )


def to_cursor_hash(datetime_or_id: Union[datetime, strawberry.ID]) -> str:
    return str(b64encode(str(datetime_or_id).encode('utf-8')), 'utf-8')


def from_cursor_hash(cursor: str) -> Union[datetime, strawberry.ID]:
    decoded = str(b64decode(cursor), 'utf-8')
    try:
        parse(decoded)
        return datetime.fromisoformat(decoded)
    except:  # noqa
        return decoded
