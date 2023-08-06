"""
command line interface
"""

from argparse import ZERO_OR_MORE, ArgumentParser
from pathlib import Path

from . import __version__
from .fdupes import find_duplicates
from .utils import color_str, is_in_folder


def run():
    """
    entry point
    """
    parser = ArgumentParser(description="find and delete duplicate files")

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print more information",
    )
    group.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="print less information",
    )
    parser.add_argument(
        "--rm",
        action="store_true",
        help="delete duplicated files with no copy in keep folders",
    )
    parser.add_argument(
        "-1",
        "--keep-first",
        action="store_true",
        help="if multiple copies found in keep folders, keep only first copy",
    )
    parser.add_argument(
        "-k",
        "--keep",
        type=Path,
        metavar="DIR",
        action="append",
        help="folders containing files to keep",
    )
    parser.add_argument(
        "folders",
        type=Path,
        metavar="DIR",
        nargs=ZERO_OR_MORE,
        help="folders to analyze",
    )

    args = parser.parse_args()

    try:
        folders = list(args.folders)
        if args.keep is not None:
            folders += args.keep
        files_to_delete = []
        for duplicates in find_duplicates(folders, quiet=args.quiet):
            keep_files = [f for f in duplicates if is_in_folder(f, args.keep)]
            duplicated_files = [f for f in duplicates if f not in keep_files]
            assert len(keep_files) + len(duplicated_files) == len(duplicates)

            if len(keep_files) == 0:
                if args.verbose:
                    print("🔥 No duplicated file found in keep folders:")
                    for file in duplicated_files:
                        print(f"  {color_str(file)}")
            elif len(duplicated_files) == 0:
                if len(keep_files) > 1 and args.keep_first:
                    for file in keep_files[1:]:
                        print(
                            f"🗑 Delete {color_str(file)} duplicate of {color_str(keep_files[0])}"
                        )
                        files_to_delete.append(file)
                elif args.verbose:
                    print("🔐 All duplicated files are in keep folders:")
                    for file in keep_files:
                        print(f"  {color_str(file)}")
            else:
                files_to_delete += duplicated_files
                for file in duplicated_files:
                    print(
                        f"🗑 Delete {color_str(file)} duplicate of {color_str(keep_files[0])}"
                    )

        if len(files_to_delete) > 0 and args.rm:
            print(f"🚮 Remove {len(files_to_delete)} files")
            for file in files_to_delete:
                file.unlink()

    except KeyboardInterrupt:
        print("❌ Process interrupted")
        exit(1)
    except BaseException as error:  # pylint: disable=broad-except
        print(f"💥 Error: {error}")
        raise error
    exit(0)
