from application import InvoiceInferApp
from library.extensions import lifespan_extn


def register_app(app: InvoiceInferApp) -> None:
    lifespan_extn.init_app(app)
