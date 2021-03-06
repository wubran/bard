from discord.ext import commands, tasks
import discord
from concurrent.futures import ThreadPoolExecutor, as_completed
from butter import *
import asyncio
import json
from time import *
import random
from connectfour import *

#gaming
client = commands.Bot(command_prefix="b!")
client.remove_command('help')
with open("hypixelkey.txt") as file:
    api_key = file.read()
with open("bottoken.txt") as file:
    token = file.read()
with open("status.txt") as file:
    status = file.read()[1:-1]
#botsthots 806611882252566548
games = [] #contains the game message objects


@client.command(pass_context=True)
async def help(ctx):
    async with ctx.typing():
        author = ctx.message.author
        embed = discord.Embed(title="Bran's b! Commands: (bard #9171)", description=f"**{94*'-'}**", color=0x97f575)

        embed.add_field(name="help  :question:", value='dms u this message \n'
                                                       '"b!help here" sends this where you typed it', inline=True)
        embed.add_field(name="hello  :wave:", value="says hello to you\n"
                                                    ";D hehe\nbard's first command", inline=True)
        embed.add_field(name="simp  :pleading_face: :point_right: :point_left:",
                        value="be a simp for the mentioned user. \n"
                              "b!dream", inline=True)

        embed.add_field(name="repeat  :loud_sound:", value="repeats your message \n (same channel)", inline=True)
        embed.add_field(name="say  :mute:", value="repeats and deletes your message (same channel)", inline=True)
        embed.add_field(name="jeneral  :loudspeaker:", value="repeats your message in jeneral", inline=True)

        embed.add_field(name="online  :white_check_mark:", value="lists who (registered) is online on hypixel \n"
                                                                 "b!fl also works.", inline=True)
        embed.add_field(name="doubles  :crossed_swords:", value="states the total BW doubles wins \n"
                                                                "of the ign provided\n", inline=True)
        embed.add_field(name="namemc  :eyes:", value="sends the the given ign's NameMc link \n(same channel)", inline=True)

        embed.add_field(name="duel  :moyai: :pencil:  :scissors:", value="requests to RPS anyone. \n"
                                                                         "you can also mention someone specific. \n"
                                                                         , inline=True)
        embed.add_field(name="duelstats  :muscle:", value="obtains your stats from using the duel command. \n"
                                                          "b!stats also works.", inline=True)
        embed.add_field(name=":point_left: (description)", value="RPS stands for rock paper scissors. \n"
                                                                 "Prepare for the bot's DM.", inline=True)

        embed.add_field(name="birth  :cake:", value="log your birthday in the bot (mm/dd/yyyy). \n"
                                                    "wait for a surprise ;)", inline=True)
        embed.add_field(name="birthdays  :tada:", value="lists all registered birthdays in the bot. \n"
                                                        "register with b!birth", inline=True)
        embed.add_field(name="nextbirth  :cupcake:", value="get the closest next birthday that is \n"
                                                           "registered in the bot.", inline=True)

        embed.add_field(name="status  :thumbsup:", value="sets the object in the status of this bot \n"
                                                         "~~please be careful with it~~", inline=True)
        embed.add_field(name="data  :pencil2:", value="store some data in the bot \n"
                                                      "b!data (categories>) (carrots seperating) data", inline=True)
        embed.add_field(name="get  :mag_right:", value="be a simp for the mentioned user. \n"
                                                       "b!mem also works", inline=True)
        if str(ctx.message.content)[7:] == "here":
            await ctx.send(embed=embed)
        else:
            await ctx.send("dm sent :D")
            await author.send(embed=embed)


@client.event
async def on_ready():
    global status
    global jeneral
    with open("status.txt") as file:
        status = file.read()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {status}."))
    jeneral = await client.fetch_channel(748241629747347559)
    print(f"bot started {strftime('%I:%M %p, %m/%d', localtime())}")  # use %c for a full, pre-made date


