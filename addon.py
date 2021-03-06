#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from urllib import quote, unquote_plus, unquote, urlencode, quote_plus, urlretrieve
from resources.lib.xbox_api import XboxApi
from resources.lib._json import write_json, read_json, check_file, check_dir_userdata, dir_db, dir_userdata, file_games

addonID = "plugin.video.xbl"
addon = xbmcaddon.Addon(id=addonID)
fanart = ''
pluginhandle = int(sys.argv[1])
loglevel = 1
log_msg = addonID + ' - '

fr_fanart = False
fr_thumb = False
sc_thumb = False
#gm_xb360 = False
gm_yours = False
api_key = addon.getSetting('api-key')
lang = addon.getSetting('language')
if addon.getSetting('fr_fanart') == 'true': fr_fanart = True
if addon.getSetting('fr_thumb') == 'true': fr_thumb = True
if addon.getSetting('sc_thumb') == 'true': sc_thumb = True
#if addon.getSetting('gm_xb360') == 'true': gm_xb360 = True
if addon.getSetting('gm_yours') == 'true': gm_yours = True



xbl = XboxApi(api_key, lang)

try:
    xuid = xbl.get_xuid()['xuid']
except KeyError:
    xuid = ''
    #login failed
    #create popup

def root():
    #check_game_list_update()
    #check_dir_userdata()
    addDir(get_translation(30005), str(xuid), 'recs', '', '', '', '')
    addDir(get_translation(30006), str(xuid), 'scrn', '', '', '', '')
    addDir(get_translation(30007), str(xuid), 'fnds', '', '', '', '')
    addDir(get_translation(30008), str(xuid), 'gams', '', '', '', '')


def get_friends(xuid):
    data = xbl.get_user_friends(xuid)
    fanart = ''
    thumb = ''
    for friend in data:
        fr_xuid = str(friend['id'])
        name = friend['Gamertag']
        gmrsc = str(friend['Gamerscore'])
        if fr_thumb:
            thumb = friend['GameDisplayPicRaw']
        if fr_fanart:
            fanart = thumb
        addDir(name, fr_xuid, 'frnd', thumb, fanart, '', gmrsc)


def get_games(xuid, mode):
    games = {}
    if mode == 'gams':
        if addon.getSetting('up_games') == 'true':
            update_games()
            addon.setSetting(id='up_games', value='false')
        if check_file(file_games):
            games = get_games_from_db()
        else:
            games = get_games_from_api(xuid)
    elif mode == 'gams_frnd':
        games = get_games_from_api(xuid)
    list_games(games)


def update_games():
    xbmc.log('UPDATE GAMES')
    check_dir_userdata()
    games = []
    data = xbl.get_user_xone_games(xuid)
    for game in data['titles']:
        titleId = str(game['titleId'])
        game = get_game_details(titleId)
        games.append(game)
    #optional get xbox 360 games
    '''
    if gm_xb360:
        data = xbl.get_user_x360_games(xuid)
        for game in data['titles']:
            titleId = str(game['titleId'])
            #game = get_game_details(titleId)
            games.append(game)
    '''
    write_json(file_games, games)


def get_games_from_db():
    data = read_json(file_games)
    return data


def get_game_details(title_id):
    xbmc.log(str(title_id))
    title_id_hex = hex(int(title_id))[2:]
    data = xbl.get_game_details_hex(title_id_hex)
    name = data['Items'][0]['Name']
    desc = data['Items'][0]['Description']
    thumb, fanart = get_game_details_images(data['Items'][0]['Images'])
    game = {'name': name, 'titleId': title_id, 'thumb': thumb, 'desc': desc, 'fanart': fanart}
    return game


def list_games(games):
    for game in games:
        thumb = ''
        fanart = ''
        desc = ''
        if 'thumb' in game:
            thumb = game['thumb']
        if 'fanart' in game:
            fanart = game['fanart']
        if 'desc' in game:
            desc = game['desc'].encode('utf-8')
        name = game['name'].encode('utf-8')
        #xbmc.log(name)
        titleId = str(game['titleId'])
        #xbmc.log(str(xuid))
        #xbmc.log(str(name))
        addDir(name, str(xuid), 'game', thumb, fanart, desc, titleId)


def get_game_details_images(data):
    thumb = ''
    fanart = ''
    print data
    for image in data:
        print image
        if image['Purpose'] == 'BrandedKeyArt':
            thumb = image['Url']
        if image['Purpose'] == 'TitledHeroArt':
            fanart = image['Url']
    return thumb, fanart


def get_games_from_api(xuid):
    games = []
    data = xbl.get_user_xone_games(xuid)
    for game in data['titles']:
        name = game['name']#.encode('utf-8')
        titleId = str(game['titleId'])
        game = {'name': name, 'titleId': titleId}
        games.append(game)
    #optional get xbox 360 games
    '''
    if gm_xb360:
        data = xbl.get_user_x360_games(xuid)
        for game in data['titles']:
            name = game['name'].encode('utf-8')
            titleId = str(game['titleId'])
            game = {'name': name, 'titleId': titleId}
            games.append(game)
    '''
    return games


