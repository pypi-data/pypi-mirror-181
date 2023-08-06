from typing import Optional, Iterable, Tuple, List, Callable, Dict, Any
from threading import Lock, Event
from datetime import datetime, timedelta

class Cache:
    """
    Thread-safe cache
    """
    def __init__(self, on_update: Callable[[bytes, Optional[bytes]], None]) -> None:
        """
        Constructs an empty cache.
        
        :param on_update update callback for key-value updates (1st arg is key, 2nd arg is value where None signifies deletion)
        """
        self._data : Dict[bytes, Any] = {}
        self._data_lock = Lock()
        self._last_key : Optional[bytes] = None
        self._key_event = Event()
        self._key_event.clear()
        self._stopped = False
        self._on_update = on_update

    def close(self) -> None:
        """
        Wakes any sleeping waiters.
        The service is terrible but the food is good.
        """
        self._stopped = True
        self._key_event.set()

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
            self._on_update(key, value)
            self._last_key = key
            self._key_event.set()

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
        value = str(v).encode()
        with self._data_lock:
            self._data[key] = value
            self._on_update(key, value)
            self._last_key = key
            self._key_event.set()
        return value
    
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
        value = str(v).encode()
        with self._data_lock:
            self._data[key] = value
            self._on_update(key, value)
            self._last_key = key
            self._key_event.set()
        return value

    def clear(self) -> None:
        """
        Clears all keys from the cache.
        """
        with self._data_lock:
            for k in self._data.keys():
                self._on_update(k, None)
            self._data = {}
            # NOTE: None indicates all keys were wiped
            self._last_key = None
            self._key_event.set()

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
                self._on_update(key, None)
                self._last_key = key
                self._key_event.set()
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
    
    def wait_for(self, key: bytes, value: Optional[bytes] = None, timeout: Optional[timedelta] = None) -> bool:
        """
        Waits for an event with a key.

        :param key the key
        :param value wait for associated value
        :param timeout optional timeout
        :returns True if an event for the key fired,
                 False if the cache is closed
        """
        self._key_event.clear()
        if timeout:
            timeout_time = datetime.now() + timeout
            while not self._stopped:
                now = datetime.now()
                if timeout_time < now or not self._key_event.wait((timeout_time - now).total_seconds()):
                    return False
                last_key = self._last_key
                self._key_event.clear()
                if last_key is None or (last_key == key and (value is None or self.get(last_key) == value)):
                    return True
        else:
            while not self._stopped:
                self._key_event.wait()
                last_key = self._last_key
                self._key_event.clear()
                if last_key is None or (last_key == key and (value is None or self.get(last_key) == value)):
                    return True
        return False

    def count(self) -> int:
        """
        Returns the total number of keys
        in the cache.

        :returns number of keys
        """
        with self._data_lock:
            return len(self._data)

    def keys(self) -> List[bytes]:
        """
        Returns a generator of keys.

        :returns iterable generator of keys
        """
        with self._data_lock:
            keys = list(self._data.keys())
        return keys

    def items(self) -> List[Tuple[bytes, bytes]]:
        """
        Returns a generator of key-value pairs.

        :returns iterable generator of tuples representing
                 keys and associated values
        """
        with self._data_lock:
            _data = self._data.copy()
        return list(_data.items())
