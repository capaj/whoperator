from collections import deque
import fnmatch
import os
from threading import Thread, Event
import uuid

# TODO: Add scan completion callbacks and track scans that haven't completed
# WIP: migrating things into job class as much as possible.
# Thinking of having it act as a generator for the files the scanner should scan.

# Processing callbacks handle specific file types and return usable data.
# Data callbacks do something with the data returned by the processing callback.


class InvalidScanTargetException(Exception):
    pass


class FileScanner(object):
    def __init__(self, app):
        self.scanning_queue = deque([])
        self.global_filetype_handlers = {}
        self.scan_thread = None
        self.current_job = None
        self.stop_event = Event()
        self.app = app

    def set_global_filetype_handler(self, type_glob_string, handler_callback):
        if callable(handler_callback):
            self.global_filetype_handlers[type_glob_string] = handler_callback
        else:
            raise Exception("Callback for filetype handler wasn't callable.")

    def remove_global_filetype_handler(self, type_glob_string):
        if type_glob_string in self.global_filetype_handlers:
            del self.global_filetype_handlers[type_glob_string]
            return True
        else:
            return False

    def scan_directory(self, directory_path, file_data_callback, context, filetype_filter='*', recurse=True, priority=False):
        if not os.path.isdir(directory_path):
            raise InvalidScanTargetException("Path '%s' is not a directory." % directory_path)

        if filetype_filter != '*' and not len(fnmatch.filter(self.global_filetype_handlers.iterkeys(), filetype_filter)):
            raise InvalidScanTargetException("No filetype handler defined for current filetype_filter (%s)." %
                                             filetype_filter)

        job = ScannerJob(directory_path, file_data_callback, None, context, filetype_filter, recurse)
        job.filetype_handlers = self.global_filetype_handlers.copy()

        self.app.logger.info("New scan job id: %s" % job.job_id)
        if priority:
            self.scanning_queue.appendleft(job)
        else:
            self.scanning_queue.append(job)

        self._start_scan_thread()

    def scan_file(self, file_path, file_data_callback, context, priority=False):
        if not os.path.isfile(file_path):
            raise InvalidScanTargetException("Path '%s' is not a file." % file_path)

        if not len([fnmatch.fnmatch(file_path, pattern) for pattern in self.global_filetype_handlers.iterkeys()]):
            raise InvalidScanTargetException("No filetype_handler defined for specified file.")

        job = ScannerJob(file_path, file_data_callback, None, context, '*', False)
        job.filetype_handlers = self.global_filetype_handlers.copy()

        self.app.logger.info("New scan job id: %s" % job.job_id)
        if priority:
            self.scanning_queue.appendleft(job)
        else:
            self.scanning_queue.append(job)

        self._start_scan_thread()

    def _process_scan_queue(self, scanning_queue, stop_event):
        while len(scanning_queue) and not stop_event.is_set():
            self.current_job = scanning_queue.popleft()

            self.app.logger.debug("Starting scan job id: %s" % self.current_job.job_id)

            for file_to_scan in self.current_job.files():
                if not stop_event.is_set():
                    self.app.logger.debug("Scanning file: %s" % file_to_scan.path)
                    file_to_scan.scan()
                else:
                    scanning_queue.appendleft(self.current_job)
                    self.current_job = None
                    return

            self.current_job.complete()

            self.current_job = None

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
        self.current_job = None


class ScannerJob():
    def __init__(self, path, file_data_callback, completion_callback, context, filetype_filter, recurse):
        self.job_id = uuid.uuid4()
        self.filetype_handlers = {}

        self.scan_path = path
        self.is_dir = os.path.isdir(self.scan_path)

        self.data_callback = file_data_callback
        self.completion_callback = completion_callback

        self.context = context
        self.filetype_filter = filetype_filter
        self.recurse = recurse

    def files(self):
        if self.is_dir:
            if self.recurse:
                for root_dir, dirnames, filenames in os.walk(self.scan_path):
                    if self.filetype_filter != '*':
                        filenames = fnmatch.filter(filenames, self.filetype_filter)
                    for filename in filenames:
                        processing_callbacks = [callback for type_glob_string, callback
                                in self.filetype_handlers.iteritems()
                                if fnmatch.fnmatch(filename, type_glob_string)]
                        yield ScannerJobFile(os.path.join(root_dir, filename), processing_callbacks, self.data_callback, self.context)
            else:
                file_paths = os.listdir(self.scan_path)
                if self.filetype_filter != '*':
                    file_paths = fnmatch.filter(file_paths, self.filetype_filter)
                for file_path in file_paths:
                    processing_callbacks = [callback for type_glob_string, callback
                                in self.filetype_handlers.iteritems()
                                if fnmatch.fnmatch(file_path, type_glob_string)]
                    yield ScannerJobFile(os.path.join(self.scan_path, file_path), processing_callbacks, self.data_callback, self.context)
        else:  # single file
            yield ScannerJobFile(self.scan_path, self.data_callback, self.context)

    def complete(self):
        if callable(self.completion_callback):
            self.completion_callback(self.job_id, self.scan_path, self.context)

    def set_filetype_handler(self, type_glob_string, handler_callback):
        if callable(handler_callback):
            self.filetype_handlers[type_glob_string] = handler_callback
        else:
            raise Exception("Callback for filetype handler wasn't callable.")

    def remove_filetype_handler(self, type_glob_string):
        if type_glob_string in self.filetype_handlers:
            del self.filetype_handlers[type_glob_string]
            return True
        else:
            return False


class ScannerJobFile():
    def __init__(self, path, processing_callbacks, file_data_callback, context):
        self.path = path
        self.processing_callbacks = list(processing_callbacks) if processing_callbacks else []
        self.data_callback = file_data_callback
        self.context = context

    def scan(self):
        for processing_callback in self.processing_callbacks:
            if not callable(processing_callback):
                raise Exception("Processing callback was uncallable.")

            processing_result = processing_callback(self.path, context=self.context)
            if processing_result is not None and self.data_callback is not None:
                if isinstance(processing_result, (list, tuple)):
                    self.data_callback(*processing_result, context=self.context)
                else:
                    self.data_callback(processing_result, context=self.context)
