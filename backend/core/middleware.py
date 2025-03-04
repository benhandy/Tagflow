from fastapi import Request, status
from fastapi.responses import JSONResponse
from core.logging import logger, APIException
import time
from typing import Callable
import traceback

async def error_handler(request: Request, call_next: Callable) -> JSONResponse:
    try:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log request details
        logger.info(
            f"Path: {request.url.path} | "
            f"Method: {request.method} | "
            f"Status: {response.status_code} | "
            f"Process Time: {process_time:.2f}s"
        )
        
        return response
        
    except APIException as e:
        logger.error(f"API Error: {str(e)}")
        return JSONResponse(
            status_code=e.status_code,
            content={
                "detail": e.detail,
                "internal_code": e.internal_code
            }
        )
        
    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Internal server error",
                "internal_code": "INTERNAL_ERROR"
            }
        )   