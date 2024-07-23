import logging
from api.app_logger import setup_logging
import tomli

from flask import Flask, jsonify


with open("keys.toml", "rb") as f:
    config = tomli.load(f)

logger = logging.getLogger(config["app"]["name"])


app = Flask(__name__)


logger.info("Logger set up correctly!")


@app.route("/healthcheck")
def healthcheck():
    return jsonify({
        "message": "Looks good so far ..."
    })


if __name__ == "__main__":
    app.run(debug=True)
