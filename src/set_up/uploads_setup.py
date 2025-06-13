from quart_uploads import configure_uploads

from application import DocumentInferApp
from library.extensions import pdf_loader


def register_app(app: DocumentInferApp) -> None:
    configure_uploads(app, pdf_loader)
