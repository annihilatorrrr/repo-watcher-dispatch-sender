from datetime import datetime

from pickledb_ujson import load

LocalDB = load("/app/repowatcher_local.db", True)


class Repo:
    @staticmethod
    def update_repo(repo: dict, last_commit: datetime):
        # using '/' could have some issue, so replaced with '_
        src_repo = repo["repo"].replace("/", "_")
        last_commit = LocalDB.get(src_repo)
        if not last_commit:
            LocalDB.set(src_repo, last_commit)
            return None
        LocalDB.set(src_repo, last_commit)
        return last_commit
