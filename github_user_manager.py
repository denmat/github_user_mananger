from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from lib.github_user_manager import GithubUserManager
from config import Config as Configuration


BANNER = """
github_users_manager.py %s

This manages Github users on local Linux systems - using an organisation's team lists
""" % Configuration.version()


class GitHubBaseController(CementBaseController):

    class Meta:
        label = 'base'
        description = "Fetches Github user from an Github org team, and creates user accounts and public ssh keys"

    @expose(hide=True)
    def default(self):
        print(BANNER)
        app.args.print_help()

    @expose(help="lists users for a local users")
    def list_local_users(self):
        self.app.log.info("Listing local users")
        gh = GithubUserManager(None, None)
        data = gh.list_local_users()
        if data == []:
            print('No local users with uids over or eqaul to: %s' % Configuration.starting_uid_number())
        else:
            print(data)
            headers = ['Login']
            self.app.render(data, headers=headers)

class GitHubApiBaseController(CementBaseController):
    class Meta:
         label = 'github'
         description = 'Interacting with github api'
         arguments = [
            (['-o', '--org'],
                dict(action='store', dest='org', help='Github organisation name')),
            (['-t', '--team'],
                dict(action='store', dest='team', help='Github team that users belong to')),
            (['--output'],
                dict(action='store', dest='output', help="Output format, 'tab' (default) or 'json'"))
            ]

    @expose(help="lists users for a github team, tests to see if they have local accounts, and displays their public keys")
    def list_github_users(self):
        org, team, output = self.app.pargs.org, self.app.pargs.team, self.app.pargs.output
        if output == None:
            output = 'tab'
        gh = GithubUserManager(org, team, output)
        data = gh.list_github_users()
        if output == 'json':
            print(data)
        else:
            self.app.log.info("Listing github users")
            headers = ['Login', 'On local host', 'Public key']
            self.app.render(data, headers=headers)

    @expose(help="add users from a team")
    def add_users(self):
        self.app.log.info("Inside add_users")
        org, team = self.app.pargs.org, self.app.pargs.team
        gh = GithubUserManager(org, team)
        github_users = gh.list_github_users()
        gh.add_users(github_users, team)

    @expose(help="purge users from a team")
    def purge_users(self):
        self.app.log.info("Inside purge_users")
        org, team = self.app.pargs.org, self.app.pargs.team
        gh = GithubUserManager(org, team)
        github_users = gh.list_github_users()
        gh.purge_users(github_users)

class GitHubUserCli(CementApp):
    class Meta:
        label = 'github_user_manager'
        base_controller = 'base'
        extensions = ['tabulate']
        output_handler = 'tabulate'
        handlers = [
          GitHubBaseController,
          GitHubApiBaseController
          ]

with GitHubUserCli() as app:
    app.run()
