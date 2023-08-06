# prefix_closure(p) = min { s : s > p and s[:len(p)] != p }
# prefix_closure( b'\xff' * n ) = None
# isinstance( prefix, bytes ) = True

# algorithm:
# cur_byte in range( len(prefix)-1, -1, -1 )
# try: increment cur_byte => return result
# else: result.append( b'\x00' ); continue
def select_prefix_closure( prefix ):
    buf = bytearray()
    for i in range( len(prefix)-1, -1, -1 ):
        # regrouping operation
        # if prefix[i] == b'\xff':
        if prefix[i] == 255:
            buf.append(0)
            continue
        # increment cur_byte
        X = bytearray()
        X.append( prefix[i] + 1 )
        return prefix[0:i] + bytes(X) + bytes(buf)

    # case: prefix = b'\xff' * n
    return None

# implements range_iterator
class ldb_range_iter():

    def __init__( self, db_ref, start, stop, include_start, include_stop, include_key, include_value, reverse ):
        # self.db_ref = db_ref
        self.db_it = db_ref.RangeIter(
            key_from = start,
            key_to = stop,
            include_value = include_value,
            reverse = reverse
        )

        self.start = start
        self.stop = stop
        self.include_start = include_start
        self.include_stop = include_stop
        self.include_key = include_key
        self.include_value = include_value
        self.reverse = reverse

        self.cur_kv = []
        self.val_set = False
        self.iter_finish = False

    def has_next(self):
        if self.iter_finish:
            return False
        if self.val_set:
            return True

        # self.include_value == False
        if not self.include_value:
            while True:
                # [key_ba] = next(self.db_ref, None)
                X = next(self.db_it, None)
                if X == None:
                    self.iter_finish = True
                    return False

                key_bytes = bytes(X[0])
                # x and not y = x and (not y) => op( not ) > op( and )
                if key_bytes == self.start and not self.include_start:
                    continue
                if key_bytes == self.stop and not self.include_stop:
                    continue

                if not self.include_key:
                    self.cur_kv = []
                    self.val_set = True
                    return True

                self.cur_kv = [ key_bytes ]
                self.val_set = True
                return True

            return False

        # self.include_value == True
        while True:
            # [ key_ba, val_ba ] = next(self.db_ref, None)
            X = next(self.db_it, None)
            if X == None:
                self.iter_finish = True
                return False

            key_bytes = bytes(X[0])
            value_bytes = bytes(X[1])
            # x and not y = x and (not y) => op( not ) > op( and )
            if key_bytes == self.start and not self.include_start:
                continue
            if key_bytes == self.stop and not self.include_stop:
                continue

            if not self.include_key:
                self.cur_kv = [ value_bytes ]
                self.val_set = True
                return True

            self.cur_kv = [ key_bytes, value_bytes ]
            self.val_set = True
            return True

        return False

    def get_next(self):
        if not self.has_next():
            return None
        self.val_set = False
        return self.cur_kv

class ldb_prefix_iterator():

    def __init__( self, db_ref,  prefix, include_key, include_value, reverse  ):
        prefix_closure = select_prefix_closure( prefix )
        # self.db_ref = db_ref
        self.db_it = db_ref.RangeIter(
            key_from = prefix,
            key_to = prefix_closure,
            include_value = include_value,
            reverse = reverse
        )

        self.start = prefix
        self.stop = prefix_closure
        self.include_key = include_key
        self.include_value = include_value
        self.reverse = reverse

        self.cur_kv = []
        self.val_set = False
        self.iter_finish = False

    def has_next(self):
        if self.iter_finish:
            return False
        if self.val_set:
            return True

        # self.include_value == False
        if not self.include_value:
            while True:
                # [key_ba] = next(self.db_ref, None)
                X = next(self.db_it, None)
                if X == None:
                    self.iter_finish = True
                    return False

                key_bytes = bytes(X[0])
                if self.prefix != key_bytes[0:len(self.prefix)]:
                    continue

                if not self.include_key:
                    self.cur_kv = []
                    self.val_set = True
                    return True

                self.cur_kv = [ key_bytes ]
                self.val_set = True
                return True

            return False

        # self.include_value == True
        while True:
            # [ key_ba, val_ba ] = next(self.db_ref, None)
            X = next(self.db_it, None)
            if X == None:
                self.iter_finish = True
                return False

            key_bytes = bytes(X[0])
            value_bytes = bytes(X[1])

            if self.prefix != key_bytes[0:len(self.prefix)]:
                continue

            if not self.include_key:
                self.cur_kv = [ value_bytes ]
                self.val_set = True
                return True

            self.cur_kv = [ key_bytes, value_bytes ]
            self.val_set = True
            return True

        return False

    def get_next(self):
        if not self.has_next():
            return None
        self.val_set = False
        return self.cur_kv

# functional iterator for levelDB:
# include_(key|value), include_(start|stop), prefix, reverse
# two_iteration_types: (range, prefix) iteration
# [start, stop, reverse) ~ range( start, stop, (+1,-1) )
# single pass iterator
class ldb_iterator():

    # prefix != None => prefix_iter( prefix, include_(key|value), reverse )
    # prefix == None => range_iter( start, stop, include_(start|stop), include_(key|value), reverse )
    # prefix_closure(p) = min { s : s > p and s[:len(p)] != p }
    # prefix_iter( prefix ) ~ range_iter( prefix, prefix_closure )
    def __init__(
        self,
        db_ref,
        start=None,
        stop=None,
        prefix=None,
        include_start=True,
        include_stop=False,
        include_key=True,
        include_value=True,
        reverse=False
    ):

        if prefix != None:
            self.base_it = ldb_prefix_iterator( db_ref, prefix, include_key, include_value, reverse )
            return
        self.base_it = ldb_range_iter( db_ref, start, stop, include_start, include_stop, include_key, include_value, reverse )

    # need to consider [include_start] [include_stop] in iteration
    # prefix needs to consider alphabetic ordering
    def has_next(self):
        return self.base_it.has_next()

    def get_next(self):
        return self.base_it.get_next()
