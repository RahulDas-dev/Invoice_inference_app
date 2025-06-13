import os
import time
from typing import Optional

from flask import Flask


class TimezoneExtension:
    def __init__(self, app: Optional[Flask] = None, default_timezone: str = "UTC"):
        self._default_timezone = default_timezone
        if app is not None:
            self.init_app(app)

    def get_timezone(self) -> str:
        return os.environ.get("TZ", self._default_timezone)

    def init_app(self, app: Flask) -> None:
        with app.app_context():
            time_zone_ = app.config.get("TIMEZONE", self._default_timezone)
        os.environ["TZ"] = time_zone_
        if hasattr(time, "tzset"):
            time.tzset()  # type: ignore


timezone_extn = TimezoneExtension()
