from typing import Optional

from quart import Quart, Response


class LifespanExtension:
    def __init__(self, app: Optional[Quart] = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Quart) -> None:
        @app.after_request
        async def after_request(response: Response) -> Response:
            response.headers.add("X-Version", app.config.get("API_VERSION", "NOT_SET"))
            response.headers.add("X-Env", app.config.get("DEPLOYMENT_ENV", "NOT_SET"))
            response.headers.add("X-Timezn", app.config.get("TIMEZONE", "NOT_SET"))
            response.headers.add("X-Language", app.config.get("LANGUAGE", "NOT_SET"))
            return response


lifespan_extn = LifespanExtension()
