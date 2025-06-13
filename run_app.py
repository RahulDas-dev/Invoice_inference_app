import sys

sys.path.append("src")

from src.create_app import create_application

app = create_application()

if __name__ == "__main__":
    # ruff: noqa: T201
    from src.create_app import app_config

    if app_config.DEBUG:
        app.run(debug=True, host="127.0.0.1", port=5001, use_reloader=True)
    else:
        print("+---------------------------------------------------+")
        print(" hypercorn run_app:app --workers 2 --bind 0.0.0.0:5001")
        print("+---------------------------------------------------+")
        app.run(host="0.0.0.0", port=5001)
