from collections import namedtuple
from rich import print as rprint
from chunklog.console import console
from chunklog.colored_output import get_edits_string
from textwrap import indent
from more_itertools import pairwise
from pathlib import Path
from git.repo import Repo
from git import Commit
from chunklog.entry import Entry
import typer
from typing import Optional, List
from rich.progress import Progress, track

from chunklog.cache import Cache, StoreResult, CacheStatus
import time
from configparser import ConfigParser


def _check_path_in_directory(repo: Repo, dir_path: Path, path: str):
    subdirectory = str(dir_path)[len(str(repo.working_dir)) + 1 :]
    return True if subdirectory in path else False


def _get_changed_files_and_their_status(
    repo: Repo, dir_path: Path, commit1: Commit, commit2: Commit
):
    StatusAndPath = namedtuple("StatusAndPath", ["status", "path"])
    diff_strings = repo.git.diff(commit2.hexsha, commit1.hexsha, "--name-status").split(
        "\n"
    )
    # Example output from repo.git.diff:
    # D mypath.md
    # A mypath2.md
    return_values = []
    for diff_string in diff_strings:
        status = diff_string.split("\t")[0]
        path = diff_string.split("\t")[-1]
        if _check_path_in_directory(repo, dir_path, path):
            return_values.append(StatusAndPath(status, path))
    return return_values


def _get_entries_from_commit(
    repo: Repo, commit: Commit, file_path: str, regex: str, repo_folder: str
) -> "list[Entry]":
    try:
        file_text = str(
            repo.git.execute(["git", "show", f"{commit.hexsha}:{file_path}"])
        )
    except Exception as e:
        # Fatal bad object error resulting from trying to execute git show on a submodule
        # Ignore the error if it's a directory
        if not Path(file_path).is_file():
            return []
        raise Exception("Unexpected error when executing git show")  # pragma: no cover

    return Entry.parse(file_path, file_text, commit, regex, repo_folder)


class _Commit(object):
    def __init__(self, hexsha):
        self.hexsha = hexsha


def _entry_text_without_whitespace(entry: Entry):
    return entry.text.replace("\n", "").replace(" ", "")


def _remove_entries_only_updating_whitespace(entries: "list[Entry]") -> "list[Entry]":
    """Iterate through the entries from oldest to newest, and if an entry with
    a specific id only updates whitespace compared to the old entry with that id,
    remove it."""

    latest_text_without_whitespace_from_entry_id = {}
    new_entries = []

    # entries stores from newest to oldest, so reverse it
    for entry in reversed(entries):
        previous_entry_text = latest_text_without_whitespace_from_entry_id.get(
            entry.id, "MISSING"
        )
        # If the text has changed, keep the entry and update the
        # record of the latest text for that entry
        if _entry_text_without_whitespace(entry) != previous_entry_text:
            new_entries.append(entry)
            latest_text_without_whitespace_from_entry_id[
                entry.id
            ] = _entry_text_without_whitespace(entry)

    return list(reversed(new_entries))


def add_to_cache(repo, path, cache, regex):
    """Create or add to the cache of the history of sections

    Parameters
    ----------
    repo : `Repo`
        Repo object containing information on the repository containing the sections to be added to the cache
    path : `str`
        String of the path to the code containing the sections to be added to the cache
    cache : `Cache`
        Cache object which specifies the cache where the history of different sections is stored
    regex : `str`
        String of the regular expression which matches the sections of which history will be added to the cache
    """
    repo_folder = repo.working_tree_dir.split("/")[-1]
    entries = []
    all_commits = list(repo.iter_commits(paths=path))

    # Add the empty tree sha to the list of all commits
    EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
    empty_commit = _Commit(EMPTY_TREE_SHA)
    all_commits.append(empty_commit)

    commit_tuples = list(pairwise(all_commits))

    with Progress(transient=True) as progress:
        task = progress.add_task(
            "Going through commit history...",
            total=len(commit_tuples),
        )
        while not progress.finished:
            # ALL OTHER COMMITS - Go through all commits in directory pairwise and adds the requirement to the cache if it has changed since last commit.
            # Note: Looping through all kind of files, optimisation might be to only look though for specific file types
            for commit1, commit2 in commit_tuples:
                # If commit has been added to the cache we exit the for loop
                # Okay since we add to the cache in the end of this function
                # Thus if the process was ended mid run we will never have a partially filled cache
                if (
                    cache.check_commit_in_cache(commit1.hexsha)
                    == StoreResult.ALREADY_STORED
                ):
                    progress.remove_task(task)
                    break
                """
                # Outputs the list of files in the commit provided in the second argument to git diff
                diff = repo.git.diff(commit2.hexsha, commit1.hexsha, "--name-only")
                changed_paths = diff.splitlines()
                # If files outside the subdirectory were changed in the same commit they are also included
                # Remove them by calling check_subdirectory
                changed_paths = filter_include_only_files_in_subdirectory(
                    repo, path, changed_paths
                )
                """
                # This function solves the issue regarding removed files in merge. The status variable shows which files have been deleted.
                # Skip these since we don't care about files that do not exist.
                for return_value in _get_changed_files_and_their_status(
                    repo, path, commit1, commit2
                ):
                    status, file_path = return_value
                    if status == "D":
                        continue
                    entries.extend(
                        _get_entries_from_commit(
                            repo, commit1, file_path, regex, repo_folder
                        )
                    )
                progress.update(task, advance=1)

    entries = _remove_entries_only_updating_whitespace(entries)

    for entry in track(entries, description="Adding to cache..."):
        cache.store(entry)


