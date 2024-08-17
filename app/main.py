import uvicorn

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from routers import admin, user, general
from config import settings
from auth.token_util import secure_headers

app = FastAPI()
app.include_router(admin.router)
app.include_router(user.router)
app.include_router(general.router)

@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.client_origin_url],
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=86400,
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    message = str(exc.detail)

    return JSONResponse({"message": message}, status_code=exc.status_code)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.reload,
        server_header=False,
    )
