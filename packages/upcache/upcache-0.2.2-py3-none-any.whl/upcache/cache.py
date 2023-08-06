from typing import Optional, Iterable, Tuple
from threading import Lock

class Cache:
    """
    Thread-safe cache
    """
    def __init__(self) -> None:
        """
        Constructs an empty cache.
        """
        self._data = {}
        self._data_lock = Lock()

    def get(self, key: bytes) -> Optional[bytes]:
        """
        Retrieves a value for a given key.

        :param key the key to search
        :returns associated value if found, None otherwise
        """
        with self._data_lock:
            return self._data.get(key)

    def set(self, key: bytes, value: bytes) -> None:
        """
        Assigns a value to a key.

        :param key the key
        :param value the associated value
        """
        with self._data_lock:
            self._data[key] = value

    def decrement(self, key: bytes) -> bytes:
        """
        Decrements a value associated with a key.
        If the value is not an integer, a value of -1 is assigned.

        :param key the key
        :returns decremented value
        """
        try:
            with self._data_lock:
                v = int(self._data.get(key, b'0').decode()) - 1
        except:
            v = -1
        v = str(v).encode()
        with self._data_lock:
            self._data[key] = v
        return v
    
    def increment(self, key: bytes) -> bytes:
        """
        Increments a value associated with a key.
        If the value is not an integer, a value of 1 is assigned.

        :param key the key
        :returns incremented value
        """
        try:
            with self._data_lock:
                v = int(self._data.get(key, b'0').decode()) + 1
        except:
            v = 1
        v = str(v).encode()
        with self._data_lock:
            self._data[key] = v
        return v

    def clear(self) -> None:
        """
        Clears all keys from the cache.
        """
        with self._data_lock:
            self._data = {}

    def drop(self, key: bytes) -> bool:
        """
        Drops a key from the cache.

        :param key the key
        :returns True if the key was dropped,
                 False if the key does not exist
        """
        with self._data_lock:
            if key in self._data:
                self._data.pop(key)
                return True
            else:
                return False

    def exists(self, key: bytes) -> bool:
        """
        Determines if a key exists within the
        cache.

        :param key the key
        :returns True if key exists in cache
        """
        with self._data_lock:
            return key in self._data

    def count(self) -> int:
        """
        Returns the total number of keys
        in the cache.

        :returns number of keys
        """
        with self._data_lock:
            return len(self._data)

    def keys(self) -> Iterable[bytes]:
        """
        Returns a generator of keys.

        :returns iterable generator of keys
        """
        with self._data_lock:
            keys = list(self._data.keys())
        yield from keys

    def items(self) -> Iterable[Tuple[bytes, bytes]]:
        """
        Returns a generator of key-value pairs.

        :returns iterable generator of tuples representing
                 keys and associated values
        """
        with self._data_lock:
            _data = self._data.copy()
        for key, value in _data.items():
            yield key, value
