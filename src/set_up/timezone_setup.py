from application import DocumentInferApp
from library.extensions import timezone_extn


def register_app(app: DocumentInferApp) -> None:
    timezone_extn.init_app(app)
