import subprocess
import pwd
import grp
import os
from config import Config as Configuration


class UserManagement():
    @classmethod
    def starting_user_id(cls):
        return Configuration.starting_uid_number()

    @classmethod
    def user_exist(cls, login):
        try:
            pwd.getpwnam(login)
            print('User %s on local system' % login)
            return True
        except KeyError:
            return False

    def group_exist(self, github_team):
        try:
            grp.getgrnam(github_team)
            return True
        except KeyError:
            return False

    def add_user(self, login, github_team):
        if not self.group_exist(github_team):
            self.add_group(github_team)

        try:
            print('adding %s' % login)
            subprocess.run(['useradd', '-m', '-G', github_team, login], check=True)
        except subprocess.CalledProcessError:
            raise("Failed to add %s add system" % login)

    def add_group(self, github_team):
        try:
            subprocess.run(['groupadd', github_team], check=True)
        except subprocess.CalledProcessError:
            raise("Failed to add %s to system" % github_team)

    def purge_user(self, login):
        try:
            subprocess.run(['userdel', '-r', login], check=True)
        except subprocess.CalledProcessError:
            raise("Failed to remove %s from system" % login)

    def add_ssh_pub_key(self, user, public_key):
        os.mkdir('/home/' + user + '/.ssh', mode=0o700)
        with open('/home/' + user + '/.ssh/authorized_keys') as f:
            f.w(public_key)

    def get_ids(self, uid):
        return (id for id in pwd.getpwall() if (id.pw_uid >= uid))

    def list_local_uids(self):
        for id in self.get_ids(self.starting_user_id()):
            return id.pw_uid

    def list_local_logins(self):
        for id in self.get_ids(self.starting_user_id()):
            yield id.pw_name
