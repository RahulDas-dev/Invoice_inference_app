from typing import Optional

from flask import Flask, Response


class LifespanExtension:
    def __init__(self, app: Optional[Flask] = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        # @app.before_request
        # def before_request() -> None:
        #    UniqueIdGenerator.increment_thread_recycles()

        @app.after_request
        def after_request(response: Response) -> Response:
            response.headers.add("X-Version", app.config.get("API_VERSION"))
            response.headers.add("X-Env", app.config.get("DEPLOYMENT_ENV"))
            response.headers.add("X-Timezn", app.config.get("TIMEZONE"))
            response.headers.add("X-Language", app.config.get("LANGUAGE"))
            return response


lifespan_extn = LifespanExtension()
