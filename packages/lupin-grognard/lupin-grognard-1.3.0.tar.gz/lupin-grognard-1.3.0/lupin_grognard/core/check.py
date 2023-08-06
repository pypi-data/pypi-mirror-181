import sys
from typing import List

import emoji

from commitizen.commands.check import Check
from commitizen.config.base_config import BaseConfig

from lupin_grognard.core.commit import Commit
from lupin_grognard.core.config import (
    PATTERN,
    FAILED,
    TITLE_FAILED,
    BODY_FAILED,
    SUCCESS,
    EMOJI_CHECK,
    EMOJI_CROSS,
)


def check_commit_with_commitizen(commits: List) -> List:
    # commitizen config
    config = BaseConfig()
    args = {"message": ""}
    commitizen = Check(config=config, arguments=args)

    title_checklist = []
    body_checklist = []
    for c in commits:
        commit = Commit(commit=c)
        check_commit = commitizen.validate_commit_message(
            commit_msg=commit.title, pattern=PATTERN
        )
        title_checklist.append(check_commit)
        checked_commit_result = f"{check_commit} {commit.title}"
        checked_body_result = []
        if commit.body:
            for message in commit.body:
                check_body_message = commitizen.validate_commit_message(
                    commit_msg=message, pattern=PATTERN
                )
                if check_body_message:  # must not start with a conventional message
                    body_checklist.append(False)
                    checked_body_result.append(f"{check_body_message} {message}")
        display_commit_report(
            commit_hash=commit.hash[:6],
            message=checked_commit_result,
            body=checked_body_result,
        )
    if not display_check_result_report(
        title_checklist=title_checklist, body_checklist=body_checklist
    ):
        sys.exit(1)


def display_commit_report(commit_hash: str, message: str, body: List = None):
    space = "   "
    print(f"Commit: {commit_hash}")
    print("Message:")
    message = message.replace("True", EMOJI_CHECK).replace("False", EMOJI_CROSS)
    print(emoji.emojize(f"{space}{message}"))
    if len(body) > 0:
        print("Body:")
        for message in body:
            message = message.replace("True", EMOJI_CROSS)
            print(emoji.emojize(f"{space}{message}"))
    print("\n")


def display_check_result_report(title_checklist: List, body_checklist: List) -> bool:
    error_number = title_checklist.count(False) + body_checklist.count(False)
    has_error_in_title = (False in title_checklist)
    has_error_in_body = (False in body_checklist)

    if has_error_in_title or has_error_in_body:
        print(FAILED)
        print(f"Errors found : {error_number}")
        if has_error_in_title and not has_error_in_body:
            print(TITLE_FAILED)
        elif has_error_in_body and not has_error_in_title:
            print(BODY_FAILED)
        else:
            print(f"{TITLE_FAILED}\n{BODY_FAILED}")
        return False
    else:
        print(SUCCESS)
        return True
