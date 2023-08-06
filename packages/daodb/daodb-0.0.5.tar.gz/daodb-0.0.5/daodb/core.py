'''
The basic implementation with records as binary data.

XXX use sync? -- from atomicwrites

Copyright 2022 AXY axy@declassed.art
License: BSD, see LICENSE for details.
'''

import fcntl
import os
import struct
import threading

class DaoDBFiles:
    '''
    This is a helper class that encapsulates database files.
    '''
    def __init__(self):
        self.index_file = None
        self.data_file = None

    def open_db_files(self, base_path, mode):
        if mode not in ['r', 'w']:
            raise Exception(f'Wrong mode: {mode}')
        if mode == 'w':
            dest_dir = os.path.dirname(base_path)
            if dest_dir:
                os.makedirs(dest_dir, exist_ok=True)
        try:
            self.index_file = DaoDBIndexFile(base_path, mode)
            self.data_file = DaoDBDataFile(base_path, mode)
        except:
            self.close()
            raise

    def __del__(self):
        self.close()

    def close(self):
        if self.index_file:
            self.index_file.close()
            self.index_file = None
        if self.data_file:
            self.data_file.close()
            self.data_file = None


def _make_open_flags(mode):
    '''
    `mode`: 'r' or 'w'.
    Return flags for `os.open`.
    '''
    flags = os.O_CREAT
    if mode == 'r':
        flags |= os.O_RDONLY
    else:
        flags |= os.O_RDWR
    # XXX add file permissions, based on umask
    return flags


class DaoDB(DaoDBFiles):

    def __init__(self, base_path, mode='r'):
        super().__init__()
        self.base_path = base_path
        self.rlock = threading.RLock()
        self.open_db_files(base_path, mode)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def __iter__(self):
        return self.forward_iterator()

    def __getitem__(self, key):
        if isinstance(key, int):
            if key < 0:
                # for negative key need to get the number of records to calculate record index
                count = self.count()
                record_id = count + key
                if record_id < 0 or record_id >= count:
                    raise IndexError(f'Record index {key} out of range 0..{count}')
                return self.read(record_id)
            else:
                # faster implementation for positive key
                record = self.read(key)
                if record is None:
                    raise IndexError(f'Record index {key} out of range')
                else:
                    return record
        elif isinstance(key, slice):
            count = self.count()
            start, stop, step = key.indices(count)
            if step > 0:
                return self.forward_iterator(start, stop, step)
            else:
                return self.reverse_iterator(start, stop, step)
        else:
            raise TypeError(f'Record indices must be integers or slices, not {type(key).__name__}')

    def load_record(self, data_file, pos, size):
        return data_file.read(pos, size)

    def forward_iterator(self, start=0, stop=None, step=1):
        '''
        Forward iterator, all parameters should be positive if provided.
        '''
        if stop is not None and start >= stop:
            return
        # open files again for distinct seek operations
        db_files = DaoDBFiles()
        db_files.open_db_files(self.base_path, 'r')
        try:
            if start == 0:
                data_pos = 0
            else:
                # skip to the start record
                data_pos = db_files.index_file.read_nth_entry(start - 1)
            n = start
            while True:
                next_pos = db_files.index_file.read_entry()
                if next_pos is None:
                    break
                size = next_pos - data_pos
                data = self.load_record(db_files.data_file, data_pos, size)
                yield data

                n += step
                if stop is not None and n >= stop:
                    break

                if step == 1:
                    data_pos = next_pos
                else:
                    data_pos = db_files.index_file.read_nth_entry(n - 1)
        finally:
            db_files.close()

    def reverse_iterator(self, start=None, stop=None, step=None):
        raise NotImplementedError('Reverse iteration is not implemented yet')

    def read(self, record_id):
        with self.rlock:
            if record_id == 0:
                data_pos = 0
                next_pos = self.index_file.read_nth_entry(0)
            else:
                data_pos = self.index_file.read_nth_entry(record_id - 1)
                next_pos = self.index_file.read_entry()
            if next_pos is None:
                return None
            else:
                size = next_pos - data_pos
                return self.load_record(self.data_file, data_pos, size)

    def append(self, data):
        '''
        Append new record and return its index (i.e. record id)
        '''
        with self.rlock:
            with self.index_file.lock():
                # If previous append was unsuccessfull, the data file may contain garbage at the end.
                # Get the position for writing from the index file instead of simply appending to the data file.
                pos = self.index_file.read_last_entry()
                if pos is None:
                    pos = 0
                next_pos = self.data_file.write(pos, data)
                return self.index_file.append(next_pos)

    def rollback(self, n=1):
        '''
        Rollback last n records.

        XXX Basically, this is a way to shoot in the foot.
        For now acceptable use is in a single writer only.
        '''
        with self.rlock:
            with self.index_file.lock():
                pos = self.index_file.rollback(n)
                self.data_file.truncate(pos)

    def count(self):
        '''
        Return the number of records.
        '''
        with self.rlock:
            return self.index_file.count()

    def lock(self):
        '''
        Lock the database by acquiring index file lock.
        # XXX test required
        '''
        self.rlock.acquire()
        try:
            self.index_file.lock()
        except:
            self.rlock.release()
            raise
        return DaoDBLockContext(self.unlock)

    def unlock(self):
        '''
        Unlock database.
        '''
        self.index_file.unlock()
        self.rlock.release()


