from __future__ import annotations

import os

import git


class GitRepo:
    def __init__(
        self, git_client: GitClient, url, branch, username, password, dir
    ) -> None:
        self.url = url
        self.git_client = git_client
        self.branch = branch
        self.username = username
        self.password = password
        self.dir = dir

    def commit_all_changes(self, branch):
        if branch == None:
            branch = self.branch

        current_dir = os.getcwd()
        os.chdir(self.dir)

        self.git_client.execute_git_command(["add", "."])
        diff_check = self.git_client.execute_git_command(["diff", "--staged"])
        if not diff_check:
            print(f"Nothing to commit in target repo: {self.dir}")
        else:
            self.git_client.execute_git_command(
                ["commit", "-m", "Bootstrap config update"]
            )
            self.git_client.execute_git_command(["push", "-f", "origin", branch])

        os.chdir(current_dir)


class GitClient:
    def __init__(self) -> None:
        # TODO: Don't think this will be cross platform
        self.client = git.Git(os.path.join(os.path.expanduser("~"), "git", "GitPython"))

    def execute_git_command(self, args):
        try:
            result = self.client.execute(["git", *args])
            return result
        except Exception as e:
            raise Exception("Git command failed") from e

    def clone_repo(
        self, url, destination_dir, branch="main", username=None, password=None
    ) -> GitRepo:
        if username and password:
            self.execute_git_command(
                [
                    "clone",
                    "-b",
                    branch,
                    f"https://{username}:{password}@{url}",
                    destination_dir,
                ]
            )
        else:
            self.execute_git_command(
                [
                    "clone",
                    "-b",
                    branch,
                    f"https://{url}",
                    destination_dir,
                ]
            )
        return GitRepo(
            self,
            url,
            branch=branch,
            username=username,
            password=password,
            dir=destination_dir,
        )
