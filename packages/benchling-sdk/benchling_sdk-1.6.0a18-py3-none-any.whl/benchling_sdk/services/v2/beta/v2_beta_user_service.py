from typing import Iterable

from benchling_api_client.v2.beta.api.users import (
    bulk_create_users,
    bulk_update_users,
    create_user,
    get_user_activity,
    update_user,
)
from benchling_api_client.v2.beta.models.user import User
from benchling_api_client.v2.beta.models.user_activity import UserActivity
from benchling_api_client.v2.beta.models.user_bulk_create_request import UserBulkCreateRequest
from benchling_api_client.v2.beta.models.user_bulk_update import UserBulkUpdate
from benchling_api_client.v2.beta.models.user_bulk_update_request import UserBulkUpdateRequest
from benchling_api_client.v2.beta.models.user_create import UserCreate
from benchling_api_client.v2.beta.models.user_update import UserUpdate

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.models import AsyncTaskLink
from benchling_sdk.services.v2.base_service import BaseService


class V2BetaUserService(BaseService):
    """
    V2-Beta Users.

    Benchling users.

    See https://benchling.com/api/v2-beta/reference#/Users
    """

    @api_method
    def create(self, user_create: UserCreate) -> User:
        """
        Create a user.

        See https://benchling.com/api/v2-beta/reference#/Users/createUser
        """
        response = create_user.sync_detailed(client=self.client, json_body=user_create)
        return model_from_detailed(response)

    @api_method
    def update(self, user_id: str, user_update: UserUpdate) -> User:
        """
        Update a user.

        See https://benchling.com/api/v2-beta/reference#/Users/updateUser
        """
        response = update_user.sync_detailed(client=self.client, user_id=user_id, json_body=user_update)
        return model_from_detailed(response)

    @api_method
    def bulk_create(self, user_creates: Iterable[UserCreate]) -> AsyncTaskLink:
        """
        Bulk create users.

        See https://benchling.com/api/v2-beta/reference#/Users/bulkCreateUsers
        """
        body = UserBulkCreateRequest(list(user_creates))
        response = bulk_create_users.sync_detailed(client=self.client, json_body=body)
        return model_from_detailed(response)

    @api_method
    def bulk_update(self, user_updates: Iterable[UserBulkUpdate]) -> AsyncTaskLink:
        """
        Bulk update users.

        See https://benchling.com/api/v2-beta/reference#/Users/bulkUpdateUsers
        """
        body = UserBulkUpdateRequest(list(user_updates))
        response = bulk_update_users.sync_detailed(client=self.client, json_body=body)
        return model_from_detailed(response)

    @api_method
    def get_user_activity(self, user_id: str) -> UserActivity:
        """
        Get activity metadata for a specific user.

        See https://benchling.com/api/v2-beta/reference#/Users/getUserActivity
        """
        response = get_user_activity.sync_detailed(client=self.client, user_id=user_id)
        return model_from_detailed(response)
