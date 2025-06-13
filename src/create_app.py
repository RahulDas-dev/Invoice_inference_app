# ruff: noqa: LOG015
import logging
import time

from application import InvoiceInferApp
from configs import app_config


def _register_extensions(app: InvoiceInferApp, bebug: bool = False) -> None:
    from set_up import (
        envvar_setup,
        health_setup,
        lifespan_setup,
        logging_setup,
        timezone_setup,
        uploads_setup,
        warning_setup,
        werkzeug_setup,
    )

    extensions = [
        timezone_setup,
        warning_setup,
        logging_setup,
        werkzeug_setup,
        health_setup,
        lifespan_setup,
        envvar_setup,
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


def _register_services(app: InvoiceInferApp) -> None:
    from service import InvoiceService, Pdf2ImgService

    Pdf2ImgService.configure_from_app(app)
    InvoiceService.configure_from_app(app)


def _register_blueprints(app: InvoiceInferApp) -> None:
    from blueprints import api

    api.init_app(app)


def create_application() -> InvoiceInferApp:
    start_time = time.perf_counter()
    app = InvoiceInferApp(__name__)
    app.config.from_mapping(app_config.model_dump())
    debug_ = app.config.get("DEBUG", False)
    _register_extensions(app, debug_)
    _register_services(app)
    _register_blueprints(app)
    if debug_:
        latency = round((time.perf_counter() - start_time) * 1000, 3)
        logging.info(f"Application created in {latency} seconds")
    return app
