# code-assistant

A FastHTML app that makes FastHTML apps.

## Install and run

Install with pip:

    pip install code-assistant

Run:

    code-assistant

this will start the web server on port 5001 and will create a generated_apps directory on your current working directory. You can override this directory by setting the CA_GENERATED_APPS_DIR environment variable.

    export CA_GENERATED_APPS_DIR="~/my_apps"
    code-assistant

## Run as an isolated program

use pipx or uvx if you're a uv user to run as an isolated program:

    pipx run code-assistant

or

    uvx code-assistant

