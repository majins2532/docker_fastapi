from fastapi import Depends, FastAPI, Request, Header
# from fastapi.exceptions import HTTPException, RequestValidationError
# from fastapi.security import APIKeyHeader
# from fastapi.responses import JSONResponse

from core.settings import TAGS_METADATA, DESCRIPTION, MAIN_API_PREFIX, PROXY_PATH_ROOT, SERVER_URL, VERSION
# from core.dependencies import get_token_header, odoo

# from authorizations.token_jwt import router as router_auth
from routers.api_control import router as router_control
# from core.mdbutils import mdb_connection

# import requests #exceptions | HTTPError,ConnectionError,Timeout
# from handlers.error import http_error_handler,validation_exception_handler,requests_http_error_exceptions_handler, server_exceptions_handler, requests_connection_error_exceptions_handler, requests_timeout_error_exceptions_handler

def get_application():

    ## Start FastApi App 
    application = FastAPI(
        servers = SERVER_URL,
        openapi_url=f"{PROXY_PATH_ROOT}/openapi.json",
        docs_url=f"{PROXY_PATH_ROOT}/docs",
        openapi_tags=TAGS_METADATA,
        redoc_url=None,
        version=VERSION,
        terms_of_service="http://docs.majin.xyz/",
        title="MP API APP",
        #responses=ERROR_RESPONSES,
        description=DESCRIPTION,
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
        #dependencies=[Depends(get_token_header)]
    )

    ## Mapping api Auth
    application.include_router(router_control, prefix=MAIN_API_PREFIX)

    ## Mapping api routes
    # application.include_router(router_auth, prefix=MAIN_API_PREFIX ,dependencies=[Depends(get_token_header)])

    ## Add exception handlers
    # application.add_exception_handler(HTTPException, http_error_handler)
    # application.add_exception_handler(RequestValidationError, validation_exception_handler)
    # application.add_exception_handler(Exception, server_exceptions_handler)
    # application.add_exception_handler(requests.exceptions.HTTPError, requests_http_error_exceptions_handler)
    # application.add_exception_handler(requests.exceptions.ConnectionError, requests_connection_error_exceptions_handler)
    # application.add_exception_handler(requests.exceptions.Timeout, requests_timeout_error_exceptions_handler)
    
    return application

app = get_application()

@app.get(f"{PROXY_PATH_ROOT if PROXY_PATH_ROOT else '/'}")
async def root():
    return {"message": "Hello Bigger Applications!"}