def get_game(xuid, titleId):
    addDir(get_translation(30030), xuid, 'stat', '', '', '', titleId)  # Game-Stats
    addDir(get_translation(30031), xuid, 'achv', '', '', '', titleId)  # Achievements
    addDir(get_translation(30033), xuid, 'recs_titl', '', '', '', titleId)  # Recordings
    addDir(get_translation(30034), xuid, 'scrn_titl', '', '', '', titleId)  # Screenshots
    if gm_yours:
        addDir(get_translation(30038), xuid, 'recs_your', '', '', '', titleId)  # Your Recordings
        addDir(get_translation(30039), xuid, 'scrn_your', '', '', '', titleId)  # Your Screenshots


def get_game_stats(xuid, titleId):
    stats = []
    data = xbl.get_user_game_stats_by_title(xuid, titleId)
    for i in data['statlistscollection'][0]['stats']:
        name = i['name'].encode('utf-8')
        if 'value' in i:
            value = str(i['value']).encode('utf-8')
        else:
            value = ''
        stat = {'name': name, 'value': value}
        stats.append(stat)
    for i in data['groups'][0]['statlistscollection'][0]['stats']:
        name = i['groupproperties']['DisplayName'].encode('utf-8')
        if 'value' in i:
            value = str(i['value']).encode('utf-8')
        else:
            value = ''
        stat = {'name': name, 'value': value}
        stats.append(stat)
    # List stats
    for i in stats:
        name = i['name']
        value = i['value']
        name += ' ' + value
        addDir(name, '', '', '', '', '', '')


def get_achievements(xuid, titleId):
    data = xbl.get_user_achievements_by_title(xuid, titleId)
    for achiev in data:
        name = (achiev['name']).encode('utf-8')
        if achiev['progressState'] == 'Achieved':
            value = '[COLOR green]%sGS[/COLOR]' % achiev['rewards'][0]['value']
            date = get_clean_datetime(achiev['progression']['timeUnlocked']).encode('utf-8')
            desc = date + (get_translation(30051) + '\n').encode('utf-8')
            desc += achiev['description'].encode('utf-8')
        elif achiev['progressState'] == 'NotStarted':
            value = '[COLOR red]%sGS[/COLOR]' % achiev['rewards'][0]['value']
            desc = achiev['description'].encode('utf-8')
        name += ' - ' + value
        fanart = achiev['mediaAssets'][0]['url']
        addDir(name, '', '', fanart, fanart, desc, '')


def get_recordings(xuid):
    data = xbl.get_user_gameclips(xuid)
    list_recordings(data)


def get_recordings_for_title(titleId):
    data = xbl.get_gameclips_by_title(titleId)
    list_recordings(data)


def get_user_recordings_for_title(xuid, titleId):
    data = xbl.get_user_gameclips_by_title(xuid, titleId)
    list_recordings(data)


def get_screenshots(xuid):
    data = xbl.get_user_screenshots(xuid)
    list_screenshots(data)


def get_screens_for_title(titleId):
    data = xbl.get_screenshots_by_title(titleId)
    list_screenshots(data)


def get_user_screens_for_title(xuid, titleId):
    data = xbl.get_user_screenshots_by_title(xuid, titleId)
    list_screenshots(data)


def list_screenshots(data):
    for pic in data:
        xbmc.log(str(pic))
        name = pic['titleName'].encode('utf-8')
        name += ' ' + pic['dateTaken'].encode('utf-8')
        url1 = pic['screenshotUris'][0]['uri']
        thumb = pic['thumbnails'][0]['uri']
        fanart = pic['thumbnails'][1]['uri']
        if sc_thumb:
            fanart = url1
        #addLink(name, url1, 'play', '', '', '', '', '')
        addImage(name, url1, thumb, fanart, 0)


def list_recordings(data):
    for rec in data:
        if rec['state'] == 'Published':
            name = rec['titleName'].encode('utf-8')
            #xbmc.log(name)
            date_recorded = rec['dateRecorded'].encode('utf-8')
            name += ' ' + date_recorded
            url1 = rec['gameClipUris'][0]['uri']
            thumb_sma = rec['thumbnails'][0]['uri']
            thumb_big = rec['thumbnails'][1]['uri']
            duration = rec['durationInSeconds']
            desc = 'rating: %s, ratingCount: %s, views: %s \ncommentCount: %s, likeCount: %s, shareCount: %s'\
                   % (rec['rating'], rec['ratingCount'], rec['views'],
                      rec['commentCount'], rec['likeCount'], rec['shareCount'])
            addLink(name, url1, 'play', thumb_sma, desc, duration, date_recorded, thumb_big)



