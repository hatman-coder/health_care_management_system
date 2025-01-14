from core.redis import is_token_blacklisted
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import base64
import jwt
from core.jwt import SECRET_KEY, ALGORITHM


class TokenValidationMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            authorization: str = request.headers.get("Authorization")

            if authorization and authorization.startswith("Bearer "):
                token = authorization.split(" ")[1]

                try:
                    # If the token is base64 encoded, decode it first
                    decoded_token = base64.urlsafe_b64decode(token).decode()

                    # Decode the JWT payload
                    payload = jwt.decode(
                        decoded_token, SECRET_KEY, algorithms=[ALGORITHM]
                    )

                    # Extract the jti (JWT ID) from the decoded payload
                    jti = payload.get("jti")

                    # Check if the token has been blacklisted
                    if jti and is_token_blacklisted(jti):
                        response = JSONResponse(
                            content={"detail": "Token has been revoked"},
                            status_code=401,
                        )
                        await response(scope, receive, send)
                        return

                except jwt.ExpiredSignatureError:
                    response = JSONResponse(
                        content={"detail": "Token has expired"},
                        status_code=401,
                    )
                    await response(scope, receive, send)
                    return
                except jwt.InvalidTokenError:
                    response = JSONResponse(
                        content={"detail": "Invalid token"},
                        status_code=401,
                    )
                    await response(scope, receive, send)
                    return
                except Exception as e:
                    response = JSONResponse(
                        content={"detail": str(e)},
                        status_code=400,
                    )
                    await response(scope, receive, send)
                    return

        # Continue processing the request if no issues
        await self.app(scope, receive, send)
