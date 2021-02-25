import requests
import time
with open("hypixelkey.txt") as file:
    api_key = file.read()

def do_embed(uuid, embed):
    mojangdata = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}").json()
    playername = mojangdata["name"]
    playerdata = requests.get(f"https://api.hypixel.net/player?key={api_key}&name={playername}").json()
    if playerdata["player"]["lastLogin"] > playerdata["player"]["lastLogout"]:
        try:
            recentgame = playerdata["player"]["mostRecentGameType"]
        except KeyError:
            recentgame = "Main Lobby"

        dictionary = {
            "DUELS": "Duels",
            "LEGACY": "Classic Lobby",
            "BEDWARS": "Bedwars",
            "SKYWARS": "Skywars",
            "GINGERBREAD": "TKR",
            "ARCADE": "Arcade Games",
            "BUILD_BATTLE": "Build Battle",
            "MURDER_MYSTERY": "Murder Mystery",
            "PROTOTYPE": "Prototype",
            "PIT": "The Pit",
            "HOUSING": "Housing",
        }

        if recentgame in dictionary:
            recentgame = dictionary[recentgame]
        timeonline = time.time() - playerdata["player"]["lastLogin"]/1000
        minutes = round((timeonline%3600)/60)
        seconds = round(timeonline%60)
        timeonline = round(timeonline/3600-minutes/60)
        #print(f"{timeonline} {minutes} {seconds}")
        if timeonline > 0:
            timeonline = f" {timeonline}h, "
            minutes = f" {minutes}m"
            seconds = ""
        elif minutes > 0:
            timeonline = ""
            minutes = f" {minutes}m, "
            seconds = f"{seconds}s"
        else:
            timeonline = ""
            minutes = ""
            seconds = f" {seconds}s"
        embed.add_field(name=":white_check_mark: "+playername, value=f"{recentgame},  \n     Online for{timeonline}{minutes}{seconds}.", inline=True)
        return True