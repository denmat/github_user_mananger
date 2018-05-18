import subprocess
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
        except CalledProcessError:
            raise("Failed to add %s add system" % login)

    def add_group(self, github_team):
        try:
            subprocess.run([ 'groupadd', github_team], check=True)
        except CalledProcessError:
            raise("Failed to add %s to system" % github_team)

    def purge_user(self, login):
        try:
            subprocess.run([ 'userdel', '-r', login], check=True)
        except CalledProcessError:
            raise("Failed to remove %s from system" % login)

    def get_ids(self, uid):
        return (id for id in pwd.getpwall() if (id.pw_uid > uid))

    def list_local_uids(self, starting_uid):
        for id in self.get_ids(starting_uid):
            return id
