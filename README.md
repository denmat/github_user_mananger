# GitHub User Manager

This tool talks to the Github API and returns a list of users that belong to team for an organisation.

It will return the login name, if the user currently has a local account and their public key.

The aim of this tool is that it can be used to manage users on hosts according to your team lists in Github.

While we could make this tool do more, like manage sudo and set base UID, it is probably best to let other configuration management
tools handle those. 

## Current state of play

  * it can list current people in an team, return their public keys and if they have a local account.
  * it can add and remove users from local accounts according to any Github movement out of a team.


## Example:

This requires a valid Github personal token with read access to an org, and read access to public key. The token should
be in exported as an environment variable: `export GITHUB_AUTH_KEY=<key>`

If you wish to use AWS Secrets Manager to store your GitHub token, you should export the `GITHUB_AUTH_KEY` like so:

```bash
export GITHUB_AUTH_KEY=secretsmanager:<KeyName>:<region>
```

```text
$ python ./github_user_manager.py list-github-users --org sinfield --team cafe
INFO: Listing github users

| Login         | On local host   | Public key                   |
|---------------+-----------------+------------------------------|
| elaine        | Not Present     | ssh-rsa AAAAB3Nz....MlBBUQ== |
| kramer        | Not Present     | ssh-rsa AAAAB3Nz....g60SLks9 |
| gerry         | Not Present     | ssh-rsa AAAAB3Nz....B3FpFQ== |
| george        | Not Present     | ssh-rsa AAAAB3Nz....f1VrXQ== |
```

```text
./github_user_manager.py --help
usage: github_user_manager (sub-commands ...) [options ...] {arguments ...}

Fetches Github user from an Github org team, and creates user accounts and public ssh keys

commands:

  add-users
    add users from a team

  list-github-users
    lists users for a github team, tests to see if they have local accounts, and displays their public keys

  list-local-users
    lists users for a local users

  purge-users
    purge users from a team

optional arguments:
  -h, --help            show this help message and exit
  --debug               toggle debug output
  --quiet               suppress all output
  -o ORG, --org ORG     Github organisation name
  -t TEAM, --team TEAM  Github team that users belong to
  --output OUTPUT       Output format, 'tab' (default) or 'json'
  ```

