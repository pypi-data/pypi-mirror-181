import argparse
import sys

from . import basketcase


def main():
    """Handle command-line script execution."""

    parser = argparse.ArgumentParser(description='Download images and videos from Instagram.')
    parser.add_argument(
        'input_file',
        type=argparse.FileType('r'),
        help='A list of URLs separated by newline characters'
    )
    parser.add_argument('-s', '--sessionid', help='The session cookie id')
    args = parser.parse_args()

    urls = set()

    for line in args.input_file:
        line = line.rstrip()

        if line:
            urls.add(line)
    
    bc = basketcase.BasketCase()

    if bc.authenticator.needs_authentication():
        if args.sessionid:
            bc.authenticator.login_with_cookie(args.sessionid)
        else:
            bc.authenticator.login()

    bc.fetch(urls)

    return 0


if __name__ == '__main__':
    sys.exit(main())
