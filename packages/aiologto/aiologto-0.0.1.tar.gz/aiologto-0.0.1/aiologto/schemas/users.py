import datetime
from typing import Optional, Type, List, Dict, Any
from aiologto.types.base import BaseRoute, BaseResource, lazyproperty

__all__ = [
    'User',
    'UserResponse',
    'UserRoute',
]

# https://docs.logto.io/api/#tag/Users

class BaseUser(BaseResource):
    primary_email: Optional[str]
    username: Optional[str]
    name: Optional[str]

    def dict(
        self,
        *,
        by_alias: bool = True,
        exclude_none: bool = False,
        **kwargs
    ):
        return super().dict(
            by_alias=by_alias,
            exclude_none=exclude_none,
            **kwargs
        )
    

class User(BaseUser):
    password: Optional[str]

class UserUpdate(BaseUser):
    primary_phone: Optional[str]
    avatar: Optional[str]
    custom_data: Optional[Dict]
    role_names: Optional[List]
    identities: Optional[Dict]
    application_id: Optional[str]

class UserResponse(BaseUser):
    id: Optional[str]
    primary_phone: Optional[str]
    avatar: Optional[str]
    custom_data: Optional[Dict]
    role_names: Optional[List]
    identities: Optional[Dict]
    application_id: Optional[str]
    last_sign_in_at: Optional[datetime.datetime]
    created_at: Optional[datetime.datetime]

UserListResponse = Optional[List[UserResponse]]

