import io
import json
import urllib

import requests
from requests.auth import HTTPBasicAuth

from autumn8.lib.api_creds import retrieve_api_creds
from autumn8.cli.cli_environment import CliEnvironment
from autumn8.common.config.s3 import init_s3


def url_with_params(url, params):
    url_parse = urllib.parse.urlparse(url)
    url_new_query = urllib.parse.urlencode(params)
    url_parse = url_parse._replace(query=url_new_query)

    new_url = urllib.parse.urlunparse(url_parse)
    return new_url


def require_ok_response(response):
    if response.status_code == 403:
        raise Exception(
            f"Received response {response.status_code}:\n{response.text}\n\nUser not authenticated; please run `autumn8-cli login` to authorize your CLI"
        )
    if response.status_code != 200:
        raise Exception(
            f"Received response {response.status_code}:\n{response.text}"
        )


def fetch_user_data(environment: CliEnvironment):
    user_id, api_key = None, None
    autodl_host = environment.value["host"]
    try:
        user_id, api_key = retrieve_api_creds()
    except:
        raise Exception(
            f"API key is missing! To configure API access, please visit {autodl_host}/profile and generate an API key, then run `autumn8-cli login`"
        )

    user_api_route = f"{autodl_host}/api/user"
    response = requests.get(
        user_api_route,
        headers={"Content-Type": "application/json"},
        auth=HTTPBasicAuth(user_id, api_key),
    )

    require_ok_response(response)
    return json.loads(response.text)["user"]


def post_model(environment, organization_id, model_config):
    autodl_host = environment.value["host"]
    api_route = f"{autodl_host}/api/lab/model"
    print("Submitting model to", api_route)
    response = requests.post(
        url_with_params(api_route, {"organization_id": organization_id}),
        headers={"Content-Type": "application/json"},
        data=json.dumps(model_config),
        auth=HTTPBasicAuth(*retrieve_api_creds()),
    )

    require_ok_response(response)
    return response.json()["id"]


def delete_model(environment, organization_id, model_id):
    autodl_host = environment.value["host"]
    new_url = url_with_params(
        f"{autodl_host}/api/lab/model",
        {"model_id": model_id, "organization_id": organization_id},
    )
    response = requests.delete(
        new_url,
        auth=HTTPBasicAuth(*retrieve_api_creds()),
    )
    require_ok_response(response)


def post_model_file(environment, bytes_or_filepath, s3_file_url):
    S3 = init_s3(environment.value["s3_host"])
    s3_bucket_name = environment.value["s3_bucket_name"]
    if isinstance(bytes_or_filepath, io.BytesIO):
        f = bytes_or_filepath
        S3.Bucket(s3_bucket_name).Object(s3_file_url).upload_fileobj(f)
    else:
        with open(bytes_or_filepath, "rb") as f:
            S3.Bucket(s3_bucket_name).Object(s3_file_url).upload_fileobj(f)


def async_prediction(environment, organization_id, model_id):
    autodl_host = environment.value["host"]
    new_url = url_with_params(
        f"{autodl_host}/api/lab/model/async_prediction",
        {
            "model_id": model_id,
            "organization_id": organization_id,
        },
    )
    response = requests.post(
        new_url,
        auth=HTTPBasicAuth(*retrieve_api_creds()),
    )
    require_ok_response(response)
    return response
