from datetime import datetime
from chunklog.entry import Entry
from pathlib import Path
import glob
import json
from enum import Enum
import shutil
import argparse
from dataclasses import dataclass, asdict


class StoreResult(Enum):
    """Enumeration value indicating whether or not a commit has been stored in cache"""

    ALREADY_STORED = 1
    NOT_STORED = 2


class CacheStatus(Enum):
    """Enumeration value indicating whether or not the cache is empty"""

    EMPTY = 1
    NON_EMPTY = 2


class Cache:
    """An instantiation of a cache storing the history of sections,
    created in a subdirectory in the root of a given repository
    """

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        configs_dir = Path(repo_path) / ".sectionHistory"
        if not configs_dir.is_dir():
            configs_dir.mkdir()
        self.cache_dir = configs_dir / "cache"

    def store(self, entry: Entry):
        """Store an entry in the cache, representing the change that occured to a section

        Parameters
        ----------
        entry: `Entry`
            The Entry object to be stored in the cache
        """
        # Create dir for cachedReqs if it does not exist - user should add .sectionHistory to the gitignore files
        self.cache_dir.mkdir() if not self.cache_dir.is_dir() else False

        reqid_dir = self.cache_dir / f"{entry.id}"
        # Create a directory for the req if we do not find it
        reqid_dir.mkdir() if not reqid_dir.is_dir() else False

        # Add the commit (i.e. the entry) to the dir -> name is the commit hash
        new_file = reqid_dir / f"{entry.commit}.json"

        entry_dictionary = {"entry": asdict(entry)}

        with new_file.open("w") as f:
            json.dump(entry_dictionary, f, default=str)

    def get_cached_history(self, section_id: str) -> "list[Entry]":
        """Returns the history of a specific section ordered by timestamp of commit in reverse order

        Parameters
        ----------
        section_id : `str`
            The ID of the section which history will be fetched

        Returns
        -------
        section_history : `list` [`Entry`]
            A list of Entry objects representing the history of the section matching the given ID
        """
        section_path = self.cache_dir / f"{section_id}/*.json"
        section_history = []
        for file in glob.glob(str(section_path)):
            f = open(file)
            data = json.load(f)

            section_entry = Entry(
                data["entry"]["file"],
                data["entry"]["repo"],
                data["entry"]["commit"],
                data["entry"]["author"],
                data["entry"]["date"],
                data["entry"]["text"],
                data["entry"]["id"],
                data["entry"]["message"],
            )
            section_history.append(section_entry)
            f.close()
        section_history.sort(key=lambda r: r.date, reverse=True)
        return section_history

    def remove_cache(self):
        """Delete the cache and all its content"""
        shutil.rmtree(self.cache_dir) if self.cache_dir.is_dir() else False
        return self.cache_dir

    def check_commit_in_cache(self, commit):
        """Check if a certain commit is present in the cache

        Parameters
        ----------
        commit : `str`
            String of the hexsha value identifying the commit

        Returns
        -------
        StoreResult : `Enum`
            An enumeration value returning 1 (ALREADY_STORED) if it is located in the cache
            or 2 (NOT_STORED) if it has not been added to the cache
        """
        paths = sorted(self.cache_dir.rglob(f"{commit}.json"))
        if len(paths) > 0:
            return StoreResult.ALREADY_STORED
        else:
            return StoreResult.NOT_STORED

    def check_cache_empty(self):
        """Check if cache is empty

        Returns
        ------
        CacheStatus : `Enum``
            An enumeration value returning 1 (EMPTY) if cache is empty but 2 (NON_EMPTY) otherwise
        """
        return (
            CacheStatus.EMPTY
            if not self.cache_dir.is_dir() or not any(Path(self.cache_dir).iterdir())
            else CacheStatus.NON_EMPTY
        )

    def get_cache_dir(self):
        return self.cache_dir


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove cache")
    parser.add_argument("--remove-cache", action="store_true", help="Remove cache")
    args = parser.parse_args()
    if args.remove_cache:
        Cache.remove_cache()
