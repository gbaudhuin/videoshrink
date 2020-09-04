# videoshrink
A python script that shrinks video files with almost no quality loss.

## Usage

```shell
py go.py
```

## Description
This project targets short videos made with low quality cameras (phones, old cameras, etc.).
It looks for files recusively and converts them to H265/aac if not in this format.

Conversion is done in multiple passes :

- A first call to *py go.py*, files are converted to *out* directory.
- User checks files and move them to *out/ok*, *out/ko* or *out/kill* directories
    - ok : output is ok
    - ko : output is not ok
    - kill : original file should be deleted
- A second call to *py go.py* will take care of files in *out/ok*, *out/ko* or *out/kill* directories :
    - ok : original is overwritten by converted file
    - ko : original file is kept as is. converted file is deleted
    - kill : original file and converted file are deleted

## Output quality
By default, output quality is medium H265 for video. This should not change original quality too much.
Resolution is set to a maximum of 720p. Bigger video are scaled down. This actually has a small effect because 1080p movies made with low range cameras and phones are usually a bit blurry.
Audio is set to AAC mono 32K : stereo is nonsense for such videos. 32K AAC is more than enough if you think about the way sound is recored from the tiny microphones used on phones and cameras.
