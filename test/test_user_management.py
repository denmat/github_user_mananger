import pytest
import mock
import pwd
import grp
import subprocess
from lib.user_management import UserManagement

@mock.patch('pwd.getpwnam')
def test_user_exist(mock_pwd):
    login = 'elaine'
    UserManagement.user_exist(login)
    pwd.getpwnam.assert_called_with('elaine')

@mock.patch('grp.getgrnam')
def test_group_exist(mock_grp):
    github_team = 'soup'
    UserManagement.group_exist(github_team)
    grp.getgrnam.assert_called_with('soup')

@mock.patch('subprocess.run')
@pytest.mark.parametrize("login,github_team,uid", [
    ("george", "soup", 5000) ])
def test_add_user(mock_subprocess, login, github_team, uid):
    um = UserManagement()
    um.add_user(login, github_team, uid)
    subprocess.run.assert_called_with(['useradd', '-u', 5000, '-m', '-G', 'soup', 'george'], check=True)

@mock.patch('subprocess.run')
@pytest.mark.parametrize("login,github_team,uid", [
    ("george", "soup", 5000) ])
def test_add_user(mock_subprocess, login, github_team, uid):
    um = UserManagement()
    um.add_user(login, github_team, uid)
    subprocess.run.assert_called_with(['useradd', '-u', 5000, '-m', '-G', 'soup', 'george'], check=True)

@mock.patch('subprocess.run')
@pytest.mark.parametrize("github_team", [
    ("soup") ])
def test_add_group(mock_subprocess, github_team):
    um = UserManagement()
    um.add_group(github_team)
    subprocess.run.assert_called_with(['groupadd', 'soup'], check=True)

@mock.patch('subprocess.run')
@pytest.mark.parametrize("login", [
    ("george") ])
def test_purge_user(mock_subprocess, login):
    um = UserManagement()
    um.purge_user(login)
    subprocess.run.assert_called_with(['userdel', '-r', 'george'], check=True)