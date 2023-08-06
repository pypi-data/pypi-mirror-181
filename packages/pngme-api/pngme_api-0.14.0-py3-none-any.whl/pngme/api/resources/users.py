import asyncio
from abc import ABC
from datetime import datetime
from typing import Any, Dict, List, Optional, TypedDict

from pydantic import validate_arguments

from ..cache import cache
from ..core import BaseClient
from ..encoders import encode_query_params
from ..errors import RequestError, ServerError, UserNotFoundError
from ..retry import retry_policy

PATH = "/users"
USER_PATH = "/users/{user_uuid}"

User = Dict[str, Any]


class UsersResponse(TypedDict):
    page: int
    num_pages: int
    users: List[User]


class BaseUsersResource(ABC):
    def __init__(self, client: BaseClient):
        self._client = client

    @retry_policy(
        max_retry_count=4,
        max_retry_interval_seconds=10,
        retryable_exceptions=[ServerError],
    )
    async def _get_page(
        self,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        search: Optional[str] = None,
        phone_number: Optional[str] = None,
        device_id: Optional[str] = None,
        external_id: Optional[str] = None,
        page: int = 1,
    ) -> UsersResponse:
        async with self._client.session() as session:
            response = await session.get(
                PATH,
                params=encode_query_params(
                    created_after=created_after,
                    created_before=created_before,
                    search=search,
                    phone_number=phone_number,
                    device_id=device_id,
                    external_id=external_id,
                    page=page,
                ),
            )

        if response.status_code // 100 == 5:
            raise ServerError(response.text)

        if response.status_code // 100 == 4:
            raise RequestError(response.text)

        users_response: UsersResponse = response.json()
        return users_response

    @validate_arguments
    @cache
    async def _get(
        self,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        search: Optional[str] = None,
        phone_number: Optional[str] = None,
        device_id: Optional[str] = None,
        external_id: Optional[str] = None,
    ) -> List[User]:
        response = await self._get_page(
            created_after=created_after,
            created_before=created_before,
            search=search,
            device_id=device_id,
            external_id=external_id,
            phone_number=phone_number,
        )
        max_pages = response["num_pages"]
        if max_pages > 1:
            coroutines = [
                self._get_page(
                    created_after=created_after,
                    created_before=created_before,
                    search=search,
                    device_id=device_id,
                    external_id=external_id,
                    page=page + 2,
                )
                for page in range(max_pages - 1)
            ]
            response_pages = await asyncio.gather(*coroutines)
            responses = (response, *response_pages)
        else:
            responses = (response,)

        return [user for response in responses for user in response["users"]]

    @retry_policy(
        max_retry_count=4,
        max_retry_interval_seconds=10,
        retryable_exceptions=[ServerError],
    )
    @validate_arguments
    @cache
    async def _get_user(
        self,
        user_uuid: str,
    ) -> List[User]:
        async with self._client.session() as session:
            response = await session.get(USER_PATH.format(user_uuid=user_uuid))

        if response.status_code // 100 == 5:
            raise ServerError(response.text)

        if response.status_code == 404:
            raise UserNotFoundError(response.text)

        if response.status_code // 100 == 4:
            raise RequestError(response.text)

        user: User = response.json()
        return [user]


class AsyncUsersResource(BaseUsersResource):
    async def get(
        self,
        *,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        search: Optional[str] = None,
        user_uuid: Optional[str] = None,
        phone_number: Optional[str] = None,
        device_id: Optional[str] = None,
        external_id: Optional[str] = None,
    ) -> List[User]:
        if user_uuid:
            return await self._get_user(
                user_uuid=user_uuid,
            )

        return await self._get(
            created_after=created_after,
            created_before=created_before,
            search=search,
            phone_number=phone_number,
            device_id=device_id,
            external_id=external_id,
        )


class SyncUsersResource(BaseUsersResource):
    def get(
        self,
        *,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        search: Optional[str] = None,
        user_uuid: Optional[str] = None,
        phone_number: Optional[str] = None,
        device_id: Optional[str] = None,
        external_id: Optional[str] = None,
    ) -> List[User]:
        if user_uuid:
            return self._client.run(
                self._get_user(
                    user_uuid=user_uuid,
                )
            )

        return self._client.run(
            self._get(
                created_after=created_after,
                created_before=created_before,
                search=search,
                phone_number=phone_number,
                device_id=device_id,
                external_id=external_id,
            )
        )
