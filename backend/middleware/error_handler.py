from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from jose.exceptions import JWTError
from typing import Union, Dict, Any
import logging
import traceback

logger = logging.getLogger(__name__)

class ErrorHandler:
    async def __call__(
        self,
        request: Request,
        call_next: callable
    ) -> Union[JSONResponse, Any]:
        try:
            return await call_next(request)
        except Exception as e:
            return self.handle_error(e)

    def handle_error(self, exc: Exception) -> JSONResponse:
        if isinstance(exc, HTTPException):
            return self.handle_http_exception(exc)
        elif isinstance(exc, JWTError):
            return self.handle_jwt_error(exc)
        elif isinstance(exc, SQLAlchemyError):
            return self.handle_database_error(exc)
        else:
            return self.handle_unknown_error(exc)

    def handle_http_exception(self, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "type": "http_error",
                    "code": exc.status_code,
                    "message": exc.detail,
                }
            }
        )

    def handle_jwt_error(self, exc: JWTError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "error": {
                    "type": "auth_error",
                    "code": "invalid_token",
                    "message": "Invalid or expired token",
                }
            },
            headers={"WWW-Authenticate": "Bearer"}
        )

    def handle_database_error(self, exc: SQLAlchemyError) -> JSONResponse:
        logger.error(f"Database error: {str(exc)}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "type": "database_error",
                    "code": "database_error",
                    "message": "Database operation failed",
                }
            }
        )

    def handle_unknown_error(self, exc: Exception) -> JSONResponse:
        logger.error(f"Unexpected error: {str(exc)}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "type": "server_error",
                    "code": "internal_server_error",
                    "message": "An unexpected error occurred",
                }
            }
        ) 