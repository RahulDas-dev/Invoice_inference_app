from application import InvoiceInferApp
from database import db


def register_app(app: InvoiceInferApp) -> None:
    db.init_app(app)
    with app.app_context():
        # db.metadata.create_all(db.engine)
        db.create_all()
