from application import InvoiceInferApp
from library.extensions import logging_extn


def register_app(app: InvoiceInferApp) -> None:
    logging_extn.init_app(app)