async def theloop():
    await client.wait_until_ready()
    global status
    while not client.is_closed():
        await client.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"over {status}."))
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Activity(
            type=discord.ActivityType.listening, name=f"{status}."))
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Game(name=f"with {status}."))
        await asyncio.sleep(5)
        with open("last_daily.txt") as file:
            lastday = file.read()
            nowday = localtime().tm_mday
        if not int(lastday) == int(nowday):
            with open("last_daily.txt", "w") as out_file:
                out_file.write(str(nowday))
            with open("birthdays.json") as in_file:
                filedata = json.load(in_file)
            if int(localtime().tm_mon) in filedata["month"] and int(localtime().tm_mday) in filedata["month"]:
                await jeneral.send("gm :D")
                for each in range(len(filedata["author"])):
                    if filedata["month"][each] == int(localtime().tm_mon) and filedata["day"][each] == int(localtime().tm_mday):
                        age = int(localtime().tm_year)-filedata["year"][each]
                        ones = age%10
                        if ones > 2 or ones == 0:
                            age = str(age) + "th"
                        elif ones == 2:
                            age = str(age) + "nd"
                        elif ones == 1:
                            age = str(age) + "st"
                        name = await client.fetch_user(filedata['author'][each])
                        name = name.mention
                        await jeneral.send(f"IT'S {name}'S "
                                       f"{age} BIRTHDAYYY")


@client.command(pass_context=True)
async def status(ctx):
    global status
    status = str(ctx.message.content)[9:]
    with open("status.txt", "w") as out_file:
        out_file.write(status)
    await ctx.send(f"status object changed to {status}")


@client.command(pass_context=True)
async def birthdays(ctx):
    with open("birthdays.json") as in_file:
        filedata = json.load(in_file)
    embed = discord.Embed(title="Registered Birthdays:", description=f"**{94 * '-'}**", color=0x97f575)
    for each in range(len(filedata["author"])):
        if filedata["month"][each] == 12 or filedata["month"][each] <= 2:
            emoji = "❄️"
        elif filedata["month"][each] <= 5:
            emoji = "🌱️"
        elif filedata["month"][each] <= 8:
            emoji = "☀️"
        else:
            emoji = "🍂"
        embed.add_field(name=f"{emoji} {await client.fetch_user(filedata['author'][each])}",
                        value=f'{filedata["month"][each]}/{filedata["day"][each]}/{filedata["year"][each]}', inline=True)
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def birth(ctx):
    msgdata = str(ctx.message.content)[8:]
    validdays = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    try:
        author = await client.fetch_user(ctx.message.raw_mentions[0])
        author = author.id
    except IndexError:
        author = ctx.author.id
    try:
        month = int(msgdata.split("/")[0])
        day = int(msgdata.split("/")[1])
        year = int(msgdata.split("/")[2].split()[0])
        if month > 12:
            await ctx.send("this is not a valid month.")
            return
        if day > validdays[month] and not year % 4 == 0 and not month == 2 and not day == 29:
            await ctx.send("this is not a valid day.")
            return
        if year < 1000:
            await ctx.send("four digit year pls ;)")
            return
        if year < 2000:
            await ctx.send("ok smol")
            return
    except IndexError:
        await ctx.send("provide a valid birthday (mm/dd/yyyy)")
        return
    except ValueError:
        await ctx.send("provide a valid birthday (mm/dd/yyyy)")
        return

    with open("birthdays.json") as in_file:
        filedata = json.load(in_file)

    if author not in filedata["author"]:
        filedata["month"].append(month)
        filedata["day"].append(day)
        filedata["year"].append(year)
        filedata["author"].append(author)
    else:
        ind = filedata["author"].index(author)
        filedata["month"][ind] = month
        filedata["day"][ind] = day
        filedata["year"][ind] = year

    with open("birthdays.json", "w") as out_file:
        json.dump(filedata, out_file, indent=4)
    await ctx.send("birthday saved :D")


