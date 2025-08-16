import argparse
import os

from lib.cal import load_cal
from lib.display import print_result


def pull_and_display(
    mode, urls_path, cache_path, cache_timeout, interval, no_skip=False
):
    cal = load_cal(urls_path, cache_path, cache_timeout, no_skip)
    print_result(mode, cal, interval, no_skip)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        prog="calparse", description="Parses iCal URLs in different ways."
    )
    argparser.add_argument("mode", nargs="?", help="supports 'random', 'list'")
    argparser.add_argument(
        "-u",
        "--urls",
        help="JSON file containing a list of iCal URLs (default: ./urls.json)",
        default=os.path.join(os.path.dirname(__file__), "urls.json"),
    )
    homedir = os.environ.get("HOME")
    argparser.add_argument(
        "-c",
        "--cache",
        help="cache file of calendar state (default $HOME/.cache/calparse-cache.json)",
        default=os.path.join(homedir, ".cache/calparse-cache.json"),
    )
    argparser.add_argument(
        "--cache_timeout",
        help="length of time the cache is good for (seconds, default: 3600)",
        default=3600,
    )
    argparser.add_argument(
        "-i",
        "--interval",
        help="number of seconds in an interval for the 'sequence' mode ",
        default=30,
    )
    argparser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="force update of the cache, overriding cache_timeout",
    )
    argparser.add_argument(
        "--version",
        action="store_true",
        help="print version information (latest git commit hash and date)",
    )
    argparser.add_argument(
        "-n",
        "--no-skip",
        action="store_true",
        help="do not skip any events despite not_until_days configuration",
    )
    args = argparser.parse_args()
    if args.version:
        import subprocess

        try:
            version = (
                subprocess.check_output(
                    ["git", "log", "-1", "--format=%H,%ad", "--date=iso"],
                    stderr=subprocess.DEVNULL,
                )
                .decode()
                .strip()
            )
            print(version)
        except Exception:
            print("Version info not available.")
        exit(0)
    if not args.mode:
        argparser.error("the following arguments are required: mode")
    cache_timeout = 0 if args.force else args.cache_timeout
    pull_and_display(
        args.mode.lower(),
        args.urls,
        args.cache,
        cache_timeout,
        args.interval,
        args.no_skip,
    )