class DaoDBLockContext:
    '''
    Helper class for `DaoDB.lock` method.
    '''
    def __init__(self, unlock_method):
        self.unlock_method = unlock_method

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.unlock_method()


class DaoDBIndexFile:

    entry_format = '<Q'
    entry_size = struct.calcsize(entry_format)

    def __init__(self, base_path, mode):
        self.fd = None
        self.fd = os.open(base_path + '.index', _make_open_flags(mode))

    def __del__(self):
        self.close()

    def close(self):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None

    def lock(self):
        fcntl.lockf(self.fd, fcntl.LOCK_EX)
        return DaoDBLockContext(self.unlock)

    def unlock(self):
        fcntl.lockf(self.fd, fcntl.LOCK_UN)

    def seek(self, entry_index):
        if entry_index < 0:
            # seek from the end, this may raise OSError if resulting position is negative
            os.lseek(self.fd, entry_index * self.entry_size, os.SEEK_END)
        else:
            # seek from the beginning
            os.lseek(self.fd, entry_index * self.entry_size, os.SEEK_SET)

    def read_entry(self):
        '''
        Read entry at current position.
        '''
        entry = os.read(self.fd, self.entry_size)
        if len(entry) == self.entry_size:
            return struct.unpack(self.entry_format, entry)[0]
        else:
            return None

    def read_nth_entry(self, n):
        '''
        Read Nth entry.
        '''
        self.seek(n)
        return self.read_entry()

    def read_last_entry(self):
        '''
        Read last entry.
        '''
        try:
            self.seek(-1)
        except OSError:
            # index file is empty
            return None
        return self.read_entry()

    def append(self, entry):
        '''
        Append new entry and return its index in the file.
        '''
        pos = os.lseek(self.fd, 0, os.SEEK_END)
        os.write(self.fd, struct.pack(self.entry_format, entry))
        return pos // self.entry_size

    def rollback(self, n):
        '''
        Rollback last n entries.
        Return position for writing to the data file.
        '''
        try:
            self.seek(-n-1)
        except OSError:
            os.ftruncate(self.fd, 0)
            return 0
        entry = self.read_entry()
        os.ftruncate(self.fd, os.lseek(self.fd, 0, os.SEEK_CUR))
        return entry

    def count(self):
        return os.lseek(self.fd, 0, os.SEEK_END) // self.entry_size


class DaoDBDataFile:

    def __init__(self, base_path, mode):
        self.fd = None
        self.fd = os.open(base_path + '.data', _make_open_flags(mode))

    def close(self):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None

    def __del__(self):
        self.close()

    def read(self, pos, size):
        '''
        Read `size` bytes from data file starting from `pos`.
        '''
        os.lseek(self.fd, pos, os.SEEK_SET)
        return os.read(self.fd, size)

    def write(self, pos, data):
        os.lseek(self.fd, pos, os.SEEK_SET)
        bytes_written = os.write(self.fd, data)
        return pos + bytes_written

    def truncate(self, pos):
        os.ftruncate(self.fd, pos)
