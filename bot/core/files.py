import hashlib
import os
from typing import List

import aiofiles


class FileStorage:
    def __init__(self) -> None:
        self.files = {}

    def get(self, name: str) -> str:
        """
        Returns the path to the file.
        """
        if name not in self.files.keys():
            raise AttributeError(f"File {name} not found.")

        if isinstance(self.files[name], list):
            raise AttributeError(f"File {name} is a list. Use get_list().")

        return self.files[name]

    def get_list(self, name: str) -> List[str]:
        """
        Returns list of files.
        """
        if name not in self.files:
            raise AttributeError(f"File {name} not found.")

        if not isinstance(self.files[name], list):
            raise AttributeError(f"File {name} is not a list. Use get().")
        return self.files[name]

    async def save(self, name: str, data: bytes) -> None:
        """
        Saves the file to the filesystem.

        Nothing is returned.
        """
        data_hash = hashlib.sha256(data).hexdigest()
        filename = f"/tmp/{data_hash}"
        async with aiofiles.open(filename, "wb") as f:
            await f.write(data)

        self.files[name] = filename

    async def append(self, name: str, data: bytes) -> None:
        """
        Adds item to list of files.
        """
        data_hash = hashlib.sha256(data).hexdigest()
        filename = f"/tmp/{data_hash}"
        async with aiofiles.open(filename, "wb") as f:
            await f.write(data)

        if name not in self.files:
            self.files[name] = []
        self.files[name].append(filename)

    async def clear(self) -> None:
        """
        Clears all files from the filesystem.
        """
        for name in self.files:
            if isinstance(self.files[name], list):
                for filename in self.files[name]:
                    os.remove(
                        filename
                    )  # Supposedly it's only one call to the kernel and shouldn't be a problem.
            else:
                os.remove(self.files[name])  # ^^^^^
        self.files = {}