@client.command(pass_context=True)
async def nextbirth(ctx): # assumes no twins
    with open("birthdays.json") as in_file:
        filedata = json.load(in_file)
    validdays = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    daysaway = []
    today = int(localtime().tm_yday)
    for entry in range(len(filedata["month"])):
        yeardate = 0
        for month in range(filedata["month"][entry]):
            if not month == 0:
                yeardate = yeardate + validdays[month]
        daysaway.append(yeardate + filedata["day"][entry] - today)
    beforesort = []
    for number in daysaway:
        beforesort.append(number)
    daysaway.sort()
    for boop in daysaway:
        if boop >= 0:
            ind = beforesort.index(boop)
            age = int(localtime().tm_year) - filedata["year"][ind]
            name = await client.fetch_user(filedata['author'][ind])
            name = str(name)[:-5]
            await ctx.send(f'The next registered birthday is:\n{name} (turning {age}) on '
                           f'{filedata["month"][ind]}/{filedata["day"][ind]}/{filedata["year"][ind]}')
            break


@client.command(pass_context=True, aliases=["give", "push"])
async def data(ctx):
    msgdata = str(ctx.message.content)[7:].split(">")
    if len(msgdata) >= 4:
        await ctx.send("3 is the maximum number of layers")
        return
    perameter = msgdata[-1]
    perameter = perameter[len(perameter.split(" ")[0])+1:]
    msgdata[-1] = msgdata[-1][:-(1+len(perameter))]

    with open("data.json") as in_file:
        filedata = json.load(in_file)
    if len(msgdata) == 3:
        if msgdata[0] not in filedata:
            filedata[msgdata[0]] = {msgdata[1]: {msgdata[2]: perameter}}
        elif msgdata[1] not in filedata[msgdata[0]]:
            filedata[msgdata[0]][msgdata[1]] = {msgdata[2]: perameter}
        else:
            filedata[msgdata[0]][msgdata[1]][msgdata[2]] = perameter
    elif len(msgdata) == 2:
        if msgdata[0] not in filedata:
            filedata[msgdata[0]] = {msgdata[1]: perameter}
        elif msgdata[1] not in filedata[msgdata[0]]:
            filedata[msgdata[0]][msgdata[1]] = perameter
    elif len(msgdata) == 1:
        filedata[msgdata[0]] = perameter

    with open("data.json", "w") as out_file:
        json.dump(filedata, out_file, indent=4)
    await ctx.send(f"data stored.")


@client.command(pass_context=True, aliases=["mem"])
async def get(ctx):
    msgdata = str(ctx.message.content)[6:].split(">")
    if len(msgdata) >= 4:
        await ctx.send("3 is the maximum number of layers")
        return
    elif msgdata[0] == "":
        await ctx.send("provide a category (or two) and a name separated by >'s to pull from my memory.")
        return

    with open("data.json") as in_file:
        filedata = json.load(in_file)
    if len(msgdata) == 3:
        await ctx.send(str(filedata[msgdata[0]][msgdata[1]][msgdata[2]]).replace("{", "{\n    ").replace("}", "\n}    "))
    elif len(msgdata) == 2:
        await ctx.send(str(filedata[msgdata[0]][msgdata[1]]).replace("{", "{\n    ").replace("}", "\n}    "))
    elif len(msgdata) == 1:
        await ctx.send(str(filedata[msgdata[0]]).replace("{", "{\n    ").replace("}", "\n}    "))


@client.command(pass_context=True, aliases=["dream"])
async def simp(ctx):
    async with ctx.typing():
        dream = str(ctx.message.content)[7:].upper()
        if len(dream) > 0:
            await ctx.send(f"{dream}‼️{dream}‼️ Hello 😀👋🏻 do your shoes need shining? 🤔👟✨ \n"
                           f"{dream}😳‼️{dream} please 🥺☹️🙏 Should you need coffee? 👀☕️ \n"
                           f"Come back 😫 PLEASE my clout 😤🤑 Dont go away from me 🥺\n{dream} Please 😫😫🤨")


@client.command(pass_context=True)
async def hello(ctx):
    async with ctx.typing():
        await ctx.send("heyyy world ;)")
    return


