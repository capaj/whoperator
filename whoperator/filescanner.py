from collections import deque
import fnmatch
import os
from threading import Thread, Event


class InvalidScanTargetException(Exception):
    pass


class FileScanner(object):
    def __init__(self, app):
        self.scanning_queue = deque([])
        self.filetype_handlers = {}
        self.scan_thread = None
        self.current_scan = None
        self.stop_event = Event()
        self.app = app

    def set_filetype_handler(self, type_glob_string, handler_callback):
        self.filetype_handlers[type_glob_string] = handler_callback

    def remove_filetype_handler(self, type_glob_string):
        if type_glob_string in self.filetype_handlers:
            del self.filetype_handlers[type_glob_string]
            return True
        else:
            return False

    def scan_directory(self, directory_path, file_data_callback, context, filetype_filter='*', recurse=True, priority=False):
        if not os.path.isdir(directory_path):
            raise InvalidScanTargetException("Path '%s' is not a directory." % directory_path)

        if filetype_filter != '*' and not len(fnmatch.filter(self.filetype_handlers.iterkeys(), filetype_filter)):
            raise InvalidScanTargetException("No filetype handler defined for current filetype_filter (%s)." %
                                             filetype_filter)

        queue_item = (directory_path, file_data_callback, context, filetype_filter, recurse)
        if priority:
            self.scanning_queue.appendleft(queue_item)
        else:
            self.scanning_queue.append(queue_item)

        self._start_scan_thread()

    def scan_file(self, file_path, file_data_callback, context, priority=False):
        if not os.path.isfile(file_path):
            raise InvalidScanTargetException("Path '%s' is not a file." % file_path)

        if not len([fnmatch.fnmatch(file_path, pattern) for pattern in self.filetype_handlers.iterkeys()]):
            raise InvalidScanTargetException("No filetype_handler defined for specified file.")

        queue_item = (file_path, file_data_callback, context, '*', False)
        if priority:
            self.scanning_queue.appendleft(queue_item)
        else:
            self.scanning_queue.append(queue_item)

        self._start_scan_thread()

    def _process_scan_queue(self, scanning_queue, stop_event):
        while len(scanning_queue) and not stop_event.is_set():
            self.current_scan = scanning_queue.popleft()

            path, data_callback, context, filetype_filter, recurse = self.current_scan
            if os.path.isdir(path):
                if recurse:
                    for root_dir, dirnames, filenames in os.walk(path):
                        if filetype_filter != '*':
                            filenames = fnmatch.filter(filenames, filetype_filter)
                        for filename in filenames:
                            scanning_queue.appendleft((os.path.join(root_dir, filename), data_callback, context, filetype_filter, False))
                else:
                    file_paths = os.listdir(path)
                    if filetype_filter != '*':
                        file_paths = fnmatch.filter(file_paths, filetype_filter)
                    for file_path in file_paths:
                        scanning_queue.appendleft((os.path.join(path, file_path), data_callback, context, filetype_filter, False))
                self.current_scan = None
                continue

            processing_callbacks = [callback for type_glob_string, callback
                                    in self.filetype_handlers.iteritems()
                                    if fnmatch.fnmatch(path, type_glob_string)]

            for processing_callback in processing_callbacks:
                self.app.logger.debug("Scanning file: %s" % path)
                processing_result = processing_callback(path, context=context)
                if processing_result is not None:
                    if isinstance(processing_result, (list, tuple)):
                        data_callback(*processing_result, context=context)
                    else:
                        data_callback(processing_result, context=context)
                else:
                    self.app.logger.debug("Scan returned None!")

            self.current_scan = None

    def _start_scan_thread(self):
        if not self.scan_thread:
            self.app.logger.info("Starting file scan...")
            self.scan_thread = Thread(target=self._process_scan_queue,
                                      name="FileScanner",
                                      args=[self.scanning_queue, self.stop_event])
            self.scan_thread.start()

    def resume_scan(self):
        if len(self.scanning_queue):
            self._start_scan_thread()

    def stop_scan(self):
        self.stop_event.set()
        if self.scan_thread and self.scan_thread.isAlive():
            self.scan_thread.join()
        self.scan_thread = None
        self.stop_event = Event()
        return self.scanning_queue

    def clear_queue(self):
        self.scanning_queue.clear()
        self.current_scan = None


