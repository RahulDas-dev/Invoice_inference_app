from application import InvoiceInferApp
from library.extensions import configure_uploads, pdf_loader


def register_app(app: InvoiceInferApp) -> None:
    configure_uploads(app, pdf_loader)