@client.command(pass_context=True)
async def repeat(ctx):
    async with ctx.typing():
        if len(str(ctx.message.content)) > 9:
            if ctx.message.mention_everyone:
                message = discord.utils.escape_mentions(str(ctx.message.content)[8:])
            else:
                message = str(ctx.message.content)[8:]
            await ctx.send(message)


@client.command(pass_context=True)
async def say(ctx):
    async with ctx.typing():
        if len(str(ctx.message.content)) > 6:
            if ctx.message.mention_everyone:
                message = discord.utils.escape_mentions(str(ctx.message.content)[5:])
            else:
                message = str(ctx.message.content)[5:]
            await ctx.send(message)
        await ctx.message.delete()


@client.command(pass_context=True)
async def jeneral(ctx):
    async with ctx.typing():
        if len(str(ctx.message.content)) > 9:
            if ctx.message.mention_everyone:
                message = discord.utils.escape_mentions(str(ctx.message.content)[10:])
            else:
                message = str(ctx.message.content)[10:]
            await jeneral.send(message)


@client.command(pass_context=True)
async def doubles(ctx):
    async with ctx.typing():
        parameters = ctx.message.content.split()
        if len(parameters) <= 1:
            await ctx.send("give ign :)")
            return
        player = parameters[1]
        data = requests.get(f"https://api.hypixel.net/player?key={api_key}&name={player}").json()
        if data["player"] is None:
            await ctx.send("ign bad")
            return
        ign = data["player"]["displayname"]
        try:
            whatiwant = data["player"]["stats"]["Bedwars"]["eight_two_wins_bedwars"]
        except KeyError:
            whatiwant = f"{ign} has no stats in that game"
        if whatiwant == 1:
            plural = ""
        else:
            plural = "s"
        await ctx.send(f"{ign} has {whatiwant} win{plural} in doubles bedwars")
    return


@client.command(pass_context=True)
async def namemc(ctx):
    async with ctx.typing():
        parameters = ctx.message.content.split()
        if len(parameters) <= 1:
            await ctx.send("give ign :)")
            return
        await ctx.send(f"https://namemc.com/profile/{parameters[1]}")
    return


@client.command(pass_context=True, aliases=["fl"])
async def online(ctx):
    async with ctx.typing():
        with open("registered_players.txt") as player_file:
            contents = player_file.read().split()
        embed=discord.Embed(title="Online Players:", description="(current lobby or game)", color=0x97f575)
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/TFgA-LouGUg-"
                                "cNDEn5waBZkt7kX7iGVzHy0Vjrfm5go/https/hypixel.net/attachments/hypixel-jpg.760131/")

        processes = []
        with ThreadPoolExecutor() as executor:
            for uuid in contents:
                processes.append(executor.submit(do_embed, uuid, embed))
        anyoneonline = False
        for thing in as_completed(processes):
            if thing.result():
                anyoneonline=True
                break
        if anyoneonline == False:
            bedem=discord.Embed(title="Online Players:", description="no one online ;-;", color=0x97f575)
            bedem.set_thumbnail(url="https://images-ext-2.discordapp.net/external/TFgA-LouGUg-"
                                    "cNDEn5waBZkt7kX7iGVzHy0Vjrfm5go/https/hypixel.net/attachments/hypixel-jpg.760131/")
            await ctx.send(embed=bedem)
        else:
            await ctx.send(embed=embed)
    return


@client.command(pass_context=True, aliases=["duel"])
async def rps(ctx):
    result = await duelstart(ctx, "Rock Paper Scissors")
    if result == 0:
        return
    challenger = result[0]
    challenged = result[1]
    await ctx.send(f"{challenged} accepted the duel! Check your dms!")
    challenger_message = await challenger.send(f"{challenger} vs {challenged} \n you have 10 seconds to respond")
    challenged_message = await challenged.send(f"{challenger} vs {challenged} \n you have 10 seconds to respond")
    game_messages = [[ctx, challenger, challenged, "rps"], challenger_message, challenged_message]
    games.append(game_messages)
    emojis = ["🗿", "📝", "✂"]
    for message in game_messages[1:]:
        for emoji in emojis:
            await message.add_reaction(emoji)


