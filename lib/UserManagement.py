import os
import pwd
import grp

class UserManagement():

    @classmethod
    def user_exist(cls, login):
        try:
            pwd.getpwnam(login)
            return True
        except KeyError:
            return False

    def group_exist(self, login):
        return True

    def add_user(self, login, group):
        useradd = login
        os.execute(useradd)

    def add_group(self, github_team):
        os.execute(groupadd)

    def user_purge(self, login):
        os.execute(userdel)
