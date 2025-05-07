import mmap
from typing import Union

KEY_SIZE = 16
VAL_SIZE = 64
ENTRY_SIZE = KEY_SIZE + VAL_SIZE
MAX_ENTRIES = 1024  # Can hold 1024 key-value pairs

class MemoryKVStore:
    def __init__(self):
        self.size = ENTRY_SIZE * MAX_ENTRIES
        self.mmap = mmap.mmap(-1, self.size)
        self.view = memoryview(self.mmap)

    def _find_key_index(self, key: str) -> int:
        kbytes = key.encode('utf-8').ljust(KEY_SIZE, b'\x00')
        for i in range(MAX_ENTRIES):
            offset = i * ENTRY_SIZE
            if self.view[offset:offset + KEY_SIZE] == kbytes:
                return i
        return -1

    def set(self, key: str, value: bytes):
        if len(key) > KEY_SIZE:
            raise ValueError("Key too long")
        if len(value) > VAL_SIZE:
            raise ValueError("Value too long")

        idx = self._find_key_index(key)
        if idx == -1:
            # Find first empty slot
            for i in range(MAX_ENTRIES):
                offset = i * ENTRY_SIZE
                if self.view[offset:offset + KEY_SIZE].tobytes().strip(b'\x00') == b'':
                    idx = i
                    break
            if idx == -1:
                raise MemoryError("Store full")

        # Write key
        offset = idx * ENTRY_SIZE
        self.view[offset:offset + KEY_SIZE] = key.encode('utf-8').ljust(KEY_SIZE, b'\x00')
        self.view[offset + KEY_SIZE:offset + ENTRY_SIZE] = value.ljust(VAL_SIZE, b'\x00')

    def get(self, key: str) -> Union[bytes, None]:
        idx = self._find_key_index(key)
        if idx == -1:
            return None
        offset = idx * ENTRY_SIZE + KEY_SIZE
        return self.view[offset:offset + VAL_SIZE].tobytes().rstrip(b'\x00')

    def delete(self, key: str):
        idx = self._find_key_index(key)
        if idx == -1:
            return
        offset = idx * ENTRY_SIZE
        self.view[offset:offset + ENTRY_SIZE] = b'\x00' * ENTRY_SIZE