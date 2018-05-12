# GitHub User Manager

This tool talks to the Github API and returns a list of users that belong to team for an organisation.

It will return the login name, if the user currently has a local account and their public key.

The aim of this tool is that it can be used to manage users on hosts according to your team lists in Github.

## Current state of play

  * it can list current people in an team, return their public keys and if they have a local account.

## Future

  * it can add and remove users from local accounts according to any Github movement out of a team.

## Example:

This requires a valid Github personal token with read access to an org, and read access to public key. The token should
be in exported as an environment variable: `export GITHUB_AUTH_KEY=<key>`

```
$ python github_users.py list-users --org sinfield --team cafe
INFO: Listing github users

| Login         | On local host   | Public key                   |
|---------------+-----------------+------------------------------|
| elaine        | Not Present     | ssh-rsa AAAAB3Nz....MlBBUQ== |
| kramer        | Not Present     | ssh-rsa AAAAB3Nz....g60SLks9 |
| gerry         | Not Present     | ssh-rsa AAAAB3Nz....B3FpFQ== |
| george        | Not Present     | ssh-rsa AAAAB3Nz....f1VrXQ== |
```

```
python github_users.py

github_users.py 0.0.1

This manages Github users on local Linux systems - using an organisation's team lists

usage: github_user (sub-commands ...) [options ...] {arguments ...}

Fetches Github user from an Github org team, and creates user accounts and public ssh keys

commands:

  add-users
    add users from a team

  list-users
    lists users for a github team, tests to see if they have local accounts, and displays their public keys

  purge-users
    purge users from a team

optional arguments:
  -h, --help            show this help message and exit
  --debug               toggle debug output
  --quiet               suppress all output
  -o ORG, --org ORG     Github organisation name
  -t TEAM, --team TEAM  Github team that users belong to
  -s, --sudo            Add user to sudo (default: false)
```
