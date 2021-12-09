from contextlib import suppress
from io import BytesIO
from itertools import chain
from json import loads, dumps
from pathlib import Path
from sys import argv
from tarfile import open as tar_open, TarFile, TarInfo
from time import time
from typing import Any, Generator, Iterable, Optional, Union


# extract the responses as parsed JSON
def extract_responses(filepath: str) -> Generator[Any, None, None]:
    with open(filepath, "r") as file:
        for line in file:
            # Skip anything that's not a response line
            if "getitemdetailresponse" not in line:
                continue
            # Drop the \n and )]}'" suffix (if present)
            line = line.removesuffix("\n").removesuffix(")]}'")
            # Parse the JSON, bail if we get an IndexError
            yield loads(line)


# Safely traverse the keys in an objects returning Any
def traverse(data: Any, *keys: Union[str, int]) -> Optional[Any]:
    try:
        for key in keys:
            data = data[key]
        return data
    except IndexError:
        return None


# Add a file from memory to a tarball
def addfile(tar: TarFile, filename: str, contents: str):
    with BytesIO(contents.encode("utf-8")) as buf:
        info: TarInfo = TarInfo(filename)
        info.size = buf.getbuffer().nbytes
        info.mtime = time()
        tar.addfile(info, buf)


if __name__ == "__main__":
    # Extract the responses from each details file iteratively
    paths: Iterable[Path] = Path.cwd().glob("*.details.json")
    responses: Iterable[Any] = chain.from_iterable(
        (extract_responses(path) for path in paths)
    )
    # Open each of the output tarballs
    with tar_open(f"manifests-{argv[1]}.tgz", "w:gz") as manifests, tar_open(
        f"details-{argv[1]}.tgz", "w:gz"
    ) as details:
        for response in responses:
            data = response[1][1]
            filename: str = f"{data[0][0]}.json"
            with suppress(IndexError):
                addfile(manifests, filename, traverse(data, 9, 0))
            with suppress(IndexError):
                addfile(
                    details,
                    filename,
                    dumps(
                        {
                            "name": traverse(data, 0, 1),
                            "summary": traverse(data, 0, 6),
                            "description": traverse(data, 1, 1),
                            "category": traverse(data, 0, 10),
                            "rating": traverse(data, 0, 12),
                            "reviews": traverse(data, 0, 22),
                            "users": traverse(data, 0, 23),
                            "version": traverse(data, 6),
                            "updated": traverse(data, 7),
                            "size": traverse(data, 25),
                        }
                    ),
                    indent=2,
                )
