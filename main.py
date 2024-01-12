import datetime
import os
import time
from typing import Generator, Iterator, List
from zipfile import ZipFile
from loguru import logger
from pathlib import Path
import os
import shutil
from tqdm import tqdm

# How many minutes in 30 days

HOUR = 3600
DAY = HOUR * 24

ROOT = os.path.dirname(os.path.realpath(__file__))

logger.add(os.path.join(ROOT, "LOG"), level="INFO", colorize=False, backtrace=True)


def remove(_path: Path) -> None:
    """deletes a file or path from the filesystem"""
    if _path.is_file():
        Path.unlink(_path)
    else:
        shutil.rmtree(_path)


def get_str_date(ts):
    """convenience for human readable dates from timestamps"""
    return datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def get_download_directory():
    """returns path of home directory"""
    return Path(os.path.join(Path.home(), "Downloads"))


def get_folder_items(_path: Path) -> List[Path]:
    """returns a list of files and folder from a directory"""
    root, folders, files = next(os.walk(_path))
    return [Path(os.path.join(Path(root, (x)))) for x in folders + files]


def is_archivable(_path: Path) -> bool:
    """return true if _path is archivable"""
    test = time.time() - (30 * DAY)
    actual = os.path.getmtime(_path)
    return test > actual


def main():
    """main point of execution"""
    logger.info("starting")
    archivable = [
        item
        for item in tqdm(get_folder_items(get_download_directory()))
        if is_archivable(item)
    ]

    with ZipFile("archive.zip", "w") as myzip:
        for _file in archivable:
            logger.info(f"writing {_file} to zip")
            myzip.write(_file)
            logger.info(f"deleting {_file} to zip")
            remove(_file)


if __name__ == "__main__":
    main()
