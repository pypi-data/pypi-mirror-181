import boto3
import requests
from datetime import datetime, timezone

_aws_access_key_id = None
_aws_region = None
_aws_secret_access_key = None
_aws_session_expiration = None
_aws_session_token = None

table_name = None
identity_id = None


def get_client():
    if (
        _aws_access_key_id is None
        or _aws_secret_access_key is None
        or _aws_session_token is None
        or _aws_session_expiration is None
        or _aws_region is None
        or _aws_session_expiration < datetime.now(timezone.utc)
    ):
        _fetch_credentials()

    return boto3.client(
        "dynamodb",
        aws_access_key_id=_aws_access_key_id,
        aws_secret_access_key=_aws_secret_access_key,
        aws_session_token=_aws_session_token,
        region_name=_aws_region,
    )


def _fetch_credentials():
    from spackle import api_key, api_base

    global table_name
    global identity_id
    global _aws_access_key_id
    global _aws_region
    global _aws_secret_access_key
    global _aws_session_token
    global _aws_session_expiration

    session = requests.post(
        f"{api_base}/auth/session",
        headers={"Authorization": f"Bearer {api_key}"},
    ).json()

    sts_client = boto3.client("sts")
    credentials = sts_client.assume_role_with_web_identity(
        RoleArn=session["role_arn"],
        RoleSessionName=session["account_id"],
        WebIdentityToken=session["token"],
    )

    identity_id = session["identity_id"]
    table_name = session["table_name"]
    _aws_access_key_id = credentials["Credentials"]["AccessKeyId"]
    _aws_region = session["aws_region"]
    _aws_secret_access_key = credentials["Credentials"]["SecretAccessKey"]
    _aws_session_token = credentials["Credentials"]["SessionToken"]
    _aws_session_expiration = credentials["Credentials"]["Expiration"]
