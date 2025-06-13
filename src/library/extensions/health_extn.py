import os
import threading
from typing import Optional

from quart import Quart
from quart_schema import hide


class HealthExtension:
    def __init__(self, app: Optional[Quart] = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Quart) -> None:
        @app.route("/health")
        @hide
        async def get_health_info() -> tuple[dict[str, str], int]:
            resonse_ = {
                "pid": os.getpid(),
                "status": "ok",
                "version": app.config.get("API_VERSION"),
                "app_name": app.config.get("APPLICATION_NAME"),
            }
            return resonse_, 201

        @app.route("/threads")
        @hide
        async def get_threads_info() -> tuple[dict[str, str], int]:
            num_threads = threading.active_count()
            threads = threading.enumerate()

            thread_list = []
            for thread in threads:
                thread_name = thread.name
                thread_id = thread.ident
                is_alive = thread.is_alive()

                thread_list.append(
                    {
                        "name": thread_name,
                        "id": thread_id,
                        "is_alive": is_alive,
                    }
                )

            reponse_ = {"pid": os.getpid(), "thread_num": num_threads, "threads": thread_list}
            return reponse_, 201


health_extn = HealthExtension()
