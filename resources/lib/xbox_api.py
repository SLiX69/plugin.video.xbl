# -*- coding: utf-8 -*-
import requests
import json

class XboxApi:
    # XboxApi key
    api_key = ""

    def __init__(self, api_key, lang):
        """Only requires the XboxApi key"""
        self.api_key = api_key
        self.language = lang

    def get_profile(self):
        """Return information for current token profile"""
        res = self.request("https://xboxapi.com/v2/profile")
        return res.json()

    def get_xuid(self):
        """Return your xuid"""
        res = self.request("https://xboxapi.com/v2/accountXuid")
        return res.json()

    def get_messages(self):
        """Return your messages"""
        res = self.request("https://xboxapi.com/v2/messages")
        return res.json()

    def get_conversations(self):
        """Return your messages"""
        res = self.request("https://xboxapi.com/v2/conversations")
        return res.json()

    def get_xuid_by_gamertag(self, gamertag):
        """Return XUID by gamertag"""
        res = self.request("https://xboxapi.com/v2/xuid/{}".format(gamertag))
        return res.json()

    def get_gamertag_by_xuid(self, xuid):
        """Return gamertag by XUID"""
        res = self.request("https://xboxapi.com/v2/gamertag/{}".format(xuid))
        return res.json()

    def get_user_profile(self, xuid):
        """Return profile by XUID"""
        res = self.request("https://xboxapi.com/v2/{}/profile".format(xuid))
        return res.json()

    def get_user_gamercard(self, xuid):
        """Return gamercard by XUID"""
        res = self.request("https://xboxapi.com/v2/{}/gamercard".format(xuid))
        return res.json()

    def get_user_presence(self, xuid):
        """Return current presence information by XUID"""
        res = self.request("https://xboxapi.com/v2/{}/presence".format(xuid))
        return res.json()

    def get_user_activity(self, xuid):
        """Return current activity information by XUID"""
        res = self.request("https://xboxapi.com/v2/{}/activity".format(xuid))
        return res.json()

    def get_user_activity_recent(self, xuid):
        """Return recent activity information by XUID"""
        res = self.request("https://xboxapi.com/v2/{}/activity/recent".format(xuid))
        return res.json()

    def get_user_friends(self, xuid):
        """Return friends by XUID"""
        res = self.request("https://xboxapi.com/v2/{}/friends".format(xuid))
        return res.json()

    def get_user_followers(self, xuid):
        """Return followers by XUID"""
        res = self.request("https://xboxapi.com/v2/{}/followers".format(xuid))
        return res.json()

    def get_recent_players(self):
        """Return recent players by XUID"""
        res = self.request("https://xboxapi.com/v2/recent-players")
        return res.json()

    def get_user_gameclips(self, xuid):
        """Return game clips by XUID"""
        res = self.request("https://xboxapi.com/v2/{}/game-clips".format(xuid))
        return res.json()
    # check
    def get_user_gameclips_saved(self, xuid):
        """Return user-saved game clips by XUID"""
        res = self.request("https://xboxapi.com/v2/{}/game-clips/saved".format(xuid))
        return res.json()
    # check
    def get_user_gameclips_by_title(self, xuid, titleId):
        """Return uses game clips by XUID and titleId"""
        res = self.request("https://xboxapi.com/v2/{}/game-clips/{}".format(xuid, titleId))
        return res.json()

    # test !!
    def get_gameclips_by_title(self, titleId):
        """Return saved gameclips by titleId """
        res = self.request("https://xboxapi.com/v2/game-clips/{}".format(titleId))
        return res.json()

    # test !!
    def get_user_screenshots(self, xuid):
        """Return screenshots by XUID"""
        res = self.request("https://xboxapi.com/v2/{}/screenshots".format(xuid))
        return res.json()

    # test !!
    #20
    def get_user_screenshots_by_title(self, xuid, titleId):
        """Return screenshots by XUID and titleId"""
        res = self.request("https://xboxapi.com/v2/{}/screenshots/{}".format(xuid, titleId))
        return res.json()

    # test !!
    #21
    def get_screenshots_by_title(self, titleid):
        """Return screenshots by titleId"""
        res = self.request("https://xboxapi.com/v2/screenshots/{}".format(titleid))
        return res.json()

    # test !!
    #22
    def get_user_game_stats_by_title(self, xuid, titleid):
        """Return game-stats by XUID and titleId"""
        res = self.request("https://xboxapi.com/v2/{}/game-stats/{}".format(xuid, titleid))
        return res.json()
    # test !!
    #23
    def get_user_x360_games(self, xuid):
        """Return Xbox 360 games by XUID"""
        res = self.request("https://xboxapi.com/v2/{}/xbox360games".format(xuid))
        return res.json()
    # test !!
    #24
    def get_user_xone_games(self, xuid):
        """Return Xbox One games by XUID"""
        res = self.request("https://xboxapi.com/v2/{}/xboxonegames".format(xuid))
        return res.json()
    # test !!
    #25
    def get_user_achievements_by_title(self, xuid, titleId):
        """Return Xbox games achievements by XUID and titleId"""
        res = self.request("https://xboxapi.com/v2/{}/achievements/{}".format(xuid, titleId))
        return res.json()




    def send_message(self, message, xuids=[]):
        """Send a message to a set of user(s)"""
        headers = {
            "X-AUTH": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "message": message,
            "to": []
        }

        for xuid in xuids:
            payload["to"].append(xuid)

        res = requests.post("https://xboxapi.com/v2/messages", headers=headers, data=json.dumps(payload))
        res.json()

    def request(self, url):
        """Wrapper on the requests.get"""
        headers = {
            "X-AUTH": self.api_key,
            "Accept-Language": self.language
        }
        res = requests.get(url, headers=headers, verify=False)
        return res
