from lib.user_management import UserManagement
from github import Github
from config import Config as Configuration


class GithubUsers():

    def __init__(self, org, team):
        self.org = org
        self.team = team

    def _g(self):
        return Github(Configuration.github_auth_key())

    def _validate_org(g, org_name):
        name = g.get_organization(org_name).name
        return name

    def _get_team_id(self, g, org_name, team_name):
        teams = (team for team in g.get_organization(org_name).get_teams() if (team.name == team_name))
        for team in teams:
            return team.id

    def _team_members(self, g, org_name, team_id):
        return g.get_organization(org_name).get_team(team_id)

    def _members_logins(self, members):
        for members in members.get_members():
            yield members.login

    def _get_public_keys(self, g, login):
        for key in g.get_user(login).get_keys():
            return key.key

    def _list_users(self, org, team):
        data = []
        team_id = self._get_team_id(self._g(), self.org, self.team)
        members = self._team_members(self._g(), org, team_id)
        for member in self._members_logins(members):
            key = self._get_public_keys(self._g(), member)
            if UserManagement.user_exist(member):
                present = 'Present'
            else:
                present = 'Not Present'
            data.append([member, present, key])
        return data

    def list_users(self):
        data =  self._list_users(self.org, self.team)
        return data
