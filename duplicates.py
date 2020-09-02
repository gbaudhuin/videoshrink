import settings
import glob
import os

#
# A short script to identify duplicates recursively
# Obvious ones are removed automatically. Others are just displayed.
#


def remove_if_obvious(file1, file2):
    cameraRoll = "C:\\Users\\baudh\\OneDrive\\Pictures\\Camera Roll"
    if cameraRoll in file1:
        os.remove(file1)
    elif cameraRoll in file2:
        os.remove(file2)


files = glob.glob(settings.rootpath + '/**/*.*', recursive=True)
filesizes = {}
filepaths = {}
excessive_size = 0
doubles_count = 0
for file in files:
    name = os.path.basename(file)
    filesize = os.path.getsize(file)
    if name in filesizes:
        if filesizes[name] == filesize:
            print("{} : {}  {:.1f}MB".format(file, filepaths[name], filesize / (1024 * 1024)))
            excessive_size += filesize
            doubles_count += 1
            remove_if_obvious(file, filepaths[name])
    else:
        filepaths[name] = file
        filesizes[name] = filesize
print("{:d} duplicates. Total excessive size : {:.1f} MB".format(doubles_count, excessive_size / (1024 * 1024)))
