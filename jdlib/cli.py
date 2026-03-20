import argparse

from jdlib import __version__


def main():
    parser = argparse.ArgumentParser(prog='jdcli')
    parser.add_argument('--version', action='version', version=f'{__version__}')
    parser.parse_args()


if __name__ == '__main__':
    main()
