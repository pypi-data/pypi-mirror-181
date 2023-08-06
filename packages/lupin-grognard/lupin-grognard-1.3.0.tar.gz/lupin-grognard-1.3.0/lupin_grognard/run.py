import os
import sys
from typing import Optional

from dotenv import load_dotenv
import typer

from lupin_grognard.__init__ import __version__
from lupin_grognard.core.check import check_commit_with_commitizen
from lupin_grognard.core.git import Git
from .core.tools.utils import (
    create_branch_list,
    display_current_branch_name,
    display_number_of_commits_to_check,
    generate_commit_list,
    generate_commits_range_to_check,
)

load_dotenv()
GROG_BRANCHES = os.getenv("GROG_BRANCHES")


cli = typer.Typer()


@cli.command()
def version():
    print(f"Version: {__version__}")


@cli.command()
def check_commits(
    all: bool = typer.Option(
        False, "--all", "-a", help="check all commits from initial commit"
    ),
    branches_name: Optional[str] = typer.Argument(
        default="master, main, dev, development", envvar="GROG_BRANCHES"
    ),
):
    """
    Run 'git log --first-parent --pretty=oneline -50' command

    Check every commit message with commitizen since the last request to merge one of the branches from branches_name

    - With --all option :
    grog check-commits [--all or -a] to check all commits from initial commit

    - With branches_name argument: grog check-commits "branch_1, branch_2..."

    You can set GROG_BRANCHES env var in .env, gitlab, github...
    """
    git = Git()
    if all:  # --all option
        git_log = git.get_log()
    else:
        git_log = git.get_log(max_line_count=50)
    if git_log.stderr:
        print(f"git error {git_log.return_code}\n{git_log.stderr}")
        sys.exit(1)

    branch_list = create_branch_list(branches_name=branches_name)
    commit_list = generate_commit_list(data=git_log.stdout)
    display_current_branch_name()

    if all:  # --all option
        display_number_of_commits_to_check(commit_list=commit_list)
        check_commit_with_commitizen(commits=commit_list)
    else:
        commit_range_list_to_check = generate_commits_range_to_check(
            branch_list=branch_list, commit_list=commit_list
        )
        display_number_of_commits_to_check(commit_list=commit_range_list_to_check)
        check_commit_with_commitizen(commits=commit_range_list_to_check)
