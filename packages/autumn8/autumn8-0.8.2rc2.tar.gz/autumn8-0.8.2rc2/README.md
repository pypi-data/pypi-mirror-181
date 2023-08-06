# Autumn8 CLI

Autumn8 CLI is a toolkit, which allows you to easily interact programatically
with the Autumn8's ML service, AutoDL.

## Usage

To use the CLI - as a prerequisite, you'll have to log in into
autodl.autumn8.ai and generate an API key for you CLI from your Profile page.

Follow the instructions on https://autodl.autumn8.ai/profile
to authenticate your CLI.

## Available commands

```
Usage: autumn8-cli [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  login
  submit-model
  test-connection
```

### Login

```
Usage: autumn8-cli login [OPTIONS]

Options:
  -u, --user_id TEXT  The ID of the user that the CLI will authenticate as in
                      AutoDL.
  -a, --api_key TEXT  API Key to use when authenticating in AutoDL from now
                      on.
  --help              Show this message and exit.
```

### Submit model

> TODO: mention supported formats
> TODO: describe annotation import mode

```
Usage: autumn8-cli submit-model [OPTIONS] MODEL_FILE_PATH
                                [MODEL_SCRIPT_ARGS]...

Options:
  -n, --name TEXT                 Name of the model to be used in AutoDL.
  -q, --quantization, --quants [FP32|FP16|INT8]
                                  Quantization for the model.
  --input_dims TEXT               The model input dimensions, specified as a
                                  JSON array
  --input_file TEXT               The model input filepath
  -y, --yes                       Skip all confirmation input from the user.
  -o, --organization_id, --org_id INTEGER
                                  The ID of the Organization to submit the
                                  model to
  -g, --group_id TEXT             The ID of the group to submit the model to
  --help                          Show this message and exit.
```

### Test connection

```
Usage: autumn8-cli test-connection [OPTIONS]

Options:
  -e, --environment, --env [LOCALHOST|STAGING|PRODUCTION]
                                  Environment to use
  --help                          Show this message and exit.
```
