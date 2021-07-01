import logging
import boto3
import os
from botocore.exceptions import ClientError


def str2mdown(str):
    return str.replace("-", "\\-").replace("!", "\\!").replace(".", "\\.")


def read_ssm_parameter(param_name):
    ssm_client = boto3.client("ssm", endpoint_url=os.getenv("AWS_ENDPOINT_URL", None))
    try:
        result = ssm_client.get_parameter(Name=param_name, WithDecryption=False)
        value = result["Parameter"]["Value"]
    except (ClientError, KeyError) as e:
        logging.error(e)
        return None

    return value
