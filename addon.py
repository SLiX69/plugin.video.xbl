#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from urllib import quote, unquote_plus, unquote, urlencode, quote_plus, urlretrieve
from resources.lib.xbox_api import XboxApi

addonID = "plugin.video.xbl"
addon = xbmcaddon.Addon(id=addonID)
fanart = ''
pluginhandle = int(sys.argv[1])
loglevel = 1
log_msg = addonID + ' - '

api_key = addon.getSetting('api-key')

xbl = XboxApi(api_key)

try:
    xuid = xbl.get_xuid()['xuid']
except KeyError:
    pass
    #login failed
    #create popup

def root():
    addDir(get_translation(30005), '', 'recs', '')


def get_recordings():
    data = xbl.get_user_gameclips(xuid)
    for rec in data:
        if rec['state'] == 'Published':
            name = rec['titleName'].encode('utf-8')
            xbmc.log(name)
            name += ' ' + rec['dateRecorded'].encode('utf-8')
            url1 = rec['gameClipUris'][0]['uri']
            thumb_sma = rec['thumbnails'][0]['uri']
            thumb_big = rec['thumbnails'][1]['uri']
            xbmc.log(name)
            xbmc.log(url1)
            addLink(name, url1, 'play', thumb_sma, '', '', '', thumb_big)


def addDir(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + quote_plus(url) + "&mode=" + str(mode) + "&name=" + quote_plus(name)
    ok = True
    item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    item.setInfo(type="Video", infoLabels={"Title": name})
    item.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(pluginhandle, url=u, listitem=item, isFolder=True)


def addLink(name, url, mode, iconimage, desc, duration, date, fanart):
    u = sys.argv[0] + "?url=" + quote_plus(url) + "&mode=" + str(mode)
    ok = True
    item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    item.setInfo(type="Video", infoLabels={'Genre': 'Xbox Live Recording', "Title": name, "Plot": desc, "Duration": duration, "dateadded": date})
    item.setProperty('IsPlayable', 'true')
    item.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(pluginhandle, url=u, listitem=item)
    xbmc.executebuiltin("Container.SetSortMethod(7)")


def play(url):
    try:
        video_url = url
        listitem = xbmcgui.ListItem(path=video_url)
        xbmcplugin.setResolvedUrl(pluginhandle, succeeded=True, listitem=listitem)
    except ValueError:
        pass


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
if type(url) == type(str()):
    url = unquote_plus(url)


if mode == 'recs':
    get_recordings()
elif mode == 'play':
    play(url)
else:
    root()

xbmcplugin.endOfDirectory(pluginhandle)