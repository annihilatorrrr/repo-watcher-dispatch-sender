from os import environ

from errors import InvalidRepositoryFormat


# return the repository pair as a list of dict in the format:
# [{'repo': 'github_username/repo_name', 'branch': 'branch_name'}]
# By default it uses push on any branche for src
# However, a branch can be specified for src, but destination will
# always use master or default branch
# or the main/master or whatever the master branch is set as
def prettify_repository_pair(repo_pair: str):
    raw_repos = list(repo_pair.split(","))
    list_of_repos = []
    for repo in raw_repos:
        # repo: divkix/proxygrab@main:octocat/proxygrab
        repo_spltter = repo.split(":")
        branch_src = repo_spltter[0].split("@")
        branch_dest = repo_spltter[-1].split("@")

        # just to make sure we do stuff correctly
        if len(branch_dest) == 2:
            branch_dest = branch_dest[0]

        if len(repo_spltter) == 2:
            proper_dict = {}
            for source, branch_split in {
                "src": branch_src,
                "dest": branch_dest,
            }.items():

                # len(branch_dest) == 1 means that the branch is not specified
                # this is how it should be
                if len(branch_split) == 1:
                    proper_dict[source] = {"repo": branch_split[0]}
                elif len(branch_split) == 2:
                    proper_dict[source] = {
                        "repo": branch_split[0],
                        "branch": branch_split[-1],
                    }
            list_of_repos.append(proper_dict)

        else:
            raise InvalidRepositoryFormat()

    return list_of_repos


# load the var using environ.get
def load_var(var_name, def_value=None):
    return environ.get(var_name, def_value)
