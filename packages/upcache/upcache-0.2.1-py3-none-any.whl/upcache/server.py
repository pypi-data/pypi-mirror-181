from internal.tcp import run_cache_server
from argparse import ArgumentParser
import sys

def _get_arg_parser() -> ArgumentParser:
    """
    Creates a basic argument parser to accept a socket file path and an auto-kill flag argument.

    :returns argument parser
    """
    argp = ArgumentParser()
    argp.add_argument('socket_file', type=str, help='output socket connection file')
    argp.add_argument('--auto-kill', action='store_true', default=False)
    return argp

if __name__ == '__main__':
    args = _get_arg_parser().parse_args()
    run_cache_server(args.socket_file, True, args.auto_kill)
