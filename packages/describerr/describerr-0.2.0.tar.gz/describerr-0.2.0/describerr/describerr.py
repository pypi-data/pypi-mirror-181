import io
import re
import shlex
import subprocess
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Union

from loguru import logger


@dataclass
class Commits:
    generic: Dict = field(default_factory=lambda: defaultdict(list))
    breaking: Dict = field(default_factory=lambda: defaultdict(list))


@dataclass
class Commit:
    raw: str
    prefix: str = None
    scope: str = None
    topic: str = None
    author: str = None
    breaking: bool = False


commits = Dict[str, List[Commit]]
OptionalCommit = Union[None, Commit]


def _breaking_changes(func):
    def inner(f, commits_dict):
        if commits_dict:
            f.write("\n---\n")
            f.write("### BREAKING CHANGES\n")
            func(f, commits_dict)
            f.write("---\n")

    return inner


class Describerr:
    """
    Simple Opinionated git log to a changelog.

    Dump `git log` to a file that is always a `CHANGELOG.md`. Commits are split into following areas:
    * feat - added features
    * chore - changes in existing features
    * fix - fixed bugs
    * docs - changes in documentation (README, docstrings)
    * refactor - code refactoring
    * test - testing code
    * ci - CI and CD related code like gitlab/github yaml files
    * revert - commit reverting merged changes
    * proj - project configuration and setup
    * other - commits that could not be parsed using previously mentioned keys

    Commit format that is properly parsed:

        prefix[(scope)][!]: topic

    where `(scope)` and `!`are optional and `!` means breaking change. More info on proper commit message format:
    https://www.conventionalcommits.org/en/v1.0.0/

    Commits with `release` prefix or starting with "Merge" word are **ignored**!
    """

    _PREFIXES_USE = {
        "feat": "Features",
        "chore": "Chore",
        "fix": "Fixes",
        "revert": "Reverts",
        "docs": "Documentation",
        "refactor": "Refactoring",
        "test": "Tests",
        "ci": "CI/CD",
        "proj": "Project configuration",
        "other": "Other changes",
    }
    _IGNORE_REGEXPS = (
        r".*Create release.*",
        r"Merge.*",
    )
    _CHANGELOG_FILE = "CHANGELOG.md"
    _PREFIX = rf"(?P<prefix>{'|'.join(_PREFIXES_USE.keys())})?"
    _SCOPE = r"\(?(?P<scope>[\w\s]+)?\)?"
    _BREAKING = r"(?P<breaking>\!)?"
    _TOPIC = r"(?P<topic>.*)"
    _AUTHOR = r".*\<(?P<author>.*)\>$"
    _COMMIT_REGEXP = rf"{_PREFIX}{_SCOPE}{_BREAKING}:\s*{_TOPIC}\s+\<"
    _SKIP_WORDS = (
        "release",
        "merge",
    )

    def __init__(self) -> None:
        self._commits = Commits()

    def parse_commits_into_obj(self, from_tag: str, to_tag: str) -> None:
        """
        Parse output from `git log` cmd to dictionary (k->prefix, v->List[Commit])

        :param from_tag: Annotated tag for the start of history. Use `""` for history from beginning to `to_tag`
        :param to_tag: Annotated tag for the end of history. Use `HEAD` for history till now
        :return: None
        """
        for commit_raw_str in self._get_commit_list(from_tag, to_tag):
            if re.match("|".join(self._IGNORE_REGEXPS), commit_raw_str):
                logger.debug(f"Skipping ignored commit: {commit_raw_str}")
                continue
            commit_obj = self._commit2obj(commit_raw_str)
            if commit_obj is None:
                continue
            if commit_obj.breaking:
                self._commits.breaking[commit_obj.prefix].append(commit_obj)
            else:
                self._commits.generic[commit_obj.prefix].append(commit_obj)

    def _commit2obj(self, commit_raw_str: str) -> OptionalCommit:
        """
        Parse single commit into a `Commit` object.

        If commit can't be parsed will be treated as 'other'.

        :param commit_raw_str: String containing single line from git log output
        :return: `Commit` object
        """
        if commit_raw_str.lower().startswith(Describerr._SKIP_WORDS):
            return
        match_obj = re.match(self._COMMIT_REGEXP, commit_raw_str)
        commit = Commit(raw=commit_raw_str, prefix="other")
        if match_obj:
            commit.prefix = match_obj.group("prefix") or "other"
            commit.scope = match_obj.group("scope")
            commit.topic = self._get_topic(match_obj)
            commit.breaking = match_obj.group("breaking") is not None
        match_author = re.match(self._AUTHOR, commit_raw_str)
        commit.author = match_author.group("author")  # author is always available
        # Set topic for unparsed commits = raw - author
        if not commit.topic:
            commit.topic = commit.raw.rsplit(f"<{commit.author}>", 1)[0].rstrip()
        logger.debug(commit)
        return commit

    def _get_topic(self, match_obj) -> str:
        topic = match_obj.group("topic").strip()
        topic = topic[0].capitalize() + topic[1:]
        return topic

    def create_changelog(self, release: str) -> None:
        """
        Create CHANGELOG.md and add commits in structured way.

        :param release: Release name e.g v1.0.0
        :return: None
        """
        with open(self._CHANGELOG_FILE, "w") as f:
            self.__add_date_and_release(f, release)
            add_breaking_changes = _breaking_changes(self.__add_commits)
            add_breaking_changes(f, self._commits.breaking)
            self.__add_commits(f, self._commits.generic)
        logger.info(f"Changelog written to {self._CHANGELOG_FILE}")

    @staticmethod
    def _get_commit_list(from_tag: str, to_tag: str):
        """
        Get commits as list of subjects with authors.

        :param from_tag: Annotated tag for the start of history. Use `""` for history from beginning to `to_tag`
        :param to_tag: Annotated tag for the end of history. Use `HEAD` for history till now
        :return: Generator of commit strings from `git log` cmd
        """
        # %an - commit author
        # %s - commit topic
        log_range = f"{from_tag}..{to_tag}"
        if not from_tag:
            log_range = to_tag

        git_command = f'git log {log_range} --pretty="%s <%an>"'
        result = subprocess.run(shlex.split(git_command), capture_output=True)
        logger.info(f"Getting commits using command: {git_command}")
        result.check_returncode()
        stdout = result.stdout.decode().strip().split("\n")
        logger.debug(stdout)
        for commit_raw_str in stdout:
            yield commit_raw_str

    @staticmethod
    def __add_date_and_release(f: io.TextIOWrapper, release: str) -> None:
        """
        Add to changelog file header with release data.

        :param f: File handler to CHANGELOG.md file
        :param release: Release name e.g v1.0.0
        :return: None
        """
        f.write("# Changelog\n")
        f.write(f"## Release: {release} - {Describerr._get_current_date()}\n")

    @staticmethod
    def _get_current_date() -> str:
        return date.today().strftime("%d/%m/%Y")

    def __add_commits(self, f: io.TextIOWrapper, commits_dict: commits) -> None:
        """
        Add commits to changelog.

        :param f: File handler to CHANGELOG.md file
        :param commits_dict: Dictionary where Key is prefix type and value is list of Commits
        :return: None
        """
        if not commits_dict:
            return
        for prefix_type, prefix_name in self._PREFIXES_USE.items():
            if prefix_type not in commits_dict:
                continue
            f.write(f"### {prefix_name}:\n")
            Describerr._write_commits(f, commits_dict, prefix_type)

    @staticmethod
    def _write_commits(f, commits_dict: commits, prefix_type: str) -> None:
        """
        Write commit in one of formats: topic|raw_string (author).

        :param f: File handler to CHANGELOG.md file
        :param commits_dict: Dictionary where Key is prefix type and value is list of Commits
        :param prefix_type: Type of commit prefix e.g. fix, feat
        :return: None
        """
        for commit in commits_dict.get(prefix_type, []):
            text = "* "
            if commit.scope:
                text += f"**[{commit.scope}]** "
            text += f"{commit.topic} *({commit.author})*\n"
            f.write(text)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simple opinionated gitt log to a changelog")
    parser.add_argument("version", type=str, help="Current release name i.e. v1.2.3")
    parser.add_argument(
        "--from-tag",
        type=str,
        help="Take commits from this annotated tag or, by default, from start of history",
        default=None,
    )
    parser.add_argument(
        "--to-tag", type=str, help="Take commits to this annotated tag or, by default, to HEAD", default="HEAD"
    )

    args = parser.parse_args()

    describerr = Describerr()
    describerr.parse_commits_into_obj(args.from_tag, args.to_tag)
    describerr.create_changelog(args.version)
