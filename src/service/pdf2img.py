import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from flask import Flask, abort
from pdf2image import convert_from_path
from PIL.Image import Image
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Pdf2ImgConfig:
    poppler_path: Path = field(default_factory=Path)
    output_path: Path = field(default_factory=Path)
    max_width: int = field(default=1120)
    max_height: int = field(default=1120)
    thread_count: int = field(default=1)

    @classmethod
    def init_from_app(cls, app: Flask) -> "Pdf2ImgConfig":
        with app.app_context():
            poppler_path_ = app.config.get("POPPLER_PATH", None)
            output_path_ = app.config.get("UPLOADS_DEFAULT_DEST", "")
            output_path_ = Path(output_path_) / Path("pdf2img")
            if not output_path_.exists():
                output_path_.mkdir(parents=True)
            max_width_ = app.config.get("max_width", 1120)
            max_height_ = app.config.get("max_height", 1120)
            return Pdf2ImgConfig(
                poppler_path=poppler_path_, output_path=output_path_, max_width=max_width_, max_height=max_height_
            )


class Pdf2ImgService:
    config: ClassVar[Pdf2ImgConfig]

    @classmethod
    def configure_from_app(cls, app: Flask) -> None:
        config_ = Pdf2ImgConfig.init_from_app(app)
        cls.set_config(config_)

    @classmethod
    def set_config(cls, config: Pdf2ImgConfig) -> None:
        cls.config = config

    @classmethod
    def _convert_to_image(cls, output_folder: Path, pdf_path: str | Path, fmt: str = "png") -> None:
        images = convert_from_path(pdf_path, poppler_path=cls.config.poppler_path, fmt=fmt)
        for index, image in enumerate(images):
            page_no = index + 1
            page_save_path = output_folder / f"Page_{page_no:02}.png"
            cls._resize_and_save(image, page_save_path, fmt)

    @classmethod
    def _resize_and_save(cls, image: Image, save_path: str | Path, fmt: str = "png") -> None:
        width, height = image.size
        if fmt == "png":
            save_format_ = "PNG"
        else:
            abort(403, description=f"File format {fmt} not suported")
        logger.info(f"Processing Images of shape {width}, {height}")
        if width < height and height > cls.config.max_height:
            new_height = cls.config.max_height
            new_width = int(new_height * (width / height))
            new_image = image.resize((new_width, new_height))
            logger.info(f"Resized Images to shape {new_image.size}")
            new_image.save(save_path, save_format_)
        elif width > height and width > cls.config.max_width:
            new_width = cls.config.max_width
            new_height = int(new_width * (height / width))
            new_image = image.resize((new_width, new_height))
            logger.info(f"Resized Images to shape {new_image.size}")
            new_image.save(save_path, save_format_)
        else:
            image.save(save_path, save_format_)

    @classmethod
    def convert(cls, pdf_path: str | Path) -> Path:
        if cls.config is None:
            abort(403, description="The PdfToImageService is not configured")
        filename = secure_filename(Path(pdf_path).stem)
        filename = cls._resolve_conflict(filename)
        output_folder = cls.config.output_path / Path(filename)
        output_folder.mkdir(parents=True)
        try:
            cls._convert_to_image(output_folder, pdf_path)
        except Exception as e:
            logger.error(f"Error While Processing Pdf str{e}")
            abort(403, description=f"PdfToImageService Error While processing {filename}")
        return output_folder

    @classmethod
    def _resolve_conflict(cls, subfolder: str) -> str:
        if not (cls.config.output_path / Path(subfolder)).exists():
            return subfolder
        count = 0
        while True:
            count += 1
            if not (cls.config.output_path / Path(f"{subfolder}_{count}")).exists():
                return f"{subfolder}_{count}"