class UserRoute(BaseRoute):
    input_model: Optional[Type[BaseResource]] = User
    response_model: Optional[Type[BaseResource]] = UserResponse
    patch_model: Optional[Type[BaseResource]] = UserUpdate

    @lazyproperty
    def api_resource(self):
        return 'api/users'
    
    def get(
        self, 
        user_id: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict] = None,
        **kwargs
    )  -> UserResponse:
        """
        GET a Single User

        :param user_id: The User ID of the Resource to GET
        :param params: Optional Query Parameters
        :param headers: Optional Header Parameters
        :param kwargs: Optional keyword arguments

        :return: UserResponse
        """
        return super().get(
            resource_id=user_id,
            params=params,
            headers=headers,
            **kwargs
        )
    
    async def async_get(
        self, 
        user_id: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict] = None,
        **kwargs
    )  -> UserResponse:
        """
        GET a Single User

        :param user_id: The User ID of the Resource to GET
        :param params: Optional Query Parameters
        :param headers: Optional Header Parameters
        :param kwargs: Optional keyword arguments

        :return: UserResponse
        """
        return await super().async_get(
            resource_id=user_id,
            params=params,
            headers=headers,
            **kwargs
        )
    

    def list(
        self, 
        search: Optional[str] = None,
        hide_admin_user: Optional[bool] = None,
        is_case_sensitive: Optional[bool] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> UserListResponse:
        """
        Retrieve all Users

        :param search: The search query string
        :param hide_admin_user: Whether to hide the Admin User
        :param is_case_sensitive: Whether to search case-sensitive
        :param page: The page number
        :param page_size: The page size

        :param params: Optional Query Parameters
        :param headers: Optional Header Parameters
        :param kwargs: Optional keyword arguments
        
        :return: UserListResponse
        """
        if not params: params = {}
        if search: params['search'] = search
        if hide_admin_user is not None: params['hideAdminUser'] = hide_admin_user
        if is_case_sensitive is not None: params['isCaseSensitive'] = is_case_sensitive
        if page is not None: params['page'] = page
        if page_size is not None: params['pageSize'] = page_size

        return super().list(
            params=params,
            headers=headers,
            **kwargs
        )
    
    async def async_list(
        self,
        search: Optional[str] = None,
        hide_admin_user: Optional[bool] = None,
        is_case_sensitive: Optional[bool] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> UserListResponse:
        """
        Retrieve all Users

        :param search: The search query string
        :param hide_admin_user: Whether to hide the Admin User
        :param is_case_sensitive: Whether to search case-sensitive
        :param page: The page number
        :param page_size: The page size

        :param params: Optional Query Parameters
        :param headers: Optional Header Parameters
        :param kwargs: Optional keyword arguments
        
        :return: UserListResponse
        """
        if not params: params = {}
        if search: params['search'] = search
        if hide_admin_user is not None: params['hideAdminUser'] = hide_admin_user
        if is_case_sensitive is not None: params['isCaseSensitive'] = is_case_sensitive
        if page is not None: params['page'] = page
        if page_size is not None: params['pageSize'] = page_size
        return await super().async_list(
            params=params,
            headers=headers,
            **kwargs
        )

    def get_user_data(
        self, 
        user_id: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict] = None,
        **kwargs
    )  -> UserResponse:
        """
        GET a User's Custom Data

        :param user_id: The User ID of the Resource to GET
        :param params: Optional Query Parameters
        :param headers: Optional Header Parameters
        :param kwargs: Optional keyword arguments

        :return: UserResponse
        """
        headers = self.get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{user_id}/custom-data'
        api_response = self._send(
            method = 'GET',
            url = api_resource, 
            params = params,
            headers = headers,
            **kwargs
        )
        data = self.handle_response(api_response)
        if data: data = data.json()
        return self.prepare_response(data)
    
    async def async_get_user_data(
        self, 
        user_id: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict] = None,
        **kwargs
    )  -> UserResponse:
        """
        GET a User's Custom Data

        :param user_id: The User ID of the Resource to GET
        :param params: Optional Query Parameters
        :param headers: Optional Header Parameters
        :param kwargs: Optional keyword arguments

        :return: UserResponse
        """
        headers = await self.async_get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{user_id}/custom-data'
        api_response = await self._async_send(
            method = 'GET',
            url = api_resource, 
            params = params,
            headers = headers,
            **kwargs
        )
        data = self.handle_response(api_response)
        if data: data = data.json()
        return self.prepare_response(data)

    def update_user_data(
        self, 
        user_id: str,
        user_data: Dict,
        headers: Optional[Dict] = None,
        **kwargs
    ):
        """
        Update a users `customData` dict

        :param user_id: The User ID to Update
        :param user_data: The `customData` dict to update
        """
        
        headers = self.get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{user_id}/custom-data'
        api_response = self._send(
            method = 'PATCH',
            url = api_resource,
            data = user_data,
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        return self.prepare_response(data.json())

    async def async_update_user_data(
        self, 
        user_id: str,
        user_data: Dict,
        headers: Optional[Dict] = None,
        **kwargs
    ):
        """
        Update a users `customData` dict

        :param user_id: The User ID to Update
        :param user_data: The `customData` dict to update
        """
        headers = await self.async_get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{user_id}/custom-data'
        api_response = await self._async_send(
            method = 'PATCH',
            url = api_resource,
            data = user_data,
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        return self.prepare_response(data.json())
    
    def update_user_password(
        self, 
        user_id: str,
        password: str,
        headers: Optional[Dict] = None,
        **kwargs
    ):
        """
        Update a users password

        :param user_id: The User ID to Update
        :param password: The new user password
        """
        headers = self.get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{user_id}/password'
        api_response = self._send(
            method = 'PATCH',
            url = api_resource,
            json = {"password": password},
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        return data is not None
        # return self.prepare_response(data.json())

    async def async_update_user_password(
        self, 
        user_id: str,
        password: str,
        headers: Optional[Dict] = None,
        **kwargs
    ):
        """
        Update a users password

        :param user_id: The User ID to Update
        :param password: The new user password
        """
        headers = await self.async_get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{user_id}/password'
        api_response = await self._async_send(
            method = 'PATCH',
            url = api_resource,
            json = {"password": password},
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        return data is not None
        # return self.prepare_response(data.json())
    
    def update_user_status(
        self, 
        user_id: str,
        suspended: bool,
        headers: Optional[Dict] = None,
        **kwargs
    ):
        """
        Update a users's status, which is either suspended or not

        :param user_id: The User ID to Update
        :param suspended: bool
        """
        headers = self.get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{user_id}/is-suspended'
        api_response = self._send(
            method = 'PATCH',
            url = api_resource,
            json = {"isSuspended": suspended},
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        return self.prepare_response(data.json())

    async def async_update_user_status(
        self, 
        user_id: str,
        suspended: bool,
        headers: Optional[Dict] = None,
        **kwargs
    ):
        """
        Update a users's status, which is either suspended or not

        :param user_id: The User ID to Update
        :param suspended: bool
        """
        headers = await self.async_get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{user_id}/is-suspended'
        api_response = await self._async_send(
            method = 'PATCH',
            url = api_resource,
            json = {"isSuspended": suspended},
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        return self.prepare_response(data.json())