from application import InvoiceInferApp
from library.extensions import health_extn


def register_app(app: InvoiceInferApp) -> None:
    health_extn.init_app(app)
