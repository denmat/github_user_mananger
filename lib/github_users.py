from lib.user_management import UserManagement as local_users
from github import Github
from config import Config as Configuration


class GithubUsers():

    def __init__(self, org, team):
        self.org = org
        self.team = team

    @staticmethod
    def _g():
    	return Github(Configuration.github_auth_key())

    @staticmethod
    def _validate_org(g, org_name):
        name = g.get_organization(org_name).name
        return name

    @staticmethod
    def _get_team_id(g, org_name, team_name):
        teams = (team for team in g.get_organization(org_name).get_teams() if (team.name == team_name))
        for team in teams:
            return team.id

    @staticmethod
    def _team_members(g, org_name, team_id):
        return g.get_organization(org_name).get_team(team_id)

    @staticmethod
    def _members_logins(members):
        for members in members.get_members():
            yield members.login

    @staticmethod
    def _get_public_keys(g, login):
        for key in g.get_user(login).get_keys():
            return key.key

    @staticmethod
    def _shorten_key(key):
        if not key:
            return 'None'
        start, end = key[:16], key[-8:]
        return start + '....' + end

    @staticmethod
    def local_user_exist(login):
        local_users.user_exist(login)

    def list_users(self, org, team):
        data = []
        team_id = self._get_team_id(self._g(), org, team)
        members = self._team_members(self._g(), org, team_id)
        for member in self._members_logins(members):
            key = self._get_public_keys(self._g(), member)
            if self.local_user_exist(member):
                present = 'Present'
            else:
                present = 'Not Present'
            data.append([member, present, self._shorten_key(key)])
        return data
