from fastapi import APIRouter, Depends
from core.settings import ROUTE_PREFIX_V1
from core.dependencies import get_token_header

from . import get_message_line

router = APIRouter(
        #dependencies=[Depends(get_current_user)]
        #dependencies=[Depends(get_token_header)]
    )

def include_api_routes():
    # router.include_router(account_move.router, prefix=ROUTE_PREFIX_V1, dependencies=[Depends(get_token_header)])
    # router.include_router(fastapi_logs_mongodb.router, prefix=ROUTE_PREFIX_V1)
    # router.include_router(test_url_match.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(get_message_line.router, prefix=ROUTE_PREFIX_V1)

include_api_routes()