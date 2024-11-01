import boto3

from ...py.griptape_settings import GriptapeSettings
from ..drivers.gtUIBaseDriver import gtUIBaseDriver

DEFAULT_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
DEFAULT_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
DEFAULT_AWS_DEFAULT_REGION = "AWS_DEFAULT_REGION"


def start_session(aws_access_key_id=None, aws_secret_access_key=None, region_name=None):
    settings = GriptapeSettings()
    if not aws_access_key_id:
        aws_access_key_id = settings.get_settings_key_or_use_env(
            DEFAULT_AWS_ACCESS_KEY_ID
        )
    if not aws_secret_access_key:
        aws_secret_access_key = settings.get_settings_key_or_use_env(
            DEFAULT_AWS_SECRET_ACCESS_KEY
        )
    if not region_name:
        region_name = settings.get_settings_key_or_use_env(DEFAULT_AWS_DEFAULT_REGION)
    try:
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
        return session
    except Exception as e:
        print(f"Failed to create session: {e}")
        return None


class gtUIAmazonBedrockSession(gtUIBaseDriver):
    DESCRIPTION = "Starts a session with Amazon"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "aws_access_key_id_env_var": (
                    "STRING",
                    {"default": DEFAULT_AWS_ACCESS_KEY_ID},
                ),
                "aws_secret_access_key_env_var": (
                    "STRING",
                    {"default": DEFAULT_AWS_SECRET_ACCESS_KEY},
                ),
                "aws_default_region_env_var": (
                    "STRING",
                    {"default": DEFAULT_AWS_DEFAULT_REGION},
                ),
            }
        }

    RETURN_TYPES = ("SESSION",)
    RETURN_NAMES = ("SESSION",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Agent Configs"

    def build_params(self, **kwargs):
        params = {}
        aws_access_key_id = self.getenv(
            kwargs.get("aws_access_key_id_env_var", DEFAULT_AWS_ACCESS_KEY_ID)
        )
        aws_secret_access_key = self.getenv(
            kwargs.get("aws_secret_access_key_env_var", DEFAULT_AWS_SECRET_ACCESS_KEY)
        )
        region_name = self.getenv(
            kwargs.get("aws_default_region_env_var", DEFAULT_AWS_DEFAULT_REGION)
        )

        params["aws_access_key_id"] = aws_access_key_id
        params["aws_secret_access_key"] = aws_secret_access_key
        params["region_name"] = region_name

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        session = start_session(
            aws_access_key_id=params.get("aws_access_key_id"),
            aws_secret_access_key=params.get("aws_secret_access_key"),
            region_name=params.get("region_name"),
        )
        return (session,)
