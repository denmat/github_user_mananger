from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from lib.GithubUsers import GithubUsers 

VERSION = '0.0.1'

BANNER = """
github_users.py %s

This manages Github users on local Linux systems - using an organisation's team lists
""" % VERSION

class GitHubBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = "Fetches Github user from an Github org team, and creates user accounts and public ssh keys"
        arguments = [
            ( ['-o', '--org'],
              dict(action='store', help='Github organisation name') ),
            ( ['-t', '--team'],
              dict(action='store', help='Github team that users belong to') ),
            ( ['-s', '--sudo'],
              dict(action='store_true', help='Add user to sudo (default: false)') )
            ]

    @expose(hide=True)
    def default(self):
        print(BANNER)
        app.args.print_help()

    @expose(help="lists users for a github team, tests to see if they have local accounts, and displays their public keys")
    def list_users(self):
        self.app.log.info("Listing github users")
        github = GithubUsers(self.app.pargs.org, self.app.pargs.team)
        data = github.list_users(self.app.pargs.org, self.app.pargs.team)
        headers = [ 'Login', 'On local host', 'Public key' ]
        self.app.render(data, headers=headers)

    @expose(help="add users from a team")
    def add_users(self):
        self.app.log.info("Inside add_users")

    @expose(help="purge users from a team")
    def purge_users(self):
        self.app.log.info("Inside purge_users")
    
class GitHubUserCli(CementApp):
    class Meta:
        label = 'github_user'
        base_controller = 'base'
        extensions = ['tabulate']
        output_handler = 'tabulate'
        handlers = [GitHubBaseController]

with GitHubUserCli() as app:
    app.run()