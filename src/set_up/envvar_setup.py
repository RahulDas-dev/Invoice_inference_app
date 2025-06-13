from dotenv import load_dotenv

from application import InvoiceInferApp


def register_app(app: InvoiceInferApp) -> None:  # noqa: ARG001
    load_dotenv()
