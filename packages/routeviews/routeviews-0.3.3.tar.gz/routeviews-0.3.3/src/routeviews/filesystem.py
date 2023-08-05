import glob
import os
import pathlib
import textwrap
from datetime import datetime, timedelta

import humanize


def list_dir(path: str, sort_key=os.path.getctime, reverse: bool = True):
    """List contents of a directory.

    Default behavior sorts the returned list so the newest file is first. 

    Args:
        path (str): The directory to list contents of.
        sort_key (optional): Function used as "key" in call to sorted over 
        the returned list of file names. Defaults to os.path.getctime.
        reverse (bool, optional): Reverse the sort. Defaults to True.

    Returns:
        List[str]: List of files at "path".
    """
    files = glob.glob(f'{path}/*')
    if sort_key:
        return sorted(files, key=sort_key, reverse=reverse)
    else:
        return files


def latest_file(path: str, glob_pattern: str = '*'):
    """Which file was most recently changed at "{path}/"

    > NOTE: Calculated using `os.path.getctime`

    Args:
        path (str): Path to some directory.
        glob_pattern (str): Which files to include when searching for latest. 
            Default '*'

    Returns:
        str: The file (or directory) that was most recently changed.
    """
    files = glob.glob(f'{path}/{glob_pattern}')
    if len(files) == 0:
        raise OSError(f'No files/directories matching "{glob_pattern}" found at "{path}"')
    return max(files, key=os.path.getctime)


def mkdirs(*paths) -> str:
    """Ensure some directory exists.

    Returns:
        str: The path of the directory created.

    Example:

    >>> mkdirs('/tmp', 'tinker', 'folder')
    '/tmp/tinker/folder'
    """
    dir_path = os.path.join(*paths)
    try: 
        os.makedirs(dir_path)
    except FileExistsError:
        pass
    return dir_path


def mkdirs_for_file(*paths):
    return mkdirs(*paths[:len(paths)-1])


def touchfile(*paths):
    """Ensure some file exists, and touch it.

    Returns:
        str: The name of the file.

    Example:

    >>> touchfile('/tmp', 'tinker', 'test.md')
    '/tmp/tinker/test.md'
    """
    dir = mkdirs_for_file(*paths)
    filepath = os.path.join(dir, paths[-1])
    pathlib.Path(filepath).touch()
    return filepath


def readfile(path: str) -> str:
    return pathlib.Path(path).read_text()


def writefile(*file_path: str, text: str) -> str:
    mkdirs_for_file(*file_path)
    pathlib.Path(*file_path).write_text(text)
    return os.path.join(*file_path)


class FileMetrics:
    def __init__(self, path):
        """Collect some useful metrics for a file.

        Args:
            path (str): The file to get metrics on.
        """
        self.path = path
        self.last_updated = os.path.getctime(path)
        self.size = os.path.getsize(path)
        self.bz2 = path.endswith('.bz2')

    def age_in_minutes(self) -> int:
        return int(self.age_in_seconds()) // 60

    def age_in_seconds(self) -> float:
        return self.age().total_seconds()

    def age(self) -> timedelta:
        file_datetime = datetime.fromtimestamp(self.last_updated)
        return datetime.now() - file_datetime

    def pprint(self) -> str:
        return textwrap.dedent(f'''
            file: {self.path}
            age: {humanize.naturaldelta(self.age())} old
            size: {humanize.naturalsize(self.size)}
            bzip2: {self.bz2}
            ''').strip()
