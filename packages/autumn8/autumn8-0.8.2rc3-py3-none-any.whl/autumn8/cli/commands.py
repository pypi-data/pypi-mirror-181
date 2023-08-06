import enum
import json
import random
import uuid
from configparser import NoOptionError, NoSectionError
import os

import click
import jsonschema
import questionary
from jsonschema import validate

from autumn8.lib import api, api_creds
from autumn8.lib import service as autodl
from autumn8.cli.cli_environment import CliEnvironment
from autumn8.cli.analyze import analyze_model_file
from autumn8.cli.examples import example_model_names
from autumn8.cli.interactive import (
    pick_organization_id,
    verify_organization_id_access,
)
from autumn8.common._version import __version__
from autumn8.common.config.settings import supported_quants

USER_ID_LENGTH = len(str(uuid.uuid4()))
API_KEY_LENGTH = 32

ENABLE_TOGGLEABLE_ENVIRONMENT = False


def use_environment_option(func):
    allowed_environments = (
        [env.name for env in CliEnvironment]
        if ENABLE_TOGGLEABLE_ENVIRONMENT
        else [CliEnvironment.PRODUCTION.name]
    )

    return click.option(
        "-e",
        "--environment",
        "--env",
        type=click.Choice(allowed_environments, case_sensitive=False),
        default=CliEnvironment.PRODUCTION.value,
        callback=lambda c, p, v: getattr(CliEnvironment, v),
        help="Environment to use",
        hidden=True,
    )(func)


@use_environment_option
@click.option(
    "-u",
    "--user_id",
    help="The ID of the user that the CLI will authenticate as in AutoDL.",
)
@click.option(
    "-a",
    "--api_key",
    help="API Key to use when authenticating in AutoDL from now on.",
)
def login(user_id, api_key, environment):
    """Store API credentials for the CLI to use in the future."""

    print(
        f"To setup up CLI access, please visit {environment.value['host']}/profile - once you're signed in, generate a new API Key, then copy and paste the API Key data from the browser here\ngg"
    )
    try:
        old_user_id, _ = api_creds.retrieve_api_creds()
        if old_user_id not in ["", None]:
            print(
                f"Warning: Replacing existing credentials for the user with id={old_user_id}"
            )
    except (NoSectionError, NoOptionError):
        pass

    # using unsafe_ask so that the script is properly aborted on ^C
    # (instead of questionary passing `None` as the user's prompt answer)
    if user_id is None or len(user_id) != USER_ID_LENGTH:
        user_id = questionary.text(
            "User ID",
            validate=lambda user_id: len(user_id) == USER_ID_LENGTH,
        ).unsafe_ask()
    else:
        print(f"User ID: {user_id}")
    if api_key is None or len(api_key) != API_KEY_LENGTH:
        api_key = questionary.text(
            "API Key",
            validate=lambda api_key: len(api_key) == API_KEY_LENGTH,
        ).unsafe_ask()
    else:
        print(f"API Key: {api_key}")

    api_creds.store_api_creds(user_id, api_key)
    user_data = api.fetch_user_data(environment)
    print(f"Credentials set up successfully for {user_data['email']}!")


INPUT_DIMS_JSONSCHEMA = {
    "type": "array",
    "minItems": 1,
    "items": {
        "type": "array",
        "minItems": 1,
        "items": {"type": "number"},
    },
}


def validate_input_dims_json(jsonString):
    if jsonString == "":
        return True

    try:
        jsonData = json.loads(jsonString)
        validate(instance=jsonData, schema=INPUT_DIMS_JSONSCHEMA)
    except (
        jsonschema.exceptions.ValidationError,
        json.decoder.JSONDecodeError,
    ):
        return False
    return True


INPUT_FILE_JSONSCHEMA = {
    "type": "array",
    "minItems": 1,
}


def validate_input_file(path):
    if not os.path.exists(path):
        return False

    try:
        with open(path, "r") as f:
            jsonData = json.load(f)

        validate(instance=jsonData, schema=INPUT_FILE_JSONSCHEMA)
    except (
        jsonschema.exceptions.ValidationError,
        json.decoder.JSONDecodeError,
    ):
        return False
    return True


def normalize_input_dims_for_api(input_dims):
    if not input_dims:
        return None

    inputs = json.loads(input_dims)
    inputs = [[str(dim) for dim in input] for input in inputs]
    return json.dumps(inputs, separators=(",", ":"))


