import os
import lib_compute.typon_math as typon_math
import threading

# implement threadable [queue] [hmap] [vec]

# API:
# size: () -> int
# push: (V) -> bool
# poll: () -> V
class threadable_queue():

    def __init__(self):
        self.mutex = threading.Lock()
        self.in_buf = []
        self.out_buf = []

    def size(self):
        with self.mutex:
            return len(self.in_buf) + len(self.out_buf)

    def push(self, value):
        with self.mutex:
            self.out_buf.append(value)
            return True

    def poll(self):
        with self.mutex:
            if len(self.in_buf) == 0:
                while len(self.out_buf) > 0:
                    self.in_buf.append( self.out_buf.pop() )
                if len(self.in_buf) == 0:
                    return None
            return self.in_buf.pop()

# API:
# size: () -> int
# get: (K) -> V
# set: (K, V) -> bool
# remove: (K) -> bool
# keys: () -> list[K]
class threadable_hmap():

    def __init__(self):
        self.mutex = threading.Lock()
        self.data_map = {}

    def size(self):
        with self.mutex:
            return len(self.data_map)

    def get(self, key):
        with self.mutex:
            if key not in self.data_map:
                return None
            return self.data_map[key]

    def set(self, key, value):
        with self.mutex:
            self.data_map[key] = value
            return True

    def remove(self, key):
        with self.mutex:
            if key not in self.data_map:
                return False
            del self.data_map[key]
            return True

    def keys(self):
        with self.mutex:
            return [ x for x in self.data_map ]

# API:
# size: () -> int
# get: (int) -> V
# set: (int, V) -> bool
# remove: (int) -> bool
# keys: () -> list[V]
class threadable_vec():

    def __init__(self):
        self.mutex = threading.Lock()
        self.data_map = []

    def size(self):
        with self.mutex:
            return len(self.data_map)

    def get(self, key):
        with self.mutex:
            if key >= len(self.data_map) or key < 0:
                return None
            return self.data_map[key]

    def set(self, key, value):
        with self.mutex:
            if key >= len(self.data_map) or key < 0:
                return None
            self.data_map[key] = value
            return True

    def remove(self, key):
        with self.mutex:
            if key >= len(self.data_map) or key < 0:
                return None
            self.data_map[key] = None
            return True

    def keys(self):
        with self.mutex:
            return [ x for x in self.data_map ]
