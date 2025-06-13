import logging
import sys
import uuid
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

import flask
from flask import Flask


def get_request_id() -> str:
    if getattr(flask.g, "request_id", None):
        return flask.g.request_id

    new_uuid = uuid.uuid4().hex[:10]
    flask.g.request_id = new_uuid

    return new_uuid


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.req_id = get_request_id() if flask.has_request_context() else ""
        return True


class LoggingExtension:
    def __init__(self, app: Optional[Flask] = None):
        self._log_file = None
        self._log_lvl = "INFO"
        self._log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self._maxbytes = 20
        self._backup_count = 5
        self._datafmt = ""
        self._timezone = "UTC"
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        with app.app_context():
            self._log_file = app.config.get("LOG_FILE", self._log_file)
            self._log_lvl = app.config.get("LOG_LEVEL", self._log_lvl)
            self._log_fmt = app.config.get("LOG_FORMAT", self._log_fmt)
            self._maxbytes_ = app.config.get("LOG_FILE_MAX_SIZE", self._maxbytes)
            self._backup_count = app.config.get("LOG_FILE_BACKUP_COUNT", self._backup_count)
            self._datefmt = app.config.get("LOG_DATE_FORMAT", self._datafmt)
            self._timezone = app.config.get("TIMEZONE", self._timezone)

        self._setup_logger()

    def _setup_logger(self) -> None:
        log_handlers: list[logging.Handler] = []
        if self._log_file:
            if not Path(self._log_file).parent.is_dir():
                Path.mkdir(Path(self._log_file).parent, parents=True, exist_ok=True)
            log_handlers.append(
                RotatingFileHandler(
                    filename=self._log_file,
                    maxBytes=self._maxbytes * 1024 * 1024,
                    backupCount=self._backup_count,
                )
            )

        # Always add StreamHandler to log to console
        sh = logging.StreamHandler(sys.stdout)
        sh.addFilter(RequestIdFilter())
        log_handlers.append(sh)

        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.basicConfig(
            level=self._log_lvl,
            format=self._log_fmt,
            datefmt=self._datefmt,
            handlers=log_handlers,
            force=True,
        )
        if self._timezone:
            from datetime import datetime
            from time import struct_time

            import pytz

            timezone = pytz.timezone(self._timezone)

            def time_converter(seconds: Optional[float]) -> struct_time:
                if seconds is None:
                    return datetime.now(tz=timezone).timetuple()
                return datetime.fromtimestamp(seconds, tz=timezone).timetuple()

            for handler in logging.root.handlers:
                if handler.formatter:
                    handler.formatter.converter = time_converter


logging_extn = LoggingExtension()