# cannot use click prompt kwargs feature for the command options, because we
# want to infer input dimensions and the model name
def prompt_for_missing_model_info(
    model_name,
    quantization,
    input_dims,
    input_file,
    inferred_model_name,
    inferred_quantization,
    inferred_input_dims,
):
    # TODO - attempt reading model details from some configCache files
    if model_name is None:
        model_name = questionary.text(
            f"Please give a name to your model to be used in AutoDL (for example: '{random.choice(example_model_names)}')\n  Model name:",
            validate=lambda name: len(name) > 0,
            default=inferred_model_name,
        ).unsafe_ask()
    if quantization is None:
        quantization = questionary.select(
            "Choose quantization for the model",
            choices=supported_quants,
            use_shortcuts=True,
            default=inferred_quantization,
        ).unsafe_ask()

    class INPUT_METHODS(enum.Enum):
        FILE = "Upload input file"
        SHAPE = "Specify input shape"
        INFER = "Let us try to infer input shape"

    input_method = INPUT_METHODS.INFER.value

    if input_file is not None and input_dims is not None:
        print("Cannot specify both input file and input dimensions")
        input_file = None
        input_dims = None

    if input_dims is None and input_file is None:
        input_method = questionary.select(
            "Specify input method",
            choices=[method.value for method in INPUT_METHODS],
            use_shortcuts=True,
            default=INPUT_METHODS.INFER.value,
        ).unsafe_ask()

    if input_method == INPUT_METHODS.SHAPE.value and input_dims is None:
        input_dims = questionary.text(
            "Specify input dimensions for every model input as an array of JSON arrays "
            + '(ie. "[[3, 224, 224]]"), or leave blank to let us try to infer the input sizes")',
            validate=validate_input_dims_json,
            default=str(inferred_input_dims) if inferred_input_dims else "",
        ).unsafe_ask()

    if input_method == INPUT_METHODS.FILE.value and input_dims is None:
        input_file = questionary.text(
            "Provide an input file path (supported formats: .json)",
            validate=validate_input_file,
            default="",
        ).unsafe_ask()

    input_dims = normalize_input_dims_for_api(input_dims)

    return (model_name, quantization, input_dims, input_file)


@use_environment_option
@click.argument("model_file_path")
@click.argument("model_script_args", nargs=-1)
@click.option(
    "-n",
    "--name",
    "model_name",
    help="Name of the model to be used in AutoDL.",
)
@click.option(
    "-q",
    "--quantization",
    "--quants",
    type=click.Choice(supported_quants, case_sensitive=False),
    help="Quantization for the model.",
)
@click.option(
    "--input_dims",
    type=str,
    help="The model input dimensions, specified as a JSON array",
)
@click.option(
    "--input_file",
    type=str,
    help="The model input filepath",
)
@click.option(
    "-y",
    "--yes",
    "auto_confirm",
    is_flag=True,
    help="Skip all confirmation input from the user.",
)
@click.option(
    "-o",
    "--organization_id",
    "--org_id",
    type=int,
    help="The ID of the Organization to submit the model to",
)
@click.option(
    "-g",
    "--group_id",
    help="The ID of the group to submit the model to",
)
def submit_model(
    organization_id,
    model_file_path,
    model_script_args,
    model_name,
    auto_confirm,
    quantization,
    input_dims,
    input_file,
    group_id,
    **kwargs,
):
    """Submit a model to AutoDL."""

    # Priority: flags, then configCache, then inference, then interactive user input
    environment = kwargs["environment"]

    if organization_id is None:
        organization_id = pick_organization_id(environment)
    else:
        verify_organization_id_access(environment, organization_id)

    (
        model_file,
        inferred_model_name,
        framework,
        inferred_quantization,
        inferred_input_dims,
    ) = analyze_model_file(model_file_path, model_script_args)

    (
        model_name,
        quantization,
        input_dims,
        input_file,
    ) = prompt_for_missing_model_info(
        model_name,
        quantization,
        input_dims,
        input_file,
        inferred_model_name,
        inferred_quantization,
        inferred_input_dims,
    )
    model_config = {
        "name": model_name,
        "framework": framework,
        "quantization": quantization,
        "inputs": input_dims,
        "group_id": group_id,
    }

    print(
        "The details for your model are as follows:\n"
        + f"{json.dumps(model_config, indent=4)}\n"
    )

    if not auto_confirm:
        click.confirm(
            text="\n" + "Are you sure you want to upload that to AutoDL?",
            abort=True,
            default=True,
        )

    model_link = autodl.upload_model(
        environment, organization_id, model_config, model_file, input_file
    )
    print(f"\nDone!\nSee {model_link}")
