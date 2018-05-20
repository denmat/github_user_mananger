from config import Config as Configuration
from lib.github_users import GithubUsers as github_users
from lib.user_management import UserManagement as local_users

class GithubUserManager():

    @classmethod
    def list_github_users(cls, org, team):
        gh = github_users(org, team)
        data = gh.list_users(org, team)
        return data

    def list_local_users(self):
        loc_usr = []
        loc = local_users()
        for usr in loc.list_local_logins():
            loc_usr.append(usr)
        return loc_usr

    def list_gh_users_not_on_local(self, list_gh_users, list_local_users):
        return (gh_u for gh_u in list_gh_users if list_gh_users not in list_local_users)

    def list_local_users_not_on_gh(self, list_gh_users, list_local_users):
        return (loc_u for loc_u in list_local_users if list_local_users not in list_gh_users)

    def add_users(self, list_gh_users, list_local_users):
        users_to_purge = []
        print('here')

    def purge_users(self):
        print('here')