@client.command(pass_context=True, aliases=["c4"])
async def connect4(ctx):
    note = ""
    splitted = ctx.message.content.split()
    if len(splitted) > 1:
        ignorelol = splitted[1]
    else:
        ignorelol = ""
    if len(splitted) == 4:
        columns = splitted[2]
        rows = splitted[3]
    elif len(splitted) <= 2:
        columns = 7
        rows = 6
    elif len(splitted) > 4:
        await ctx.send("...what\nb!c4 <mention someone (or leave empty)> <length> <height>")
        return
    elif len(splitted) == 3:
        columns = splitted[2]
        rows = 6
    else:
        await ctx.send("...what\nb!c4 <mention someone (or leave empty)> <length> <height>")
        return

    print(f"ignore: {ignorelol}")
    if str(columns).isdigit() and str(rows).isdigit():
        columns = int(columns)
        rows = int(rows)
    else:
        await ctx.send("...what\nb!c4 <mention someone (or leave empty)> <length> <height>")
        return
    try:
        ignorelol = int(ignorelol)
        print("wrongtype")
        if len(splitted) == 3 and type(columns) is int:
            rows = columns
            columns = ignorelol
        elif len(splitted) == 2:
            columns = ignorelol
    except ValueError:
        pass

    else:
        ignorelol = ""
    if columns < 4:
        columns = 4
        note = "4 is the minimum number of rows/columns\n"
    elif columns > 9:
        columns = 9
        note = "9 is the maximum number of columns\n"
    if rows < 4:
        rows = 4
        note = "4 is the minimum number of rows/columns\n"
    elif rows > 30:
        rows = 30
        note = "30 is the maximum number of rows\n"
    print(f"columns: {columns}, rows: {rows}")
    result = await duelstart(ctx, f"Connect 4 ({columns}x{rows})")
    if result == 0:
        return
    if random.randint(0, 1) == 0:
        p1 = result[0]
        p2 = result[1]
        turn = 0
    else:
        p1 = result[1]
        p2 = result[0]
        turn = 0
    player1 = str(p1)[:-5]
    player2 = str(p2)[:-5]
    thegame = ConnectGame(columns, rows)
    await ctx.send(f"{note}The game has begun! P1: {player1} 🔴, P2: {player2} 🔵")
    rowids = []
    rowsleft = rows
    realrowids = []
    while rowsleft > 0:
        message = await ctx.send(thegame.formatrow(rowsleft))
        rowids.append(message)
        realrowids.append(message.id)
        if 3 >= rowsleft >= 1:
            leftovers = rowsleft
        rowsleft -= 3
        #sleep(0.2)
    infomessage = await ctx.send(f"{player1} goes first!")
    rowids.reverse()
    realrowids.reverse()
    emojis = ["✅", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    for emoji in range(columns+1):
        await message.add_reaction(emojis[emoji])
    tops = [0]*columns
    x = 0
    y = 0
    new = False
    game_messages = [[ctx, p1, p2, "c4", message, infomessage], x, y, turn, thegame, tops, new, rowids, leftovers, realrowids]
    games.append(game_messages)


@client.event
async def on_raw_reaction_add(payload):
    for game in games:
        if game[0][3] == "rps":
            await rpsgame(payload, game)
        elif game[0][3] == "c4":
            await c4game(payload, game)


async def rpsgame(payload, game):
    rpsemojis = ["🗿", "📝", "✂"]
    emojinames = ["rock", "paper", "scissors"]
    winningcases = ["paperrock", "rockscissors", "scissorspaper"]
    for message in game[1:]:
        if message not in emojinames and payload.message_id == message.id and str(payload.emoji) in rpsemojis \
                and payload.user_id != 811435588942692352:
            for thing in range(len(game[1:])):
                try:
                    if game[thing+1].id == payload.message_id:
                        game[thing+1] = emojinames[rpsemojis.index(str(payload.emoji))]
                except AttributeError:
                    pass
            if game[1] in emojinames and game[2] in emojinames:
                with open("rockpaperscissorstats.json") as in_file:
                    stats = json.load(in_file)
                if str(game[0][1].id) not in stats:
                    stats[str(game[0][1].id)] = {"wins": 0, "ties": 0, "losses": 0,
                                                 "rock": 0, "paper": 0, "scissors": 0}
                if str(game[0][2].id) not in stats:
                    stats[str(game[0][2].id)] = {"wins": 0, "ties": 0, "losses": 0,
                                                 "rock": 0, "paper": 0, "scissors": 0}
                stats[str(game[0][1].id)][game[1]] += 1
                stats[str(game[0][2].id)][game[2]] += 1
                if game[1] == game[2]:
                    who_won = f"<@!{game[0][1].id}> and <@!{game[0][2].id}> tied " \
                              f"in their duel {rpsemojis[emojinames.index(game[1])]}!"
                    stats[str(game[0][1].id)]["ties"] += 1
                    stats[str(game[0][2].id)]["ties"] += 1
                elif game[1] + game[2] in winningcases:
                    who_won = f"<@!{game[0][1].id}> {rpsemojis[emojinames.index(game[1])]} won the duel against " \
                              f"<@!{game[0][2].id}> {rpsemojis[emojinames.index(game[2])]}!"
                    stats[str(game[0][1].id)]["wins"] += 1
                    stats[str(game[0][2].id)]["losses"] += 1
                else:
                    who_won = f"<@!{game[0][2].id}> {rpsemojis[emojinames.index(game[2])]} won the duel against " \
                              f"<@!{game[0][1].id}> {rpsemojis[emojinames.index(game[1])]}!"
                    stats[str(game[0][1].id)]["losses"] += 1
                    stats[str(game[0][2].id)]["wins"] += 1
                await game[0][0].send(who_won)
                with open("rockpaperscissorstats.json", "w") as out_file:
                    json.dump(stats, out_file, indent=4)


async def c4game(payload, game):
    c4emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]  #✅
    message = game[0][4]
    thegame = game[4]
    '''if client.is_ws_ratelimited():
        print("lag!")'''
    if payload.message_id in game[9]:
        if payload.message_id == message.id:
            if payload.user_id == game[0][1 + game[3]].id:
                if str(payload.emoji) in c4emojis:
                    await game[0][5].edit(content=f"{await client.fetch_user(payload.user_id)} selected {payload.emoji}. Check to confirm.")
                    if thegame.array[game[2]][game[1]] == 3:
                        thegame.array[game[2]][game[1]] = 0
                    game[1] = c4emojis.index(str(payload.emoji))
                    game[2] = game[5][game[1]]
                    game[6] = True

                    thegame.array[game[2]][game[1]] = 3
                    rowid = round((game[2] - game[8]) / 3 - .4)
                    if rowid < 0:
                         rowid = -1
                    await game[7][rowid+1].edit(content=thegame.formatrow(game[8]+3*(rowid+1)))

                elif str(payload.emoji) == "✅" and game[6]:
                    thegame.array[game[2]][game[1]] = 1+game[3]
                    game[5][game[1]] = game[2]+1
                    rowid = round((game[2] - game[8]) / 3 - .4)
                    if rowid < 0:
                         rowid = -1
                    await game[7][rowid+1].edit(content=thegame.formatrow(game[8]+3*(rowid+1)))
                    game[6] = False
                    if thegame.checkforwin(game[1], game[2], 1+game[3]):
                        print("PLAYER WON")
                    if game[3]:
                        game[3] = 0
                    else:
                        game[3] = 1
                    await game[0][5].edit(content=f"It is now {str(game[0][1 + game[3]])}'s turn")
            if not payload.user_id == 811435588942692352:
                await message.remove_reaction(payload.emoji, await client.fetch_user(payload.user_id))
        else:
            await game[7][game[9].index(payload.message_id)].clear_reactions()
    # game_messages = [[ctx, p1, p2, "c4", message, infomessage], x, y, turn, thegame, tops, new, rowids, rows]


