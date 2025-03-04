from fastapi import HTTPException, status

class AuthError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class ForbiddenError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class InvalidCredentialsError(AuthError):
    def __init__(self):
        super().__init__(detail="Invalid credentials")

class TokenExpiredError(AuthError):
    def __init__(self):
        super().__init__(detail="Token has expired")

class InsufficientPermissionsError(ForbiddenError):
    def __init__(self, required_role: str):
        super().__init__(
            detail=f"User does not have required role: {required_role}"
        ) 