def get_user_presence(xuid):
    data = xbl.get_user_presence(xuid)
    gmrsc = xbmc.getInfoLabel("ListItem.Writer")
    thumb = xbmc.getInfoLabel("ListItem.Thumb")
    fanart = xbmc.getInfoLabel("ListItem.Art(fanart)")
    usr_state = data['state']
    usr_state2 = usr_state # save state for later use
    #name = unquote(name).decode('utf8')
    name = xbmc.getInfoLabel("ListItem.Title")
    name += get_translation(30020)
    #replace 'try's with if key exists
    if usr_state == 'Online':
        usr_state = '[COLOR green]%s[/COLOR]' % usr_state
        for i in data['devices'][0]['titles']:
            if i['placement'] == 'Full':
                state = i['name']
    elif usr_state == 'Offline':
        state = get_translation(30022)
        usr_state = '[COLOR red]%s[/COLOR]' % usr_state
        # lastSeen may not be available
        # make this better
        try:
             state += data['lastSeen']['titleName']
        except:
            state += 'unknown'
    name += usr_state # add colored state to gamertag + 30020
    addDir(name, '', 'end', thumb, fanart, '', '')
    if 'lastSeen' in data or usr_state2 == 'Online':
        addDir(state, '', 'end', thumb, fanart, '', '')
    gmrsc = get_translation(30023) + gmrsc
    addDir(gmrsc, '', 'end', thumb, fanart, '', '')
    addDir(get_translation(30005), str(xuid), 'recs', '', '', '', '')
    addDir(get_translation(30006), str(xuid), 'scrn', '', '', '', '')
    addDir(get_translation(30007), str(xuid), 'fnds', '', '', '', '')
    addDir(get_translation(30008), str(xuid), 'gams_frnd', '', '', '', '')


def addDir(name, url, mode, iconimage, fanart, desc, extra1):
    u = sys.argv[0] + "?url=" + quote_plus(url) + "&mode=" + str(mode) + "&name=" + quote_plus(name) + "&extra1=" + str(extra1)
    ok = True
    item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    item.setInfo(type="Video", infoLabels={"Title": name, "Plot": desc})
    item.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(handle=pluginhandle, url=u, listitem=item, isFolder=True)


def addLink(name, url, mode, iconimage, desc, duration, date, fanart):
    u = sys.argv[0] + "?url=" + quote_plus(url) + "&mode=" + str(mode)
    ok = True
    item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    item.setInfo(type="Video", infoLabels={'genre': 'Xbox Live', 'aired': date, 'title': name, 'plot': desc, 'duration': duration})
    item.setProperty('IsPlayable', 'true')
    item.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(pluginhandle, url=u, listitem=item)


def addImage(name, url, iconimage, fanart, tot=0):
    item = xbmcgui.ListItem(name, iconImage="DefaultImage.png", thumbnailImage=iconimage)
    item.setInfo(type="image", infoLabels={"title": name})
    item.setProperty('fanart_image', fanart)
    return xbmcplugin.addDirectoryItem(handle=pluginhandle, url=url, listitem=item, totalItems=tot)


def play(url):
    try:
        video_url = url
        listitem = xbmcgui.ListItem(path=video_url)
        xbmcplugin.setResolvedUrl(pluginhandle, succeeded=True, listitem=listitem)
    except ValueError:
        pass


def get_clean_datetime(date_string):
    date = date_string[:10]
    time = date_string[11:19]
    return '%s %s' % (date, time)


def get_translation(string_id):
    return addon.getLocalizedString(string_id)


def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict


params = parameters_string_to_dict(sys.argv[2])
mode = params.get('mode')
url = params.get('url')
name = params.get('name')
extra1 = params.get('extra1')
if type(url) == type(str()):
    url = unquote_plus(url)


if mode == 'recs':
    get_recordings(url)
elif mode == 'scrn':
    get_screenshots(url)
elif mode == 'fnds':
    get_friends(url)
elif mode == 'frnd':
    get_user_presence(url)
elif mode == 'gams':
    get_games(url, mode)
elif mode == 'gams_frnd':
    get_games(url, mode)
elif mode == 'game':
    get_game(url, extra1)
elif mode == 'achv':
    get_achievements(url, extra1)
elif mode == 'stat':
    get_game_stats(url, extra1)
elif mode == 'recs_titl':
    get_recordings_for_title(extra1)
elif mode == 'scrn_titl':
    get_screens_for_title(extra1)
elif mode == 'recs_your':
    get_user_recordings_for_title(url, extra1)
elif mode == 'scrn_your':
    get_user_screens_for_title(url, extra1)
elif mode == 'play':
    play(url)
elif mode == 'end':
    pass
else:
    root()

xbmcplugin.endOfDirectory(pluginhandle)
