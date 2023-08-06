from typing import List

from terrascope_api import TerrascopeAsyncClient
from terrascope_api.models.permission_pb2 import Permission, PermissionCreateRequest, PermissionCreateResponse
from terrascope_api.models.user_pb2 import User, UserGetRequest


class APIPermission:
    def __init__(self, client: TerrascopeAsyncClient, timeout):
        self.__timeout = timeout
        self.__client = client

    async def create(self, resource_ids: List[str], resource_type: Permission.ResourceType,
                     permission_type: Permission.PermissionType, user_ids: List[str] = [],
                     public: bool = False, public_confirm: bool = False) -> PermissionCreateResponse:
        """
        ...
        :param public:
        :param user_ids: The user IDs (emails) you'd like to share the resources with.
        :param resource_ids: The resource IDs you'd like to share with the users.
        :param resource_type: The type of resource the resource IDs reference.
        :param permission_type: Permission type to grant the users for the resource (read, write, admin).
        :param public: Flag to share publicly (all users). Must have global admin role and use the public_confirm param.
        :param public_confirm: Flag to confirm the sharing of the resource_ids publicly.
        :return: PermissionCreateResponse
        """

        if public:
            if public_confirm:
                uuids = ["1"]
            else:
                print("You must set public_confirm=True to share these resources publicly")
                return
        else:
            # Get UUID of user from emails
            user_get_request = UserGetRequest(users=[User(email=email) for email in user_ids])
            user_get_response = await self.__client.api.user.get(user_get_request)
            uuids = [user.id for user in user_get_response.users]

        request = PermissionCreateRequest(
            permissions=[
                Permission(
                    resource_type=resource_type,
                    resource_ids=resource_ids,
                    subject_ids=uuids,
                    permission_types=[permission_type]
                )
            ]
        )
        response = await self.__client.api.permission.create(request)
        return response

    async def get(self):
        """
        """
        pass
