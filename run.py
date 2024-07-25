import os

from app import create_app


flask_config = os.getenv("FLASK_CONFIG") or "default"
app = create_app(flask_config)


if __name__ == "__main__":
    app.run()
