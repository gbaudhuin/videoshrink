import glob
import os
from datetime import datetime
import pathlib


src = "C:\\Users\\baudh\\OneDrive\\Pictures\\Camera Roll"
dst = "C:\\Users\\baudh\\OneDrive\\Pictures"

files = glob.glob(src + '/*.*')


def get_month_fr(m):
    dico = {1: 'janvier',
            2: 'fevrier',
            3: 'mars',
            4: 'avril',
            5: 'mai',
            6: 'juin',
            7: 'juillet',
            8: 'aout',
            9: 'septembre',
            10: 'octobre',
            11: 'novembre',
            12: 'decembre'}
    return dico[m]


def _create_dir_if_missing(dir):
    if not os.path.isdir(dir):
        pathlib.Path(dir).mkdir(parents=True, exist_ok=True)


for file in files:
    name = os.path.basename(file)
    filesize = os.path.getsize(file)
    timestamp = os.path.getmtime(file)
    date = datetime.fromtimestamp(timestamp)
    m = get_month_fr(date.month)
    y = date.year
    dirname = 'divers {} {:d}'.format(m, y)
    dirname_full = dst + "\\" + dirname
    _create_dir_if_missing(dirname_full)
    print(src + "/" + name + " -> " + dirname_full + "/" + name)
    os.rename(src + "\\" + name, dirname_full + "\\" + name)
