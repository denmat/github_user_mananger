from config import Config as Configuration
from lib.github_users import GithubUsers as github_users

class GithubUserManager():

    @classmethod
    def list_users(cls, org, team):
        gh = github_users(org, team)
        data = gh.list_users(org, team)
        return data

    def add_users(self):
        print('here')
    def purge_users(self):
        print('here')

