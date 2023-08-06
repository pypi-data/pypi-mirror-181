from jose import jwt
from typing import Optional, List, Dict, Union
from lazyops.types import BaseModel

__all__ = [
    "TokenResponse",
    "Jwks",
]


class TokenResponse(BaseModel):
    sub: Optional[str]
    iat: Optional[int]
    exp: Optional[int]
    iss: Optional[str]
    aud: Optional[str]
    jti: Optional[str]
    client_id: Optional[str]
    scope: Optional[str]
    role_names: Optional[List]

    @property
    def user_id(self):
        return self.sub

class Jwks(BaseModel):

    key: Optional[Union[Dict, str]]
    algorithms: Optional[str]
    audience: Optional[str]
    issuer: Optional[str]
    options: Optional[Dict]

    def decode_token(
        self,
        token: str,
        key: Optional[Union[Dict, str]] = None,
        algorithms: Optional[str] = None,
        audience: Optional[str] = None,
        issuer: Optional[str] = None,
        options: Optional[Dict] = None,
        **kwargs
    ) -> TokenResponse:

        key = key if key is not None else self.key
        algorithms = algorithms if algorithms is not None else self.algorithms
        audience = audience if audience is not None else self.audience
        issuer = issuer if issuer is not None else self.issuer
        options = options if options is not None else self.options.copy()
        payload = jwt.decode(
            token,
            key = key,
            algorithms = algorithms,
            audience = audience,
            issuer = issuer,
            options = options,
            **kwargs
        )
        return TokenResponse.parse_obj(payload)