def get_history(req_id, cache):
    """Retrieve the history of a specific section from the cache.

    Parameters
    ----------
    req_id : `str`
        String whose value should be a unique id of a section
    cache : `Cache`
        Cache object which specifies the cache where the history of different sections is stored

    Returns
    -------
    history : `list` [`Entry`]
        A list of Entry objects relating the history of the section specified by the req_id located in the given cache
    """
    # Retrieves the cached entries with the matching Requirement id
    if req_id == None:
        raise typer.BadParameter("Missing argument 'REQ_ID'")
    history = cache.get_cached_history(req_id)
    return history


def _get_regex_from_config_file(repo_path):
    config_file_path = Path(repo_path) / ".sectionHistory/config.ini"
    cfg = ConfigParser()

    # Check if configuration file exists
    if not config_file_path.is_file():
        raise Exception("config.ini does not exist in .sectionHistory directory")

    cfg.read(config_file_path)

    # Check if configuration file correctly formatted
    try:
        regex_val = cfg["regex_section"]["regex_val"]
    except KeyError as e:
        raise Exception("config.ini not formatted correctly")
    return regex_val


def parse_entry_output(entries, highlight_diff):
    """Display entries in console with different highlighting formatted

    Parameters
    ----------
    entries : `list` [`Entry`]
        A list of Entry objects relating the history of a specific section
    highlight_change : `boolean`
        A boolean value which if true the change in the text of the section will be highlighted
    """
    previous_entry = ""
    for entry in reversed(entries):
        # Meta data
        rprint(entry)

        # Text
        if highlight_diff:
            if previous_entry == "":
                print(indent(get_edits_string("", entry.text), "    "))
            else:
                print(indent(get_edits_string(previous_entry.text, entry.text), "    "))
        else:
            print(indent(entry.text, "    "))
        previous_entry = entry


def _format_entries(entries: "list[list[Entry]]"):
    combine_entries = []
    for entry_list in entries:
        combine_entries.extend(entry_list)
    combine_entries.sort(key=lambda r: r.date, reverse=True)
    return combine_entries


def _initiate_repo():
    # Get current working directory
    path = Path.cwd()
    # Initiates and check if repo
    try:
        repo = Repo(path, search_parent_directories=True)
    except Exception as e:
        if e.__class__.__name__ == "InvalidGitRepositoryError":
            raise Exception("Your current working directory is not a repository")
        raise Exception("Other path error")  # pragma: no cover
    return repo, path


def main(
    req_id: Optional[str] = typer.Argument(None),
    highlight_diff: bool = typer.Option(
        True, " /--no-diff", help="Markup of requirement changes in the output "
    ),
    update_cache: bool = typer.Option(False, help="Update the global cache"),
    cache_path: List[str] = typer.Option(
        [],
        help="Specify the path to cache directory, can take multiple values when retrieving the section history",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force update the cache. Must include the update-cache flag as well.",
    ),
):
    # Adds all the reqs in the directory specified to the cache
    if update_cache:
        repo, path = _initiate_repo()
        root_path = repo.working_tree_dir

        # Gets regex to identify a section. Specified in config file in root directory of target repo.
        regex = _get_regex_from_config_file(root_path)

        # Only allow the creation of cache in a single path location at a time
        if len(cache_path) > 1:
            raise Exception(
                "Cache generation can only be done for a single path at a time"
            )
        cache = Cache(cache_path[0]) if cache_path else Cache(root_path)
        # Force update cache, i.e. remove the cache and then add the entries anew
        if force:
            cache.remove_cache()
        add_to_cache(repo, path, cache, regex)
        print(f"Cache location: {cache.get_cache_dir()}")
    # Fetch the history for a given requirement id
    else:
        caches = []
        if cache_path:
            for cp in cache_path:
                caches.append(Cache(cp))
        else:
            # Initiate the cache in the current working directory if no path provided
            caches.append(Cache(Path.cwd()))
        if len(caches) == 1 and caches[0].check_cache_empty() == CacheStatus.EMPTY:
            create_cache = typer.confirm(
                f"Cache provided is empty.\nDo you want to create cache in {caches[0].get_cache_dir()}?",
                abort=True,
            )
            repo, path = _initiate_repo()
            root_path = repo.working_tree_dir
            regex = _get_regex_from_config_file(root_path)
            add_to_cache(repo, path, caches[0], regex)
        entries = []
        # Retrieve entries specified by the id in each of the provided cache paths
        for cache in caches:
            entries.append(get_history(req_id, cache))
        entries = _format_entries(entries)
        if type(entries) != str:
            parse_entry_output(entries, highlight_diff)
        if len(entries) == 0:
            print(
                "The provided regex and ID did not match any sections in the directory."
            )
        return entries


if __name__ == "__main__":
    typer.run(main)
