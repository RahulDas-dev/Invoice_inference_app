from application import DocumentInferApp
from library.extensions import logging_extn


def register_app(app: DocumentInferApp) -> None:
    logging_extn.init_app(app)
