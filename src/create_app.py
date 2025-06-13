# ruff: noqa: LOG015
import logging
import time

from application import DocumentInferApp
from configs import app_config


def _register_extensions(app: DocumentInferApp, bebug: bool = False) -> None:
    from set_up import (
        api_schema,
        envvar_setup,
        health_setup,
        lifespan_setup,
        logging_setup,
        timezone_setup,
        uploads_setup,
        warning_setup,
    )

    extensions = [
        timezone_setup,
        logging_setup,
        warning_setup,
        envvar_setup,
        api_schema,
        health_setup,
        lifespan_setup,
        uploads_setup,
    ]
    for extension in extensions:
        logging.info(f"Registering {extension.__name__} ...")
        start_time = time.perf_counter()
        extension.register_app(app)
        if bebug:
            logging.info(
                f"{extension.__name__} registered , latency: {round((time.perf_counter() - start_time) * 1000, 3)}ms"
            )


def _register_services(app: DocumentInferApp) -> None:
    pass


def _register_blueprints(app: DocumentInferApp) -> None:
    from quart import Blueprint

    from blueprints import invoice_bp

    api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

    # Register all document processing blueprints
    api_v1.register_blueprint(invoice_bp)

    # Register the main API blueprint with the app
    app.register_blueprint(api_v1)


def create_application() -> DocumentInferApp:
    start_time = time.perf_counter()
    app = DocumentInferApp(__name__)
    app.config.from_mapping(app_config.model_dump())
    debug_ = app.config.get("DEBUG", False)
    _register_extensions(app, debug_)
    _register_services(app)
    _register_blueprints(app)
    if debug_:
        latency = round((time.perf_counter() - start_time) * 1000, 3)
        logging.info(f"Application created in {latency} seconds")
    return app
