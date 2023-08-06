import sys
from pathlib import Path
from subprocess import DEVNULL, check_output
from typing import List, Tuple


def find_duplicates(folders: List[Path], quiet: bool = False) -> List[Tuple[Path]]:
    """
    Use fdupes to find supplicates files, and yield the list of files.
    Yielded files are sorted.
    """
    command = ["fdupes", "--recurse", "--noempty"]
    if quiet:
        command.append("--quiet")
    command += [str(f) for f in folders]

    print("Looking for duplicates ...")
    stdout = check_output(
        command, text=True, stderr=sys.stderr if not quiet else DEVNULL
    )

    out = []
    files = []
    for line in stdout.splitlines():
        if len(line) == 0:
            assert len(files) > 1
            out.append(tuple(sorted(files)))
            files = []
        else:
            file = Path(line)
            assert file.is_file()
            files.append(file)
    assert len(files) == 0
    return out
