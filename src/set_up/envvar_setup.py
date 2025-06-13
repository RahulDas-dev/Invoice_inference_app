from dotenv import load_dotenv
from quart import Quart


def register_app(app: Quart) -> None:  # noqa: ARG001
    load_dotenv()