@client.command(pass_context=True, aliases=["rpsstats", "stats"])
async def duelstats(ctx):
    async with ctx.typing():
        if len(ctx.message.raw_mentions) == 0:
            player = ctx.message.author
        else:
            player = await client.fetch_user(ctx.message.raw_mentions[0])
        with open("rockpaperscissorstats.json") as in_file:
            stats = json.load(in_file)
        try:
            stats = stats[str(player.id)]
        except KeyError:
            await ctx.send("This player has no stats!")
            return
        games = stats['wins'] + stats['losses'] + stats['ties']
        statgames = stats['rock'] + stats['paper'] + stats['scissors']
        statmessage = f"<@!{player.id}>'s 🗿📝✂ stats:\n" \
                      f"They have played {games} total games.\n \n" \
                      f"Wins: {stats['wins']} ({round(100*stats['wins']/games)}%)\n" \
                      f"Ties: {stats['ties']} ({round(100*stats['ties']/games)}%)\n" \
                      f"Losses: {stats['losses']} ({round(100 * stats['losses']/games)}%)\n \n" \
                      f"Rocks: {stats['rock']} ({round(100*stats['rock']/statgames)}%)\n" \
                      f"Papers: {stats['paper']} ({round(100*stats['paper']/statgames)}%)\n" \
                      f"Scissors: {stats['scissors']} ({round(100*stats['scissors']/statgames)}%)\n"
        await ctx.send(statmessage)


