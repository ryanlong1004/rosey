"""cleans up Download directory folder on most OS's"""

# Importing necessary modules
import os
import time
from typing import List
from zipfile import ZipFile
from pathlib import Path
import shutil
from loguru import logger
from tqdm import tqdm
import click

# Constants for time calculation
HOUR = 3600
DAY = HOUR * 24

# Root directory of the script
ROOT = os.path.dirname(os.path.realpath(__file__))

# Default download directory
DOWNLOAD_DIRECTORY = Path(os.path.join(Path.home(), "Downloads"))

# Logging setup
logger.remove()
logger.add(
    os.path.join(DOWNLOAD_DIRECTORY, "LOG"),
    level="INFO",
    colorize=False,
    backtrace=True,
)


def remove(_path: Path) -> None:
    """Deletes a file or path from the filesystem."""
    if _path.is_file():
        Path.unlink(_path)
    else:
        shutil.rmtree(_path)


def get_folder_items(_path: Path) -> List[Path]:
    """Returns a list of files and folders from a directory."""
    root, folders, files = next(os.walk(_path))
    return [Path(os.path.join(Path(root, (x)))) for x in folders + files]


def is_archivable(_path: Path, age: int) -> bool:
    """Returns True if _path is archivable."""
    test = time.time() - (age * DAY)
    actual = os.path.getmtime(_path)
    return test > actual


@click.command()
@click.option("--age", default=30, help="Archive age in days.")
@click.option("--dryrun/--no-dryrun", default=False)
def archive(age, dryrun):
    """Archive items in the Download folder older than [AGE]. Defaults to 30 days."""
    logger.info("Starting archive process.")
    archivable = [
        item
        for item in get_folder_items(DOWNLOAD_DIRECTORY)
        if is_archivable(item, age)
    ]

    archive_path = os.path.join(DOWNLOAD_DIRECTORY, "archive.zip")
    with ZipFile(archive_path, "a") as myzip:
        for _file in tqdm(archivable):
            logger.info(f"Writing {_file} to zip.")
            if not dryrun:
                myzip.write(_file)
            logger.info(f"Deleting {_file}.")
            if not dryrun:
                remove(_file)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    archive()
