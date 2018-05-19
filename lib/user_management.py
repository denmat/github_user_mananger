import subprocess
import pwd
import grp
from config import Config as Configuration

class UserManagement():
    @classmethod
    def starting_user_id(cls):
        return Configuration.starting_uid_number()

    @classmethod
    def user_exist(cls, login):
        try:
            pwd.getpwnam(login)
            return True
        except KeyError:
            return False

    @classmethod
    def group_exist(self, github_team):
        try:
            grp.getgrnam(github_team)
            return True
        except KeyError:
            return False

    def add_user(self, login, github_team, uid):
        try:
            subprocess.run([ 'useradd','-u', uid, '-m', '-G', github_team, login], check=True)
        except subprocess.CalledProcessError:
            raise("Failed to add %s add system" % login)

    def add_group(self, github_team):
        try:
            subprocess.run([ 'groupadd', github_team], check=True)
        except subprocess.CalledProcessError:
            raise("Failed to add %s to system" % github_team)

    def purge_user(self, login):
        try:
            subprocess.run([ 'userdel', '-r', login], check=True)
        except subprocess.CalledProcessError:
            raise("Failed to remove %s from system" % login)

    def get_ids(self, uid):
        return (id for id in pwd.getpwall() if (id.pw_uid >= uid))

    def list_local_uids(self):
        for id in self.get_ids(self.starting_user_id()):
            return id.pw_uid

    def list_local_logins(self):
        for id in self.get_ids(self.starting_user_id()):
            return id.pw_name