async def duelstart(ctx, game):
    parameters = ctx.message.content.split()
    challenger = ctx.author
    if len(parameters) <= 1:
        return await duelnoplayer(ctx, challenger, game)
    try:
        challenged = await client.fetch_user(ctx.message.raw_mentions[0])
    except IndexError:
        return await duelnoplayer(ctx, challenger, game)
    if challenger == challenged:
        # await ctx.send("You can't duel yourself!")
        # return 0
        pass
    message = await ctx.send(f"<@!{challenger.id}> has challenged <@!{challenged.id}> "
                             f"to a duel of **{game}**!  \n They have 30 seconds to confirm!")
    challenge_emojis = ["✅", "🚫"]
    for emoji in challenge_emojis:
        await message.add_reaction(emoji)

    def check(payload):
        return payload.message_id == message.id and str(payload.emoji) in challenge_emojis \
               and payload.user_id == challenged.id

    try:
        variable = await client.wait_for('raw_reaction_add', timeout=30.0, check=check)
        # print(variable.emoji)
        if str(variable.emoji) == "✅":
            #await ctx.send(f"The duel has begun! ✅")
            pass
        else:
            await ctx.send(f"The duel was denied! 🚫")
            return 0
    except asyncio.TimeoutError:
        await ctx.send(f"Uh Oh! {str(challenged)[:-5]} didn't respond in time!")
        return 0
    return [challenger, challenged]


async def duelnoplayer(ctx, challenger, game):
    message = await ctx.send(f"<@!{challenger.id}> is looking for a duel in {game}! \n"
                             f"There are 30 seconds left for someone to respond!")
    await message.add_reaction("✅")
    global accepted
    def check(payload):
        global accepted
        accepted = payload.user_id
        return payload.message_id == message.id and str(
            payload.emoji) == "✅" and not payload.user_id in {811435588942692352, challenger.id}

    try:
        await client.wait_for('raw_reaction_add', timeout=30.0, check=check)
        accepted = await client.fetch_user(accepted)
        #await ctx.send(f"<@!{accepted.id}> accepted the challenge! ✅")
    except asyncio.TimeoutError:
        await ctx.send(f"Uh Oh! Nobody responded in time!")
        return 0
    return [challenger, accepted]


client.loop.create_task(theloop())
client.run(token)
