from flask_restx import Api

from configs import app_config

from .process import ns as process_ns

api = Api(
    title=app_config.APPLICATION_NAME,
    version=app_config.API_VERSION,
    description="Process Uploaded Document Extracts Invoice Information",
    doc="/docs/",
)

api.add_namespace(process_ns)
