from quart import Quart
from quart_schema import Info, QuartSchema


def register_app(app: Quart) -> None:
    title_ = app.config.get("APPLICATION_NAME", "")
    version_ = app.config.get("API_VERSION", "1.0.0")
    api_schema = QuartSchema(
        info=Info(title=title_, version=version_),
        # conversion_preference="pydantic",
    )

    api_schema.init_app(app)
