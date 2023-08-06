import os
import tempfile


class ObpAuthProvider(object):
    name = "obp"

    @staticmethod
    def get_client(
        module, with_error=False, role_arn=None, session_vars=None, client_params=None
    ):
        if client_params is None:
            client_params = {}

        import boto3
        from botocore.exceptions import ClientError
        from metaflow_extensions.outerbounds.plugins.auth_server import get_token

        token_info = get_token("/generate/aws")

        token_file = "/tmp/obp_token"

        # Write to a temp file then rename to avoid a situation when someone
        # tries to read the file after it was open for writing (and truncated)
        # but before the token was written to it.
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            f.write(token_info["token"])
            tmp_token_file = f.name
        os.rename(tmp_token_file, token_file)

        os.environ["AWS_WEB_IDENTITY_TOKEN_FILE"] = token_file
        os.environ["AWS_ROLE_ARN"] = token_info["role_arn"]
        if with_error:
            return boto3.client(module, **client_params), ClientError
        else:
            return boto3.client(module, **client_params)


AWS_CLIENT_PROVIDERS = [ObpAuthProvider]
