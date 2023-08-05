from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.exc import SQLAlchemyError
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class AsyncDBMiddleware(BaseHTTPMiddleware):
    """ Will start a DB Session at every request and commit or rollback in the end """
    def __init__(self, app, engine: AsyncEngine):
        super().__init__(app)
        self.engine = engine

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        async with self.engine.connect() as connection:
            request.state.db = connection

            # Continue with request
            response = await call_next(request)

            try:  # Try to commit
                await connection.commit()
                return response
            except SQLAlchemyError:
                await connection.rollback()
                return JSONResponse({'errors': 'Error while commiting to Database'}, status_code=500)  # Todo: adopt graphql spec


def build_connect_args(args: dict | None) -> dict:
    if args is None:
        args = {}
    if 'connect_timeout' not in args:
        args['connect_timeout'] = 5
    return args


def get_engine(database_uri: str, connect_args: dict | None) -> Engine:
    return create_engine(database_uri, connect_args=build_connect_args(connect_args))


def get_async_engine(database_uri: str, connect_args: dict | None) -> AsyncEngine:
    return create_async_engine(database_uri, connect_args=build_connect_args(connect_args))
