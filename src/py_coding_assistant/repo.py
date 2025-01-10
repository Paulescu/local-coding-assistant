import random
from pathlib import Path
from typing import Optional

from gitingest import ingest


class Repo:
    def __init__(self, path: str):
        self.path = Path(path)

        if not self.path.exists():
            raise FileNotFoundError(f'The path {self.path} does not exist')

        self.files: dict[str, str] = self._load_files()

    def _load_files(self) -> dict[str, str]:
        """
        Loads all the py files in the repo into a dict with the full file path as the key
        and the file content as the value.
        """
        files = {}

        for file in self.path.glob('**/*.py'):
            files[str(file.relative_to(self.path))] = file.read_text()
        return files

    def stringify(self) -> str:
        """
        Returns a string representation of the repo.
        """
        # return "\n".join(self.files.values())
        summary, tree, content = ingest(str(self.path))

        return content

    @property
    def file_count(self) -> int:
        """Returns the number of files in the repo."""
        return len(self.files)

    @property
    def file_names(self) -> list[str]:
        """Returns the names of all the files in the repo."""
        return list(self.files.keys())

    def print_file(
        self,
        file_name: Optional[str] = None,
    ):
        """
        Prints a given file, either by name or by index.
        """
        if file_name not in self.files:
            raise FileNotFoundError(f'The file {file_name} is not in the repo')

        # print(f"#### File: {file_name} ####")
        print(self.files[file_name])

    def print_random_file(self):
        """
        Prints a random file from the repo.
        """
        random_file = random.choice(self.file_names)
        # print(f"#### File: {random_file} ####")
        self.print_file(random_file)
