import logging
import tomli

from flask import Flask, jsonify, request, abort

from digital_inclusion_api.app_logger import setup_logging
from digital_inclusion_api.access import InvalidFieldException, ARPASource, ZipCodes
from digital_inclusion_api.connection import di_engine


with open("keys.toml", "rb") as f:
    config = tomli.load(f)

logger = logging.getLogger(config["app"]["name"])


app = Flask(__name__)


logger.info("Logger set up correctly!")


# Connections section ---- pooling approach tbd

db_source = ARPASource(di_engine)
zip_codes = ZipCodes(db_source)

# ---- end


@app.route("/healthcheck")
def healthcheck():
    logger.info("Healthcheck visited.")
    return jsonify({
        "message": "Looks good so far ..."
    })


@app.route("/api/v1/json/zips")
def zip_list():
    logger.info("Zip code list view visited.")
    fields = request.args.get("fields", "").split(",")
    filters = [] # TODO: What filters are important?
    
    try:
        with di_engine.connect() as db:
            return jsonify({
                "geographies": [
                    geography._asdict()
                    for geography in zip_codes.get_list(filters, db, fields)
                ],
                "metadata": "/api/v1/json/metadata?fields={}"
            })

    except InvalidFieldException:
        abort(
            404, 
            "Invalid fields requested at the zip-code level, "
            f"available fields: {zip_codes.available_fields}"
        )


@app.route("/api/v1/json/zips/<zipcode>")
def zip_detail(zipcode):
    logger.info("Zip code detail view visited.")

    fields = request.args.get("fields", "").split(",")
    filters = [] # TODO: What filters are important?
    
    try:
        with di_engine.connect() as db:
            return jsonify({
                "geography": zip_codes.get_detail(zip, db, fields)._asdict(),
                "metadata": f"/api/v1/json/metadata?fields={request.args.get('fields', '')}"
            })

    except (AttributeError, InvalidFieldException) as e:
        match e:
            case InvalidFieldException():
                abort(
                    404, 
                    f"Invalid fields requested at the zip-code level: {e.bad_fields}, "
                    f"Available fields: {zip_codes.available_fields}"
                )
            case AttributeError():
                abort(
                    404, 
                    f"Invalid zip code requested, {zipcode}."
                )



@app.route("/api/v1/json/metadata")
def metadata():
    logger.info("Metadata view visited.")

    fields = request.args.get("fields", "").split(",")

    return {
        "message": f"Metadata endpoint is to come for fields {fields}."
    }


if __name__ == "__main__":
    setup_logging()

    app.run(debug=True)
