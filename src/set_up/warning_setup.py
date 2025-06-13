from application import DocumentInferApp


def register_app(app: DocumentInferApp) -> None:
    if app.config.get("DEBUG", False) is False:
        import warnings

        warnings.simplefilter("ignore", ResourceWarning)
