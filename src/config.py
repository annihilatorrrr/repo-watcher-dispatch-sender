from utils import prettify_repository_pair, load_var


class Vars:
    # github personal access token
    GH_PAT = load_var("GH_PAT")

    # repository pair in this form: divkix/proxygrab@main:octocat/proxygrab
    REPOSITORY_PAIR = prettify_repository_pair(load_var("REPOSITORY_PAIR"))

    # After how many minutes should the script run to send repo action
    TIME_PERIOD = int(load_var("TIME_PERIOD", "60"))

    # After how many minutes should each request be made, i.e. gap between 2 requests
    SLEEP_TIME = int(load_var("SLEEP_TIME", "0"))

    # Type of event to be sent to the Github repo
    EVENT_TYPE = load_var("EVENT_TYPE", "upstream_update")
