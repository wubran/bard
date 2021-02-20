from discord.ext import commands
import discord
from concurrent.futures import ThreadPoolExecutor, as_completed
from butter import *
import asyncio
import json
#gaming+
client = commands.Bot(command_prefix="man!")
client.remove_command('help')
with open("hypixelkey.txt") as file:
    api_key = file.read()
with open("bottoken.txt") as file:
    token = file.read()
status = "you"


@client.command(pass_context=True)
async def help(ctx):
    async with ctx.typing():
        author = ctx.message.author
        embed=discord.Embed(title="Bran's Commands:", description="**---------------------------------------------------------**", color=0x97f575)

        embed.add_field(name="help", value='dms u this message \n'
                                           '"man!help here" sends this where you typed it', inline=False)
        embed.add_field(name="helloworld", value="says hello to you", inline=False)
        embed.add_field(name="repeat", value="repeats your message", inline=False)
        embed.add_field(name="say", value="repeats and deletes your message", inline=False)
        embed.add_field(name="doubles", value="the BW doubles wins of the ign provided", inline=False)
        embed.add_field(name="namemc", value="the given ign's NameMc link", inline=False)
        embed.add_field(name="online", value="lists who is online on hypixel \n"
                                             "your ign must be registered to show up on the list\n"
                                             "man!fl also works.", inline=False)
        embed.add_field(name="duel", value="requests to duel the mentioned player in rps. \n"
                                           "don't mention a player to play with anyone. \n"
                                           "man!rps also works.", inline=False)
        embed.add_field(name="duelstats", value="obtains your stats from using the duel command. \n"
                                                "man!stats also works.", inline=False)
        embed.add_field(name="status", value="sets the object in the status of this bot \n"
                                             "please be careful with it", inline=False)
        if str(ctx.message.content)[9:] == "here":
            await ctx.send(embed=embed)
        else:
            await ctx.send("dm sent :D")
            await author.send(embed=embed)

@client.event
async def on_ready():
    global status
    status = "you"
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {status}."))
    print("yes")


async def changestatus():
    await client.wait_until_ready()
    global status
    while 1 == 1: #not client.is_closed():
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {status}."))
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{status}."))
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Game(name=f"with {status}."))
        await asyncio.sleep(5)


@client.command(pass_context=True)
async def status(ctx):
    global status
    status = str(ctx.message.content)[11:]
    await ctx.send(f"status object changed to {status}")


@client.command(pass_context=True)
async def helloworld(ctx):
    async with ctx.typing():
        await ctx.send("heyyy world ;)")
    return


@client.command(pass_context=True)
async def repeat(ctx):
    async with ctx.typing():
        if len(str(ctx.message.content)) > 11:
            message = discord.utils.escape_mentions(str(ctx.message.content)[10:])
            await ctx.send(message)


@client.command(pass_context=True)
async def say(ctx):
    async with ctx.typing():
        if len(str(ctx.message.content)) > 8:
            message = discord.utils.escape_mentions(str(ctx.message.content)[7:])
            await ctx.send(message)
        await ctx.message.delete()


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


'''
@client.command(pass_context=True)
async def recentgame(ctx):
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
    recentgame = data["player"]["mostRecentGameType"]
    await ctx.send(f"{ign}'s most recent game is {recentgame}")
'''


@client.command(pass_context=True, aliases=["fl"])
async def online(ctx):
    async with ctx.typing():
        with open("registered_players.txt") as player_file:
            contents = player_file.read().split()
        embed=discord.Embed(title="Online Players:", description="(current lobby or game)", color=0x97f575)
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/TFgA-LouGUg-cNDEn5waBZkt7kX7iGVzHy0Vjrfm5go/https/hypixel.net/attachments/hypixel-jpg.760131/")

        processes = []
        with ThreadPoolExecutor() as executor:
            for uuid in contents:
                processes.append(executor.submit(do_embed, uuid, embed))
        anyoneonline=False
        for thing in as_completed(processes):
            if thing.result():
                anyoneonline=True
                break
        if anyoneonline==False:
            bedem=discord.Embed(title="Online Players:", description="no one online ;-;", color=0x97f575)
            bedem.set_thumbnail(url="https://images-ext-2.discordapp.net/external/TFgA-LouGUg-cNDEn5waBZkt7kX7iGVzHy0Vjrfm5go/https/hypixel.net/attachments/hypixel-jpg.760131/")
            await ctx.send(embed=bedem)
        else:
            await ctx.send(embed=embed)
    return


