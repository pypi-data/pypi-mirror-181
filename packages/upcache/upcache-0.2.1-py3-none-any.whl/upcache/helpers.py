from .internal.errors import InvalidNameLengthError, InvalidNameError, CacheServerConnectionError
from .internal.tcp import Client
from .daemon import start_server_daemon

from typing import Optional
import os
import json
import tempfile
import string
import time

def _validate_name(name: str) -> None:
    """
    Validates a cache name for use within a filename.
    Raises InvalidNameLengthError or InvalidNameError
    upon failure.

    :param name cache name to validate
    """
    if len(name) < 1 or len(name) > 128:
        raise InvalidNameLengthError()

    valid_chars = string.ascii_letters + string.digits + '-_'
    for ch in name:
        if ch not in valid_chars:
            raise InvalidNameError(ch)

def _open_client(filename: str) -> Client:
    """
    Opens a JSON file for cache server connection
    info and returns a cache client object.

    :param filename JSON file containing cache server port
    :returns cache client object
    """
    with open(filename, 'r') as fd:
        data = json.loads(fd.read())
        return Client('127.0.0.1', data['port'])

def create_cache_client(filename: str, wait_for_file: bool = True) -> Client:
    """
    Creates a cache client and optionally waits for
    the JSON file to be populated with connection info.

    :param filename JSON file containing cache server port
    :param wait_for_file when True, polls the file 250ms intervals
                         for a total of 2.5 seconds (10 polls) until
                         raising a CacheServerConnectionError
    :returns cache client object upon successful connection
    """
    num_retries = 10
    if wait_for_file:
        while True:
            try:
                return _open_client(filename)
            except json.JSONDecodeError:
                # Wait a little longer for the JSON file to be populated
                if num_retries == 0:
                    try:
                        st = os.stat(filename)
                        if st.st_size == 0:
                            os.unlink(filename)
                    except:
                        pass
                    # We got a non-empty JSON file that makes no sense to us
                    raise CacheServerConnectionError()
                time.sleep(0.25)
                num_retries -= 1
            except ConnectionRefusedError as e:
                # JSON file is legit, but left over from a previous UpCache instance...
                try:
                    os.unlink(filename)
                    create_cache_server(filename, True)
                    num_retries = 10
                except:
                    # Windows will throw if we try to unlink, but we have to work around it
                    raise e
    else:
        # Don't wait for the JSON file, just open
        return _open_client(filename)

def create_cache_server(filename: str, auto_kill: bool) -> None:
    """
    Creates a new cache server with a JSON file containing connection info.
    If the file exists, a file permission error is raised.

    The process spawned is not associated with any Python processes to keep
    it available and detached from any one worker process.

    :param filename output JSON connection info file
    :param auto_kill kill the server when all clients disconnect
    """
    # Create file as a barrier for multiple servers
    fd = os.open(filename, os.O_CREAT | os.O_EXCL | os.O_TRUNC | os.O_WRONLY, mode=0o644)
    os.close(fd)

    start_server_daemon(filename, auto_kill)

def UpCache(name: str, path: Optional[str] = None, auto_kill: bool = True) -> Client:
    """
    Creates a new UpCache client and optionally creates a new server.

    :param name cache name
    :param path cache JSON file output path
    :param auto_kill kill the cache server when all clients disconnect
    :returns new TCP-based Client for the associated UpCache server
    """
    _validate_name(name)
    filename = os.path.join(path or tempfile.gettempdir(), f'upcache-{name}.json')
    try:
        create_cache_server(filename, auto_kill)
    except:
        pass
    return create_cache_client(filename, wait_for_file=True)
