import json
import os
import threading
from typing import Optional

from flask import Flask, Response


class HealthExtension:
    def __init__(self, app: Optional[Flask] = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        db_type_ = ""
        with app.app_context():
            db_type_ = app.config.get("DB_TYPE", "")

        @app.route("/health")
        def get_health_info() -> Response:
            return Response(
                json.dumps({"pid": os.getpid(), "status": "ok", "version": app.config.get("API_VERSION")}),
                status=200,
                content_type="application/json",
            )

        @app.route("/threads")
        def get_threads_info() -> Response:
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

            return Response(
                json.dumps({"pid": os.getpid(), "thread_num": num_threads, "threads": thread_list}),
                status=200,
                content_type="application/json",
            )

        if db_type_.lower() != "sqlite":

            @app.route("/db-pool-info")
            def get_dbpool_info() -> Response:
                from database import db

                return Response(
                    json.dumps(
                        {
                            "pid": os.getpid(),
                            "pool_size": db.engine.pool.size(),
                            "checked_in_connections": db.engine.pool.checkedin(),
                            "checked_out_connections": db.engine.pool.checkedout(),
                            "overflow_connections": db.engine.pool.overflow(),
                            "connection_timeout": db.engine.pool.timeout(),
                            "recycle_time": db.engine.pool._recycle,  # noqa: SLF001
                        }
                    ),
                    status=200,
                    content_type="application/json",
                )


health_extn = HealthExtension()
