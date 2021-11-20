from os import getcwd

from prettyconf import Configuration
from prettyconf.loaders import EnvFile, Environment

from utils import prettify_repository_pair

env_file = f"{getcwd()}/.env"
config = Configuration(loaders=[Environment(), EnvFile(filename=env_file)])


class Vars:
    # github personal access token
    GH_PAT = config("GH_PAT", default="")

    # repository pair in this form: divkix/proxygrab@main:octocat/proxygrab
    REPOSITORY_PAIR = prettify_repository_pair(config("REPOSITORY_PAIR", default=""))

    # After how many minutes should the script run to send repo action
    TIME_PERIOD = int(config("TIME_PERIOD", default="60"))

    # After how many minutes should each request be made, i.e. gap between 2 requests
    SLEEP_TIME = int(config("SLEEP_TIME", default="0"))

    # Type of event to be sent to the Github repo
    EVENT_TYPE = config("EVENT_TYPE", default="upstream_update")
