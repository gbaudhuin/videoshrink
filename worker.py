import settings
import glob
import os
from collections import OrderedDict
import pathlib
import mediatask


class Worker:
    def __init__(self):
        self._getvideofiles()
        self._iterator = iter(self.files)
        self.output_dir = settings.out_dir
        self.ok_dir = settings.ok_dir
        self.ko_dir = settings.ko_dir
        self._check_working_dirs()

    def _getvideofiles(self):
        files = []
        for filetype in settings.filetypes:
            files.extend(glob.glob(settings.rootpath + '/**/*.' + filetype, recursive=True))
        self.files = self._getfiles_orderedbysize_desc(files)

    def _getfiles_orderedbysize_desc(self, filesList):
        filesizes = {}
        for filepath in filesList:
            filesize = os.path.getsize(filepath)
            filesizes[filepath] = filesize
        orderedfiles = OrderedDict(sorted(filesizes.items(), key=lambda kv: kv[1], reverse=True))
        return orderedfiles

    def get_total_size(self):
        total_size = 0
        for filepath in self.files:
            total_size += self.files[filepath]
        return total_size

    def _check_working_dirs(self):
        self._create_dir_if_missing(self.output_dir)
        self._create_dir_if_missing(self.ok_dir)
        self._create_dir_if_missing(self.ko_dir)

    def _create_dir_if_missing(self, dir):
        if not os.path.isdir(dir):
            pathlib.Path(dir).mkdir(parents=True, exist_ok=True)

    def run(self):
        while (True):
            try:
                self.convert_next()
            except StopIteration:
                break

    def convert_next(self):
        filepath_in = next(self._iterator)
        task = mediatask.MediaTask(filepath_in)
        task.run()
