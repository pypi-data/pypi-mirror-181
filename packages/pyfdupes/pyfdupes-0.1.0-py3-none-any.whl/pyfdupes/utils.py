import sys
from pathlib import Path
from typing import Any, List, Optional
from colorama import Fore, Style


def is_in_folder(file: Path, folders: Optional[List[Path]]) -> bool:
    """
    Check if a file is contained by any given folder
    """
    return folders is not None and any(map(file.is_relative_to, folders))


def color_str(item: Any) -> str:
    """
    colorize item given its type
    """
    if not sys.stdout.isatty():
        return str(item)
    if isinstance(item, Path):
        if item.is_dir():
            return f"{Fore.BLUE}{Style.BRIGHT}{item}/{Style.RESET_ALL}"
        return f"{Style.BRIGHT}{Fore.BLUE}{item.parent}/{Fore.MAGENTA}{item.name}{Style.RESET_ALL}"
    if isinstance(item, BaseException):
        return f"{Fore.RED}{item}{Fore.RESET}"
    return str(item)
