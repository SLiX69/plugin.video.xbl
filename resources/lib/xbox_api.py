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
    # test !!
    #26
    def get_game_details_hex(self, titleId):
        """Return the Xbox Game Information (using the game id in hex format)"""
        res = self.request("https://xboxapi.com/v2/game-details-hex/{}".format(titleId))
        return res.json()

    # test !!
    #27
    def get_game_details(self, productId):
        """Return the Xbox Game Information (using the product id)"""
        res = self.request("https://xboxapi.com/v2/game-details/{}".format(productId))
        return res.json()

    # test !!
    #28
    def get_game_details_addon(self, productId):
        """Return the Xbox Game Information (using the product id)"""
        res = self.request("https://xboxapi.com/v2/game-details/{}/addons".format(productId))
        return res.json()

    # test !!
    #29
    def get_game_details_related(self, productId):
        """Return the Xbox Game Information (using the product id)"""
        res = self.request("https://xboxapi.com/v2/game-details/{}/related".format(productId))
        return res.json()

    # test !!
    #30
    def get_latest_x360_games(self):
        """Return latest Xbox 360 games from Xbox Live Marketplace"""
        res = self.request("https://xboxapi.com/v2/latest-xbox360-games")
        return res.json()

    # test !!
    #31
    def get_latest_xone_games(self):
        """Return latest Xbox One games from Xbox Live Marketplace"""
        res = self.request("https://xboxapi.com/v2/latest-xboxone-games")
        return res.json()

    # test !!
    #32
    def get_latest_xone_apps(self):
        """Return latest Xbox One Apps from Xbox Live Marketplace"""
        res = self.request("https://xboxapi.com/v2/latest-xboxone-apps")
        return res.json()

    # test !!
    #33
    def get_gold_lounge(self):
        """Return GwG and DwG (Games and Deals with Gold)"""
        res = self.request("https://xboxapi.com/v2/xboxone-gold-lounge")
        return res.json()

    # test !!
    #34
    def get_market_x360_games(self):
        """Return Xbox 360 Games Marketplace"""
        res = self.request("https://xboxapi.com/v2/browse-marketplace/xbox360/1?sort=releaseDate")
        return res.json()

    # test !!
    #35
    def get_market_xone_games(self):
        """Return Xbox One Games Marketplace"""
        res = self.request("https://xboxapi.com/v2/browse-marketplace/games/1?sort=releaseDate")
        return res.json()

    # test !!
    #36
    def get_market_xone_apps(self):
        """Return Xbox One Apps Marketplace"""
        res = self.request("https://xboxapi.com/v2/browse-marketplace/games/1?sort=releaseDate")
        return res.json()

    # test !!
    #37
    def get_activity_feed(self):
        """Return your activity feed"""
        res = self.request("https://xboxapi.com/v2/activity-feed")
        return res.json()

    # test !!
    #38
    def get_titlehub_achievement(self, xuid):
        """Return your achievements list by game with friends who also play. (New TitleHub endpoint)"""
        res = self.request("https://xboxapi.com/v2/{}/titlehub-achievement-list".format(xuid))
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
