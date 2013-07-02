from collections import deque
import glob
import fnmatch
import os
from threading import Thread


class InvalidScanTargetException(Exception):
    pass


class FileScanner(object):
    def __init__(self):
        self.scanning_queue = deque([])
        self.filetype_handlers = {}
        self.scan_thread = None
        self.current_scan = None

    def set_filetype_handler(self, type_glob_string, handler_callback):
        self.filetype_handlers[type_glob_string] = handler_callback

    def remove_filetype_handler(self, type_glob_string):
        if type_glob_string in self.filetype_handlers:
            del self.filetype_handlers[type_glob_string]
            return True
        else:
            return False

    def scan_directory(self, directory_path, file_data_callback, filetype_filter='*', priority=False):
        # TODO: Make recursion optional
        if not os.path.isdir(directory_path):
            raise InvalidScanTargetException("Path '%s' is not a directory." % directory_path)

        if filetype_filter != '*' and not len(fnmatch.filter(self.filetype_handlers.iterkeys(), filetype_filter)):
            raise InvalidScanTargetException("No filetype handler defined for current filetype_filter (%s)." %
                                             filetype_filter)

        queue_item = (directory_path, file_data_callback, filetype_filter)
        if priority:
            self.scanning_queue.appendleft(queue_item)
        else:
            self.scanning_queue.append(queue_item)

        self._start_scan_thread()

    def scan_file(self, file_path, file_data_callback, priority=False):
        if not os.path.isfile(file_path):
            raise InvalidScanTargetException("Path '%s' is not a file." % file_path)

        if not len([fnmatch.fnmatch(file_path, pattern) for pattern in self.filetype_handlers.iterkeys()]):
            raise InvalidScanTargetException("No filetype_handler defined for specified file.")

        queue_item = (file_path, file_data_callback, '*')
        if priority:
            self.scanning_queue.appendleft(queue_item)
        else:
            self.scanning_queue.append(queue_item)

        self._start_scan_thread()

    def _process_scan_queue(self):
        while len(self.scanning_queue):
            self.current_scan = self.scanning_queue.popleft()

            path, data_callback, filetype_filter = self.current_scan
            if os.path.isdir(path):
                for dirname, dirnames, filenames in os.walk(path):
                    # TODO: fix recursion...we're getting duplicates
                    if filetype_filter != '*':
                        filenames = fnmatch.filter(filenames, filetype_filter)
                    for filename in filenames:
                        self.scanning_queue.appendleft((os.path.join(dirname, filename), data_callback, filetype_filter))
                self.current_scan = None
                continue

            processing_callbacks = [callback for type_glob_string, callback
                                    in self.filetype_handlers.iteritems()
                                    if fnmatch.fnmatch(path, type_glob_string)]

            for processing_callback in processing_callbacks:
                data_callback(processing_callback(path))

            self.current_scan = None

    def _start_scan_thread(self):
        if not self.scan_thread:
            self.scan_thread = Thread(target=self._process_scan_queue, name="FileScanner").start()

    def abort_scan(self):
        if self.scan_thread:
            old_queue = self.scanning_queue
            self.scanning_queue.clear()
            self.scan_thread.join()
            self.scan_thread = None
            if self.current_scan:
                old_queue.appendleft(self.current_scan)
                self.current_scan = None
            return old_queue
        else:
            return None
