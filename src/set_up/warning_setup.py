from application import InvoiceInferApp


def register_app(app: InvoiceInferApp) -> None:
    with app.app_context():
        if app.config.get("DEBUG", False) is False:
            import warnings

            warnings.simplefilter("ignore", ResourceWarning)
