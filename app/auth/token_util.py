import secure

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer

from jwt import PyJWKClient, exceptions as jwt_exceptions, decode as jwt_decode
from typing import Annotated

from config import settings
from exceptions.auth_exceptions import BadCredentialsException, PermissionDeniedException, UnableCredentialsException

csp = secure.ContentSecurityPolicy().default_src("'self'").frame_ancestors("'none'")
hsts = secure.StrictTransportSecurity().max_age(31536000).include_subdomains()
referrer = secure.ReferrerPolicy().no_referrer()
cache_value = secure.CacheControl().no_cache().no_store().max_age(0).must_revalidate()
x_frame_options = secure.XFrameOptions().deny()

secure_headers = secure.Secure(
    # csp=csp,
    hsts=hsts,
    referrer=referrer,
    cache=cache_value,
    xfo=x_frame_options,
)

auth_issuer: str = f"{settings.auth_base_url}/realms/{settings.realm}"
oauth_2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl=f"{auth_issuer}/protocol/openid-connect/token",
    authorizationUrl=f"{auth_issuer}/protocol/openid-connect/auth",
    refreshUrl=f"{auth_issuer}/protocol/openid-connect/token",
)


url = f"{auth_issuer}/protocol/openid-connect/certs"
jwks_client = PyJWKClient(url)


async def valid_access_token(
    access_token: Annotated[str, Depends(oauth_2_scheme)]
):
    try:
        # print(f"url= {url} \n access_token= {access_token}")
        signing_key = jwks_client.get_signing_key_from_jwt(access_token)
        print(f"signing_key = {signing_key}")
        data = jwt_decode(
            access_token,
            signing_key.key,
            algorithms=["RS256"],
            audience="account",
            options={"verify_exp": True},
        )
        print(f"data = {data}")
        return data
    except jwt_exceptions.PyJWKClientError:
        raise UnableCredentialsException
    except jwt_exceptions.InvalidTokenError:
        raise BadCredentialsException


async def get_assigned_roles(token_data: dict):
    roles = token_data["realm_access"]["roles"]
    if settings.client_id in token_data["resource_access"].keys():
        roles.extend(token_data["resource_access"][settings.client_id]["roles"])

    print(f"all roles = {roles}")

    return roles


def has_role(role_name: str):
    async def check_role(
        token_data: Annotated[dict, Depends(valid_access_token)]
    ):
        assigned_roles = await get_assigned_roles(token_data)
        if role_name.casefold() not in (name.casefold() for name in assigned_roles):
            raise PermissionDeniedException

    return check_role


def has_any_role(role_names: list[str]):
    async def check_role(
        token_data: Annotated[dict, Depends(valid_access_token)]
    ):
        assigned_roles = await get_assigned_roles(token_data)
        authorized = False
        for role in role_names:
            print("checking for this role= ", role)
            if role.casefold() in (name.casefold() for name in assigned_roles):
                authorized = True
                break

        if not authorized:
            raise PermissionDeniedException
    return check_role
