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
        arguments = [
            (['-o', '--org'],
                dict(action='store', help='Github organisation name')),
            (['-t', '--team'],
                dict(action='store', help='Github team that users belong to')),
            (['--output'],
                dict(action='store', help="Output format, 'tab' (default) or 'json'")),
            (['-s', '--sudo'],
                dict(action='store_true', help='Add user to sudo (default: false)'))
            ]

    @expose(hide=True)
    def default(self):
        print(BANNER)
        app.args.print_help()

    @expose(help="lists users for a github team, tests to see if they have local accounts, and displays their public keys")
    def list_github_users(self):
        self.app.log.info("Listing github users")
        org, team = self.app.pargs.org, self.app.pargs.team
        data = GithubUserManager.list_github_users(org, team)
        headers = ['Login', 'On local host', 'Public key']
        self.app.render(data, headers=headers)

    @expose(help="lists users for a local users")
    def list_local_users(self):
        self.app.log.info("Listing local users")
        gh = GithubUserManager()
        data = gh.list_local_users()
        if 'nobody' in data:
            print('No local users with uids over or eqaul to: %s' % Configuration.starting_uid_number())
        else:
            headers = ['Login']
            self.app.render(data, headers=headers)

    @expose(help="add users from a team")
    def add_users(self):
        self.app.log.info("Inside add_users")
        org, team = self.app.pargs.org, self.app.pargs.team
        github_users = GithubUserManager.list_github_users(org, team)
        gh = GithubUserManager()
        gh.add_users(github_users, team)

    @expose(help="purge users from a team")
    def purge_users(self):
        self.app.log.info("Inside purge_users")


class GitHubUserCli(CementApp):
    class Meta:
        label = 'github_user_manager'
        base_controller = 'base'
        extensions = ['tabulate']
        output_handler = 'tabulate'
        handlers = [GitHubBaseController]

with GitHubUserCli() as app:
    app.run()
