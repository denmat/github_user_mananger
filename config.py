import os


class Config():
    @classmethod
    def version(cls):
        return '0.0.1'

    @classmethod
    def starting_uid_number(cls):
        return 3333

    @classmethod
    def github_auth_key(cls):
        try:
            key = os.environ['GITHUB_AUTH_KEY']
        except KeyError:
            print("You must have your GITHUB_AUTH_KEY in your environment")
        return key

