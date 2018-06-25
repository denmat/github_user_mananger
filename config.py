import os
import boto3


class Config():
    @classmethod
    def version(cls):
        return '0.0.1'

    @classmethod
    def starting_uid_number(cls):
        return 1000

    @classmethod
    def github_auth_key(cls):
        try:
            _env_key = os.environ['GITHUB_AUTH_KEY']
            if _env_key.split(':')[0] == 'secretsmanager':
                auth, secret_id, region = _env_key.split(':')
                client = boto3.client('secretsmanager', region)
                key = client.get_secret_value(SecretId=secret_id)['SecretString']
                return key
            else:
                return _env_key
        except KeyError:
            print("You must have your GITHUB_AUTH_KEY in your environment")

