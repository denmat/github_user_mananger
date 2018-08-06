import subprocess
import pwd
import grp
import os
from config import Config as Configuration

class UserDeleteFailed(Exception):
    pass

class UserAddFailed(Exception):
    pass

class UserManagement():
    @classmethod
    def starting_user_id(cls):
        return Configuration.starting_uid_number()

    @classmethod
    def user_exist(cls, login, output=False):
        try:
            pwd.getpwnam(login)
            if output:
                print('User {} on local system'.format(login))
            return True
        except KeyError:
            return False

    def group_exist(self, github_team):
        try:
            grp.getgrnam(github_team)
            return True
        except KeyError:
            return False

    def add_user(self, login, github_team, key):
        _github_team = github_team.lower().replace(' ', '_')
        if not self.group_exist(_github_team):
            self.add_group(_github_team)

        try:
            print('adding {}'.format(login))
            subprocess.run(['useradd', '-m', '-G', _github_team, login], check=True)
            self.add_ssh_pub_key(login, key)
        except subprocess.CalledProcessError:
            raise UserAddFailed("Failed to add {} add system".format(login))

    def add_group(self, github_team):
        try:
            subprocess.run(['groupadd', github_team], check=True)
        except subprocess.CalledProcessError:
            raise GroupAddFailed("Failed to add {} to system".format(github_team))

    def purge_user(self, login):
        try:
            run = subprocess.run(['userdel', '-r', login], stdout=subprocess.PIPE, stderr=subprocess.PIPE )
            if run.returncode == 12:
                print("Can't remove {}, does not own home directory".format(login))
            if run.returncode == 6:
                print("User {} already deleted".format(login))
        except subprocess.CalledProcessError:
            raise UserDeleteFailed("Failed to remove {} from system".format(login))

    def add_ssh_pub_key(self, user, public_key):
        if not public_key:
            return "No public key provided"
        _dir = '/home/' + user + '/.ssh'
        _file = 'authorized_keys'
        _auth_file = _dir + '/' + _file

        os.mkdir(_dir, mode=0o700)
        with open(_auth_file, 'w') as f:
            for _key in public_key:
                f.write(_key + "\n")
        os.chown(_auth_file, self.get_uid(user), self.get_gid(user))
        os.chown(_dir, self.get_uid(user), self.get_gid(user))

    def get_uid(self, login):
        return pwd.getpwnam(login)[2]

    def get_gid(self, login):
        return pwd.getpwnam(login)[3]

    def get_ids(self, uid):
        return (id for id in pwd.getpwall() if (id.pw_uid >= uid))

    def list_local_uids(self):
        for id in self.get_ids(self.starting_user_id()):
            if id.pw_uid != 65534:
                return id.pw_uid

    def list_local_logins(self):
        for id in self.get_ids(self.starting_user_id()):
            if id.pw_uid != 65534:
                yield id.pw_name