games = [] #contains the game message objects
@client.command(pass_context=True, aliases=["rps", "rockpaperscissors", "challenge"])
async def duel(ctx):
    parameters = ctx.message.content.split()
    challenger = ctx.author
    if len(parameters) <= 1:
        await duelnoplayer(ctx, challenger)
        return
    challenged = await client.fetch_user(ctx.message.raw_mentions[0])
    if challenger == challenged:
        await ctx.send("You can't duel yourself!")
        return
    message = await ctx.send(f"<@!{challenger.id}> has challenged <@!{challenged.id}> to a duel of Rock Paper Scissors!  \n They have 30 seconds to confirm!")
    challenge_emojis = ["✅", "🚫"]
    for emoji in challenge_emojis:
        await message.add_reaction(emoji)
    def check(payload):
        return payload.message_id == message.id and str(payload.emoji) in challenge_emojis and payload.user_id == challenged.id
    try:
        variable = await client.wait_for('raw_reaction_add', timeout=30.0, check=check)
        #print(variable.emoji)
        if str(variable.emoji) == "✅":
            await ctx.send(f"The duel has begun! Check your DMS!!! ✅")
        else:
            await ctx.send(f"The duel was denied! 🚫")
            return
    except asyncio.TimeoutError:
        await ctx.send(f"Uh Oh! {str(challenged)[:-5]} didn't respond in time!")
        return

    challenger_message = await challenger.send(f"{challenger} vs {challenged} \n you have 10 seconds to respond")
    challenged_message = await challenged.send(f"{challenger} vs {challenged} \n you have 10 seconds to respond")
    game_messages = [[ctx, challenger, challenged], challenger_message, challenged_message]
    games.append(game_messages)
    emojis = ["🗿", "📝", "✂"]
    for message in game_messages[1:]:
        for emoji in emojis:
            await message.add_reaction(emoji)


async def duelnoplayer(ctx, challenger):
    message = await ctx.send(f"<@!{challenger.id}> is looking for a duel in Rock Paper Scissors! \n"
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
        await ctx.send(f"<@!{accepted.id}> accepted the challenge! Check your DMS!!! ✅")
    except asyncio.TimeoutError:
        await ctx.send(f"Uh Oh! Nobody responded in time!")
        return

    challenger_message = await challenger.send(f"{challenger} vs {accepted} \n you have 10 seconds to respond")
    challenged_message = await accepted.send(f"{challenger} vs {accepted} \n you have 10 seconds to respond")
    game_messages = [[ctx, challenger, accepted], challenger_message, challenged_message]
    games.append(game_messages)
    emojis = ["🗿", "📝", "✂"]
    for message in game_messages[1:]:
        for emoji in emojis:
            await message.add_reaction(emoji)


@client.event
async def on_raw_reaction_add(payload):
    emojis = ["🗿", "📝", "✂"]
    emojinames = ["rock", "paper", "scissors"]
    winningcases = ["paperrock", "rockscissors", "scissorspaper"]
    for game in games:
        for message in game[1:]:
            if message not in emojinames and payload.message_id == message.id and str(payload.emoji) in emojis and payload.user_id != 811435588942692352:
                for thing in range(len(game[1:])):
                    try:
                        if game[thing+1].id == payload.message_id:
                            game[thing+1] = emojinames[emojis.index(str(payload.emoji))]
                    except AttributeError:
                        pass
                if game[1] in emojinames and game[2] in emojinames:
                    with open("rockpaperscissorstats.json") as in_file:
                        stats = json.load(in_file)
                    if str(game[0][1].id) not in stats:
                        stats[str(game[0][1].id)] = {"wins": 0, "ties": 0, "losses": 0, "rock": 0, "paper": 0, "scissors": 0}
                    if str(game[0][2].id) not in stats:
                        stats[str(game[0][2].id)] = {"wins": 0, "ties": 0, "losses": 0, "rock": 0, "paper": 0, "scissors": 0}
                    stats[str(game[0][1].id)][game[1]] += 1
                    stats[str(game[0][2].id)][game[2]] += 1
                    if game[1] == game[2]:
                        who_won = f"<@!{game[0][1].id}> and <@!{game[0][2].id}> tied in their duel {emojis[emojinames.index(game[1])]}!"
                        stats[str(game[0][1].id)]["ties"] += 1
                        stats[str(game[0][2].id)]["ties"] += 1
                    elif game[1] + game[2] in winningcases:
                        who_won = f"<@!{game[0][1].id}> {emojis[emojinames.index(game[1])]} won the duel against <@!{game[0][2].id}> {emojis[emojinames.index(game[2])]}!"
                        stats[str(game[0][1].id)]["wins"] += 1
                        stats[str(game[0][2].id)]["losses"] += 1
                    else:
                        who_won = f"<@!{game[0][2].id}> {emojis[emojinames.index(game[2])]} won the duel against <@!{game[0][1].id}> {emojis[emojinames.index(game[1])]}!"
                        stats[str(game[0][1].id)]["losses"] += 1
                        stats[str(game[0][2].id)]["wins"] += 1
                    await game[0][0].send(who_won)
                    with open("rockpaperscissorstats.json", "w") as out_file:
                        json.dump(stats, out_file, indent=4)


@client.command(pass_context=True, aliases=["rpsstats", "stats"])
async def duelstats(ctx):
    async with ctx.typing():
        if len(ctx.message.raw_mentions) == 0:
            await ctx.send("Whose stats do you want?")
            return
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


client.loop.create_task(changestatus())
client.run(token)
