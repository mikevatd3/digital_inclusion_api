import requests
import tomli

from pytest import fixture


with open("keys.toml", "rb") as f:
    config = tomli.load(f)


@fixture
def base_url():
    return "http://" + config["app"]["test_url"]


def test_healthcheck_endpoint(base_url):
    request_url = base_url +"/healthcheck"
    response = requests.get(request_url)

    obj = response.json()

    assert obj["message"] == "Looks good so far ..."


def test_geos_within_geo(base_url):
    request_url = base_url + "/zips"
    response = requests.get(request_url)

    obj = response.json()

    assert obj["message"] == "Looks good so far ..."


def test_zip_base(base_url):
    request_url = base_url + "/zips/48202"
    response = requests.get(request_url)

    obj = response.json()

    assert obj["message"] == "Looks good so far ... for 48202"
