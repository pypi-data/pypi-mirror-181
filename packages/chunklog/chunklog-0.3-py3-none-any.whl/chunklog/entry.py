from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re
from rich.text import Text


@dataclass(frozen=True)
class Entry:
    """Represents the state of the change of a section in a certain file in a specific commit in the repository"""

    file: str
    repo: str
    commit: str
    author: str
    date: str
    text: str
    id: str
    message: str

    def __str__(self):
        return f"\nFile: {self.repo}/{self.file} \nCommit: {self.commit} \nAuthor: {self.author} \nDate: {self.date} \nCommit message: {self.message} \n\n{self.text}"

    def __rich__(self):
        return Text.assemble(
            ("\nFile: ", "bold magenta"),
            (self.repo + "/", "bold yellow"),
            (self.file, "yellow"),
            ("\nCommit: ", "bold magenta"),
            (self.commit, "yellow"),
            ("\nAuthor: ", "bold magenta"),
            (self.author, "yellow"),
            ("\nDate: ", "bold magenta"),
            (self.date, "yellow"),
            ("\nMessage: ", "bold magenta"),
            (self.message.split("\n", 1)[0], "yellow"),
            "\n",
        )

    @classmethod
    def _add_entry_info(cls, commit, filename, section_text, id, repo_folder):
        new_entry = Entry(
            filename,
            repo_folder,
            commit.hexsha,
            f"{commit.author} <{commit.author.email}>",
            f"{commit.committed_datetime}",
            section_text,
            id,
            commit.message,
        )
        return new_entry

    @classmethod
    def parse(
        cls, filename: str, file_text: str, commit, regex, repo_folder: str
    ) -> "list[Entry]":
        """Find sections in a file matching a regex and return a list of entry objects representing the sections found

        Parameters
        ----------
        filename : `str`
            The name of the file to be analysed
        file_text : `str`
            String containing the content of the file
        commit : `Commit`
            Commit object from the GitPython library containing the information of a specific commit matching the state of the file_text
        regex : `str`
            String of the regular expression which matches the sections of which history will be added to the cache
        repo_folder: `str`
            String containing the name of the folder which the root of the repositiry resides in, i.e. the name of the repository

        Returns
        -------
        entries : `list` [`Entry`]
            A list of entry objects containing the sections in the file text which matched the given regular expression
        """
        entries = []
        # Check if regex is valid
        try:
            for match in re.finditer(
                regex,
                file_text,
                flags=re.DOTALL,
            ):
                req_id = match.group(1)
                entries.append(
                    Entry._add_entry_info(
                        commit, filename, match.group(0), req_id, repo_folder
                    )
                )
        except Exception as e:
            raise Exception("The provided regex is not valid, update config.ini")

        return entries
