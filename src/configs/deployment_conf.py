from enum import Enum

from pydantic import Field, PositiveInt
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    PRODUCTION = "PRODUCTION"
    STAGING = "STAGING"
    DEVELOPMENT = "DEVELOPMENT"


class DeploymentConfig(BaseSettings):
    APPLICATION_NAME: str = Field(description="Application name", default="invoice-infer")
    DEBUG: bool = Field(description="Debug mode", default=False)
    DEPLOYMENT_ENV: Environment = Field(description="Environment", default=Environment.DEVELOPMENT)
    HOST: str = Field(description="Host", default="127.0.0.0")
    PORT: PositiveInt = Field(description="Port", default=5000)
    API_VERSION: str = Field(description="API version", default="1.0.0")
    TIMEZONE: str = Field(description="Timezone", default="UTC")
    LANGUAGE: str = Field(description="Language", default="en")
