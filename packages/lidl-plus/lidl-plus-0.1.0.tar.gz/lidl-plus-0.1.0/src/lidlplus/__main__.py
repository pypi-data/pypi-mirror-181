#!/usr/bin/env python3
import argparse
from getpass import getpass

from api import LidlPlusApi


def get_arguments():
    """Get parsed arguments."""
    parser = argparse.ArgumentParser(description="Speedport: Command Line Utility")
    subparser = parser.add_subparsers(title="commands", metavar="command", required=True)
    auth = subparser.add_parser("auth", help="Authenticate and get refresh_token")
    auth.add_argument("auth", help="Authenticate and get refresh_token", action="store_true")
    return vars(parser.parse_args())


def print_refresh_token():
    username = input("Enter lidl plus username (usually a phone number): ")
    password = getpass("Enter lidl plus password: ")
    language = input("Enter language (DE, EN, ...): ")
    country = input("Enter country (de, at, ...): ")
    lidl_plus = LidlPlusApi(language, country)
    lidl_plus.login(username, password, lambda: input("Enter verify code: "))
    length = len(token := lidl_plus.refresh_token) - len("refresh token")
    print(f"{'-' * (length // 2)} refresh token {'-' * (length // 2 - 1)}\n{token}\n{'-' * len(token)}")


def main():
    args = get_arguments()
    if args.get("auth"):
        print_refresh_token()


if __name__ == '__main__':
    main()
