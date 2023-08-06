"""
Generate a random hostname based on a wordlist
"""

import argparse
import logging
import random
import os
import sys
from genhost.__init__ import __version__


def setup_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "integer",
        metavar="N",
        type=int,
        nargs="?",
        help="The number of hostnames to commission",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List all the commissioned hostnames",
    )
    parser.add_argument(
        "-r",
        "--reuse",
        help="Decommission hostname(s) and return them to the pool of available hostnames",
    )
    parser.add_argument(
        "-w",
        "--wordlist",
        help="""Location of wordlist to use. Only needed if you want to use a wordlist
                that isn't in the default location""",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="Display version number",
    )
    return parser


def main() -> None:
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.WARNING)
    parser = setup_arguments()
    args = parser.parse_args()

    logging.debug(args)

    if args.wordlist:
        wordlist_path = args.wordlist
    elif os.environ.get("HOME"):
        wordlist_path = (
            os.environ.get("HOME") + "/.config/genhost/wordlist.txt"  # type: ignore
        )
    else:
        logging.fatal(
            "No wordlist was specified and it wasn't possible to retrieve"
            "default location for wordlist. Please specify a wordlist manually."
        )
        sys.exit()

    if args.version:
        display_version()
    if args.reuse:
        decommission_hostname(wordlist_path, args.reuse)
    elif args.list:
        list_hostnames(wordlist_path)
    elif args.integer:
        commission_hostname(wordlist_path, args.integer)


def commission_hostname(wordlist_path: str, number_of_hosts: int) -> None:
    words = read_wordlist(wordlist_path)

    for _ in range(number_of_hosts):
        selected_word = random.choice(words)  # nosec

        while selected_word.startswith("#"):
            selected_word = random.choice(words)  # nosec

        print(selected_word.strip())

        try:
            index = words.index(selected_word)
            words[index] = "#" + selected_word
        except ValueError:
            logging.fatal(
                "Randomly selected the word, %s, but it doesn't exist in the word list.",
                selected_word,
            )
            return

        write_wordlist(wordlist_path, words)


def decommission_hostname(wordlist_path: str, hostname: str) -> None:
    words = read_wordlist(wordlist_path)

    try:
        index = words.index("#" + hostname + "\n")
        words[index] = hostname + "\n"
        write_wordlist(wordlist_path, words)
        print(f"The hostname, {hostname}, has been decommissioned")
    except ValueError:
        logging.error("The hostname, %s, is not currently commissioned.", hostname)


def write_wordlist(wordlist_path: str, words: list[str]) -> None:
    with open(wordlist_path, "w", encoding="utf_8") as f:
        f.writelines(words)


def read_wordlist(wordlist_path: str) -> list[str]:
    with open(wordlist_path, "r", encoding="utf_8") as f:
        words = f.readlines()

        return words


def list_hostnames(wordlist_path: str) -> None:
    words = read_wordlist(wordlist_path)

    for word in words:
        if word.startswith("#"):
            print(word.strip("#\n"))


def display_version() -> None:
    print(__version__)
