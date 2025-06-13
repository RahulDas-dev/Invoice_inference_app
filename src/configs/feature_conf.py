from pathlib import Path

from pydantic import Field, PositiveInt, field_validator
from pydantic_settings import BaseSettings


class FeatureConfig(BaseSettings):
    UPLOADS_DEFAULT_DEST: str = Field(description="Path to the propeller model", default="")
    UPLOADED_FILES_ALLOW: list[str] = Field(
        description="Allowed extensions for the uploaded files", default_factory=lambda: ["pdf", "PDF", "png", "PNG"]
    )
    CLEANUP_TEMP_FILES: bool = Field(description="Cleanup temporary files", default=True)
    MAX_IMG_WIDTH: PositiveInt = Field(description="Maximum image width", default=2500)
    MAX_IMG_HEIGHT: PositiveInt = Field(description="Maximum image height", default=2500)
    IMG_SAVE_FORMAT: str = Field(description="Image save format, default to png", default="png")
    IMAGE_TO_TEXT_MODEL: str = Field(default="us.meta.llama4-maverick-17b-instruct-v1:0")
    PAGE_GROUPPER_MODEL: str = Field(default="o4-mini-2025-04-16")
    OUTPUT_FORMATOR_MODEL: str = Field(default="gpt-4o-mini")
    MERGER_STRATEGY: str = Field(default="classic")
    MAX_CONCURRENT_REQUEST: PositiveInt = Field(description="Maximum number of calls to the Agents", default=10)

    @field_validator("UPLOADS_DEFAULT_DEST", mode="before")
    @classmethod
    def validate_directory1(cls, value: str) -> str:
        if not Path(value).is_dir():
            raise ValueError(f"{value} is not a valid directory")
        return value
