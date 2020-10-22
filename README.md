# Secrets Wrapper Script in Python

The provided code is a modification of my old helper script / Lambda layer that read all parameters for an application and environment from Amazon Parameter Store and presents them as environment variables. This is based on this old [blog post][aws-ssm-post-link].

The wrapper consist of the secrets-wrapper.py that reads all the parameters and presents them as environment variables.

There is also an example usage of the wrapper script.

## Requirements

Parameters should be organized in parameter store according to pattern /ENV/PATH/PARAMETER_NAME then PARAMETER_NAME will be available as environment variable.

For this wrapper to be able to read the parameters the following requirements must be fulfilled:

 - The Lambda function MUST have IAM permissions to read and decrypt parameters.
 - The environment variable _APP_PARAMS_PATH_ must be present to specify the PATH of the parameters.
 - The environment variable _APP_ENV_ is optional and specify the ENV part of the parameters

## Installation and usage

First make sure all your parameters are in parameter store with the full path /ENV/PATH/PARAMETER_NAME.

Make secrets-wrapper.py executable by running

```bash
chmod +x secrets-wrapper.py
```

Install the requirements

```bash
pip3 install -r requirements.txt -t .
```

Then zip and upload everything as an Lambda Layer, full example.

```bash
#!/bin/bash

REGION=eu-north-1

cd wrapper
chmod +x secrets-wrapper.py
pip3 install -r requirements.txt -t .
cd ..

zip -r wrapper.zip .


aws lambda publish-layer-version \
 --layer-name "secrets-python-wrapper" \
 --region $REGION \
 --zip-file  "fileb://wrapper.zip"

```

To use the wrapper include the Layer in your Lambda function and make sure to set the environment variable AWS_LAMBDA_EXEC_WRAPPER to "/opt/secrets-wrapper/secrets-wrapper.py"

Or deploy the function present in the example folder.

## Invoke and test

Invoke the function using a test event. Try and access any of the parameters as environment variables.

[aws-ssm-post-link]: https://aws.amazon.com/blogs/compute/sharing-secrets-with-aws-lambda-using-aws-systems-manager-parameter-store/