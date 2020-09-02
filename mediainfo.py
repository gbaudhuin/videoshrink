import subprocess
import json
import settings
import os


class MediaInfo:
    def __init__(self, filename):
        self.filename = filename
        self.video_streams_count = 0
        self.audio_streams_count = 0
        self._get_ffmpeg_info()

    def _get_ffmpeg_info(self):
        ret = subprocess.run([settings.ffprobepath, '-print_format', 'json', '-show_streams', self.filename],
                             capture_output=True)
        self.info = json.loads(ret.stdout)
        self._analyze_all_streams()

    def _analyze_all_streams(self):
        self.duration = 0
        for streaminfo in self.info['streams']:
            if (streaminfo['codec_type'] == 'video'):
                if (self.video_streams_count == 0):
                    self._analyze_video(streaminfo)
                self.video_streams_count += 1
            if (streaminfo['codec_type'] == 'audio'):
                if (self.audio_streams_count == 0):
                    self._analyze_audio(streaminfo)
                self.audio_streams_count += 1
        self._getglobalbitrate()

    def _analyze_video(self, streaminfo):
        self.video_codec_name = streaminfo['codec_name']
        self.width = int(streaminfo['width'])
        self.height = int(streaminfo['height'])
        self.frame_rate = streaminfo['avg_frame_rate']
        self.isvertical = False
        try:
            rotate = int(streaminfo['tags']['rotate'])
            if rotate == 90 or rotate == 270:
                self.isvertical = True
        except KeyError:
            pass
        self._getduration(streaminfo)

    def _analyze_audio(self, streaminfo):
        self.audio_codec_name = streaminfo['codec_name']
        self.sample_rate = int(streaminfo['sample_rate'])
        self.channels = int(streaminfo['channels'])
        self._getduration(streaminfo)

    def _getduration(self, streaminfo):
        if (self.duration < 0.001):
            try:
                self.duration = float(streaminfo['duration'])
            except KeyError:
                try:
                    self.duration = self._get_duration_from_another_ffprobe()
                except KeyError:
                    pass

    def _getglobalbitrate(self):
        size = os.path.getsize(self.filename)
        self.bit_rate = 8 * size / self.duration

    def _get_duration_from_another_ffprobe(self):
        ret = subprocess.run([settings.ffprobepath,
                              '-v', 'error',
                              '-show_entries', 'format=duration',
                              '-of', 'default=noprint_wrappers=1:nokey=1',
                              self.filename],
                             capture_output=True)
        return float(ret.stdout)
