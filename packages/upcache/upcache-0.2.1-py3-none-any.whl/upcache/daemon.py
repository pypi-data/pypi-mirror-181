import subprocess
import os
import sys

def start_server_daemon(json_file: str, auto_kill: bool) -> None:
    """
    Starts a new TCP server for hosting the cache server.

    :param json_file output JSON file (for connecting via ephemeral port)
    :param auto_kill shut down server when all clients are disconnected
    """
    server_py = os.path.join(os.path.dirname(__file__), "server.py")
    args = [sys.executable, server_py, json_file]
    if auto_kill: args.append('--auto-kill')
    subprocess.Popen(args, start_new_session=True)
