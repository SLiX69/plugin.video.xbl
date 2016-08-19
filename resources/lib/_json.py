import os
import io
import json
import xbmc, xbmcvfs, xbmcaddon

addonID = "plugin.video.xbl"
addon = xbmcaddon.Addon(id=addonID)
dir_userdata = xbmc.translatePath(addon.getAddonInfo('profile'))
dir_db = os.path.join(dir_userdata, 'db')
file_games = os.path.join(dir_db, 'games.json')

log_msg = addonID + ' - _json_lib -'


def read_json(db_file):
    xbmc.log(log_msg + '!READ JSON!', 1)
    xbmc.log(log_msg + 'File: '+db_file, 1)
    if xbmcvfs.exists(db_file):
        xbmc.log(log_msg+'File Exists', 1)
        with open(db_file) as f:
            try:
                data = json.load(f)
                f.close()
            except ValueError:
                data = {}
    else:
        xbmc.log(log_msg + 'File Not Exists', 1)
        data = {}
    return data


def write_json(db_file, data):
    xbmc.log(log_msg + '!WRITE JSON!', 1)
    xbmc.log(log_msg + 'File: ' + db_file, 1)
    check_dir_userdata()
    with io.open(db_file, 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(data, ensure_ascii=False)))
        f.close()


def check_dir_userdata():
    if not xbmcvfs.exists(dir_userdata):
        xbmcvfs.mkdir(dir_userdata)
    check_dir_db()


def check_dir_db():
    if not xbmcvfs.exists(dir_db):
        xbmcvfs.mkdir(dir_db)


def check_file(file_db):
    if xbmcvfs.exists(file_db):
        return True
