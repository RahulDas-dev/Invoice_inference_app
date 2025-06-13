from application import DocumentInferApp
from library.extensions import lifespan_extn


def register_app(app: DocumentInferApp) -> None:
    lifespan_extn.init_app(app)
