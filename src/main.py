from requests.structures import CaseInsensitiveDict
from requests import get, post
from config import Vars
from time import sleep
from json import dumps
from db import Repo
from datetime import datetime

# This functio returns the last commit done on the repo
# if status_code of requests is 200, then it returns the latest commit date else None
def get_repo_latest_commit(src_repo: str):

    url = "https://api.github.com/repos/{}/commits".format(src_repo["repo"])

    # if branch specified, use it
    if src_repo["branch"]:
        url += "?sha={}".format(src_repo["branch"])

    # get the data from api
    resp = get(url)

    if resp.status_code == 200:
        return resp.json()[0]["commit"]["author"]["date"]
    return None


# function used to send a repository dispatch event to specified github repo
# uses personal access token to authenticated the request
# if status_code is 204, then it returns True else False
def send_repo_action(dest_repo: dict):
    url = "https://api.github.com/repos/{}/dispatches".format(dest_repo["repo"])

    # format the headers
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/vnd.github.v3+json"
    headers["Authorization"] = "Bearer {}".format(Vars.GH_PAT)
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    # the data we are sending in the request
    data = dumps({"event_type": Vars.EVENT_TYPE})

    # send the request
    resp = post(url, headers=headers, data=data)

    return resp.status_code == 204


# main funtion to execute the code
def main():
    print("Running script...")
    while True:
        for repo in Vars.REPOSITORY_PAIR:
            src_repo = repo["src"]
            dest_repo = repo["dest"]

            last_commit_date = get_repo_latest_commit(src_repo)
            if last_commit_date is None:
                print("Error getting last commit date for {}".format(src_repo["repo"]))
                continue

            last_commit_date = datetime.strptime(last_commit_date, "%Y-%m-%dT%H:%M:%SZ")

            last_commit_db = Repo.update_repo(src_repo, last_commit_date)

            # last commit date in db is None, so we need to send the dispatch event
            # it is the first time we are running the script with the repo
            if (last_commit_date > last_commit_db) or (last_commit_db is None):
                if send_repo_action(dest_repo):
                    print(
                        "Successfully sent repository_dispatch event: {} to {}".format(
                            Vars.EVENT_TYPE, src_repo["repo"]
                        )
                    )
                else:
                    print(
                        "Failed to send repository_dispatch event: {} to {}".format(
                            Vars.EVENT_TYPE, src_repo["repo"]
                        )
                    )
                if Vars.SLEEP_TIME:
                    print(f"Sleeping for {Vars.SLEEP_TIME} minutes...")
                    sleep(Vars.SLEEP_TIME * 60)
            else:
                print(
                    "No new commits found on {} since last dispatch event".format(
                        src_repo["repo"]
                    )
                )

        print("Done Running!")
        print(f"Will run again after {Vars.TIME_PERIOD} minutes...")
        sleep(Vars.TIME_PERIOD * 60)


if __name__ == "__main__":
    main()
