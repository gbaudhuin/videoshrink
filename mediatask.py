import hashlib
import settings
import os
import converter
import shutil


class MediaTask:
    def __init__(self, filepath_in):
        self.filepath_in = filepath_in
        self._prepare_filepaths_out(filepath_in)

    def _prepare_filepaths_out(self, filepath_in):
        self.filename_out = hashlib.md5(filepath_in.encode('utf-8')).hexdigest() + "." + settings.fileextension_out
        self.filepath_out = os.path.join(settings.out_dir, self.filename_out)
        self.filepath_ok = os.path.join(settings.ok_dir, self.filename_out)
        self.filepath_ko = os.path.join(settings.ko_dir, self.filename_out)
        self.filepath_kill = os.path.join(settings.kill_dir, self.filename_out)

    def run(self):
        filesize_before_mb = os.path.getsize(self.filepath_in) / (1024 * 1024)
        #print(self.filepath_in + " ({:0.1f} MB):".format(filesize_before_mb))
        try:
            self.check_filesize_in()
            self.check_not_already_done()

            if not self.check_kill_file():
                if not self.check_replace_original():
                    conv = converter.Converter(self.filepath_in, self.filepath_out)
                    self.check_original_codec(conv)
                    self.convert(conv)
        except RuntimeError as error:
            #print("\tIgnored : " + str(error))
            pass
        except KeyError as error:
            print(self.filepath_in + " ({:0.1f} MB):".format(filesize_before_mb))
            print("\tIgnored : " + str(error))

    def check_filesize_in(self):
        filesize_before_mb = os.path.getsize(self.filepath_in) / (1024 * 1024)
        if (filesize_before_mb < settings.filesize_in_min_mb):
            raise RuntimeError("Input filesize too small (< {:0.1f} MB)".format(settings.filesize_in_min_mb))
        elif (filesize_before_mb > settings.filesize_in_max_mb):
            raise RuntimeError("Input filesize too big (> {:0.1f} MB)".format(settings.filesize_in_max_mb))

    def check_not_already_done(self):
        if os.path.isfile(self.filepath_out):
            filesize_after_mb = os.path.getsize(self.filepath_out) / (1024 * 1024)
            raise KeyError("Already converted in OUT : {} ({:0.1f} MB)".format(self.filename_out, filesize_after_mb))
        elif os.path.isfile(self.filepath_ko):
            filesize_after_mb = os.path.getsize(self.filepath_ko) / (1024 * 1024)
            raise RuntimeError("Rejected by user in KO : {} ({:0.1f} MB)".format(self.filename_out, filesize_after_mb))

    def check_kill_file(self):
        if os.path.isfile(self.filepath_kill):
            os.remove(self.filepath_in)
            os.remove(self.filepath_kill)
            print("Killed")
            return True
        return False

    def check_replace_original(self):
        if os.path.isfile(self.filepath_ok):
            filesize_after_mb = os.path.getsize(self.filepath_ok) / (1024 * 1024)
            shutil.copystat(self.filepath_in, self.filepath_ok)
            os.remove(self.filepath_in)
            if os.path.isfile(self.filepath_in + ".modd"):
                os.remove(self.filepath_in + ".modd")
            if os.path.isfile(self.filepath_in + ".tnl"):
                os.remove(self.filepath_in + ".tnl")
            if os.path.isfile(self.filepath_in.replace(".MP4", ".thm")):
                os.remove(self.filepath_in.replace(".MP4", ".thm"))
            shutil.move(self.filepath_ok, self.filepath_in)
            print("Replaced by {} ({:0.1f} MB)".format(self.filepath_ok, filesize_after_mb))
            return True
        return False

    def check_original_codec(self, conv):
        if conv.mediainfo.video_codec_name == 'h265' or conv.mediainfo.video_codec_name == 'hevc':
            raise RuntimeError("Codec already H265")
        elif (conv.mediainfo.bit_rate / 1000 < settings.maxbitrate_kbits):
            raise RuntimeError("Bitrate {:0.1f} < {:d} Kbits/s".format(conv.mediainfo.bit_rate / 1000, settings.maxbitrate_kbits))

    def convert(self, conv):
        conv.run()
        if os.path.isfile(self.filepath_in):
            filesize_before_mb = os.path.getsize(self.filepath_in) / (1024 * 1024)
            filesize_after = os.path.getsize(self.filepath_out)
            filesize_after_mb = filesize_after / (1024 * 1024)
            if filesize_after_mb < 0.001:
                raise RuntimeError("Output file size problem ({} : {:d} bytes)".format(self.filepath_out, filesize_after))
            else:
                print("Output size : {:0.1f} MB ({:0.1f}x smaller)".format(filesize_after_mb, filesize_before_mb / filesize_after_mb))
        else:
            raise RuntimeError("Output file not found after conversion ({})".format(self.filepath_out))
