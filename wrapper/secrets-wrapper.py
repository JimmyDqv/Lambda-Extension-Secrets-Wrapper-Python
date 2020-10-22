#!/usr/bin/env python3

import boto3
import json
import os

LAMBDA_WRAPPER_NAME = "secrets-wrapper"


def debug_print(message):
    print(message, flush=True)


def error_print(message):
    print(message, flush=True)


def load_secrets():

    if not 'APP_PARAMS_PATH' in os.environ:
        error_print(
            f"{LAMBDA_WRAPPER_NAME} unable to load secrets APP_PARAMS_PATH not found")
        return

    app_config_path = os.environ['APP_PARAMS_PATH']
    if 'APP_ENV' in os.environ:
        env = os.environ['APP_ENV']
        full_config_path = '/' + env + '/' + app_config_path
    else:
        full_config_path = '/' + app_config_path

    debug_print(
        f"{LAMBDA_WRAPPER_NAME} Loading secrets for path {full_config_path}")

    try:
        client = boto3.client('ssm')
        # Get all parameters for this app
        param_details = client.get_parameters_by_path(
            Path=full_config_path,
            Recursive=False,
            WithDecryption=True
        )

        # Loop through the returned parameters and populate the ConfigParser
        if 'Parameters' in param_details:
            for param in param_details.get('Parameters'):
                debug_print(f"Found param: {param}")
                param_name = param.get('Name').split("/")[-1]
                debug_print(f"Name: {param_name}")
                param_value = param.get('Value')
                debug_print(f"Value: {param_value}")
                os.environ[param_name] = param_value
    except:
        debug_print(f"{LAMBDA_WRAPPER_NAME} could not load from SSM")
        raise Exception(f"{LAMBDA_WRAPPER_NAME} could not load from SSM")


def main():
    load_secrets()

    # Start the function
    args = os.sys.argv[1:]
    os.system(" ".join(args))


if __name__ == "__main__":
    main()
