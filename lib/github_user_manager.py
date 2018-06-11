import json
from config import Config as Configuration
from lib.github_users import GithubUsers as github_users
from lib.user_management import UserManagement as local_users

class GithubUserManager():

    def __init__(self, org, team, output=False):
        self.org = org
        self.team = team
        self.output = output

    def list_github_users(self):
        gh = github_users(self.org, self.team)
        data = gh.list_users()
        if self.output == 'json':
            return self._jsonify(data)
        elif self.output == 'tab':
            return self._prettify_for_tab(data)
        else:
            return data

    def list_local_users(self):
        loc_usr = []
        loc = local_users()
        for usr in loc.list_local_logins():
            loc_usr.append(usr)
        return loc_usr

    def list_gh_users_not_on_local(self, list_gh_users):
        return (gh_u for gh_u in list_gh_users if gh_u[1] == 'Not Present')

    def list_local_users_not_on_gh(self, list_gh_users, list_local_users):
        return (loc_u for loc_u in list_local_users if list_local_users not in list_gh_users)

    def add_users(self, list_gh_users, team):
        loc = local_users()
        for usr in self.list_gh_users_not_on_local(list_gh_users):
            loc.add_user(usr[0], team, usr[2])

    def purge_users(self):
        print('here')

    def _shorten_key(self, key):
        if not key:
            return 'None'
        start, end = key[:16], key[-8:]
        return start + '....' + end

    def _prettify_for_tab(self, data):
        for idx, i in enumerate(data):
            data[idx][2] = self._shorten_key(i[2])
        return data

    def _jsonify(self, data):
        return json.dumps(data)
