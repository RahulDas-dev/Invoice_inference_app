import sys

sys.path.append("src")

# if os.environ.get("FLASK_DEBUG", "0") in [0, "0", "False", "flase"]:
#    from gevent import monkey

#    monkey.patch_all()

from src.create_app import create_application

app = create_application()


if __name__ == "__main__":
    from src.create_app import app_config

    if app_config.DEBUG:
        app.run(debug=True, host="127.0.0.1", port=5001)
    else:
        # from gevent.pywsgi import WSGIServer

        # WSGIServer(("127.0.0.1", 5001), app).serve_forever()
        print("waitress-serve --listen=127.0.0.1:5001 app:app")  # noqa: T201
        print("OR")  # noqa: T201
        print("""gunicorn
        --bind "${DIFY_BIND_ADDRESS:-0.0.0.0}:${DIFY_PORT:-5001}"
        --workers ${SERVER_WORKER_AMOUNT:-1}
        --worker-class ${SERVER_WORKER_CLASS:-gevent}
        --worker-connections ${SERVER_WORKER_CONNECTIONS:-10}
        --timeout ${GUNICORN_TIMEOUT:-200}
        app:app""")  # noqa: T201
