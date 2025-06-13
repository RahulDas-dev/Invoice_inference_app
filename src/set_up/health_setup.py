from application import DocumentInferApp
from library.extensions import health_extn


def register_app(app: DocumentInferApp) -> None:
    health_extn.init_app(app)
