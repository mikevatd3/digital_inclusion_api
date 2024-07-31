import logging
from api.app_logger import setup_logging
import tomli

from flask import Flask, jsonify, request


with open("keys.toml", "rb") as f:
    config = tomli.load(f)

logger = logging.getLogger(config["app"]["name"])


app = Flask(__name__)


logger.info("Logger set up correctly!")


@app.route("/api/v1/json/healthcheck")
def healthcheck():
    return jsonify({
        "message": "Looks good so far ..."
    })


@app.route("/api/v1/json/zips")
def zip_list():
    return jsonify({
        "message": "Looks good so far ..."
    })


@app.route("/api/v1/json/zips/<zip_code>")
def zip_detail(zip_code):
    return jsonify({
        "message": f"Looks good so far ... for {zip_code}"
    })


if __name__ == "__main__":
    setup_logging()

    app.run(debug=True)
