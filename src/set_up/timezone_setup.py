from application import InvoiceInferApp
from library.extensions import timezone_extn


def register_app(app: InvoiceInferApp) -> None:
    timezone_extn.init_app(app)
