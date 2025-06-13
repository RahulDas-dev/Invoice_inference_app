from werkzeug.middleware.proxy_fix import ProxyFix

from application import InvoiceInferApp


def register_app(app: InvoiceInferApp) -> None:
    app.wsgi_app = ProxyFix(app.wsgi_app)
