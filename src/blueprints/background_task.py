import asyncio
import logging
from pathlib import Path
from typing import List

from configs import app_config

logger = logging.getLogger(__name__)


async def rm_directory(pth: Path) -> None:
    for child in pth.iterdir():
        if child.is_file():
            await asyncio.to_thread(Path(child).unlink)
        else:
            await rm_directory(child)
    pth.rmdir()


async def cleanup_temp_files(file_paths: List[Path | str]) -> None:
    if app_config.CLEANUP_TEMP_FILES is False:
        logger.info("Cleanup Temp Files is disabled")
        return
    logger.info("House keeping Going on ...")
    try:
        for f_path in file_paths:
            f_path_ = Path(f_path)
            if f_path_.is_file():
                await asyncio.to_thread(f_path_.unlink)
            if f_path_.is_dir():
                await rm_directory(f_path_)
        logger.info("House keeping Complited")
    except Exception as e:
        logger.error(f"Error while removing file {file_paths}: {e}")
