import logging
from pathlib import Path
from typing import Any, List

from blinker import signal

logger = logging.getLogger(__name__)

house_keeping = signal("clenup_temp_files")


def rm_directory(pth: Path) -> None:
    for child in pth.iterdir():
        if child.is_file():
            child.unlink()
        else:
            rm_directory(child)
    pth.rmdir()


def cleanup_temp_files(sender: Any, file_paths: List[Path]) -> None:  # noqa: ARG001
    logger.info("House keeping Going on ...")
    try:
        for f_path in file_paths:
            if f_path.is_file():
                Path(f_path).unlink()
            if f_path.is_dir():
                rm_directory(f_path)
        logger.info("House keeping Complited")
    except Exception as e:
        logger.error(f"Error while removing file {file_paths}: {e}")


house_keeping.connect(cleanup_temp_files)
