import os
import time
from typing import Optional

from quart import Quart


class TimezoneExtension:
    def __init__(self, app: Optional[Quart] = None, default_timezone: str = "UTC"):
        self._default_timezone = default_timezone
        if app is not None:
            self.init_app(app)

    def get_timezone(self) -> str:
        return os.environ.get("TZ", self._default_timezone)

    def init_app(self, app: Quart) -> None:
        time_zone_ = app.config.get("TIMEZONE", self._default_timezone)
        os.environ["TZ"] = time_zone_
        if hasattr(time, "tzset") and os.name != "nt":
            time.tzset()


timezone_extn = TimezoneExtension()
