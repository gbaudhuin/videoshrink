import mediainfo
#import subprocess
import settings
import os


class Converter:
    def __init__(self, filepath_in, filepath_out):
        self.filepath_in = filepath_in
        self.filepath_out = filepath_out
        self.mediainfo = mediainfo.MediaInfo(self.filepath_in)
        self.rotateCW = False
        self.rotateCCW = False
        self.quality = 22  # ffmpeg quality goes from 0 to 51. lower is better. Typical values are taken in 18-28 range.
        self.height = 720
        self.soundHD = True
        self.nosound = False

    def run(self):
        ffmpeg_args = self.get_ffmpeg_args()
        print("Args : " + ffmpeg_args)
        stream = os.popen(settings.ffmpegpath + " " + ffmpeg_args)
        stream.read()

    def get_ffmpeg_args(self):
        vf = self.get_video_filter()
        ffmpeg_args = ["-i \"" + self.filepath_in + "\"",
                       "-c:v libx265"]
        if vf:
            ffmpeg_args += ["-vf \"" + vf + "\""]

        ffmpeg_args += ["-pix_fmt yuv420p",
                        "-preset medium",
                        "-crf " + str(self.quality)]

        if self.nosound:
            ffmpeg_args += ["-an"]
        elif self.soundHD:
            ffmpeg_args += ["-c:a aac -ac 2 -ab 64000 -ar 44100"]
        else:
            ffmpeg_args += ["-c:a aac -ac 1 -ab 32000 -ar 22050"]

        ffmpeg_args += ["\"" + self.filepath_out + "\""]

        ffmpeg_args_str = " ".join(ffmpeg_args)
        return ffmpeg_args_str

    def get_video_filter(self):
        video_filters = []
        if self.height < self.mediainfo.height:
            if self.mediainfo.isvertical:
                video_filters.append("scale=" + str(self.height) + ":-1")
            else:
                video_filters.append("scale=-1:" + str(self.height))
        if self.rotateCW:
            video_filters.append("transpose=1")
        elif self.rotateCCW:
            video_filters.append("transpose=2")
        vf = ",".join(video_filters)

        return vf
