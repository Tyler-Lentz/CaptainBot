import discord
from discord.ext import commands
 
class Player:
    def __init__(self, member):
        self.member = member
        self.alive = True
    
    def __str__(self):
        return self.member.nick + f'(Alive: {self.alive})'

players = []

TOKEN = open("token.txt","r").readline()
client = commands.Bot(command_prefix = '>>')

# Answers with the ms latency
@client.command(brief="Checks connection to bot", description = "Returns latency in milliseconds to the bot")
async def ping(ctx):
    await ctx.send(f'Pong! {round (client.latency * 1000)}ms ')

# Reset the player list to current players in voice channel
@client.command(brief="Initializes the game.", \
                description="Sets everybody in the users voice channel as part of the game and mutes everybody")
async def start_game(ctx):
    players.clear()
    await ctx.send("Starting an Among Us game...")
    vc = ctx.author.voice.channel
    for member in vc.members:
        newPlayer = Player(member)
        players.append(newPlayer)
        await member.edit(mute=True)
        await ctx.send("Muted " + member.nick)

# Clear the player list and unmute everybody
@client.command(brief="Ends the game", description="Ends the game and unmutes everybody that is registered in the game")
async def end_game(ctx):
    for player in players:
        await player.member.edit(mute=False)
    players.clear()
    await ctx.send("Game ended")

# Dislpays the status of all the players currently registered in the game 
@client.command(brief="Lists all players", description="Gives a list of all registered players and if they are alive")
async def get_players(ctx):
    print (players)
    if not players:
        await ctx.send("No players currently in the game!")
    for player in players:
        await ctx.send(player)

# Starts a meeting, pass through parameters of people who have died
@client.command(brief="Starts a meeting and unmutes all alive players",\
                description=">>call_meeting arg1 arg2 arg3... where the args are player names that are dead")
async def call_meeting(ctx, *dead):
    for passedName in dead:
        await setDead(ctx, passedName)
    if not dead:
        await ctx.send("Calling a meeting with nobody dead")
    else:
        await ctx.send("Calling a meeting with some dead")
    await unmuteAlive()

# adds a person to the dead list
@client.command(brief="Sets a player as dead", description="Takes one argument which is the name of the dead player")
async def set_dead(ctx, name):
    await setDead(ctx, name)

# Ends a meeting and takes parameter of the person who died (or perhaps DCed)
# if applicable
@client.command(brief="Ends a meeting and mutes all alive players",\
                description=">>end_meeting arg1 arg2 arg3... where the args are player names that are dead")
async def end_meeting(ctx, *dead):
    for passedName in dead:
        await setDead(ctx, passedName)
    if not dead:
        await ctx.send("Ending the meeting with nobody dead")
    else:
        await ctx.send("Ending the meeting with someone dead")
    await muteAll()

# Takes a name that a user inputed as a message and sets that person to dead
# if that person exists
async def setDead(ctx, name):
    initialized = False
    foundPlayer = Player(member=None)
    # Find a person with the passed through name in the player list
    for player in players:
        if (name == player.member.nick):
            foundPlayer = player
            initialized = True
    # Check to see if a person was actually found
    if (initialized):
        foundPlayer.alive = False
        await ctx.send(foundPlayer.member.nick + " is now set to dead")
        await mute(foundPlayer)
    else:
        await ctx.send("ERROR: no player with name " + name)

async def muteAll():
    for player in players:
        await player.member.edit(mute=True)

async def unmuteAlive():
    for player in players:
        if player.alive:
            await player.member.edit(mute=False)

async def mute(player):
    await player.member.edit(mute=True)
 
client.run(TOKEN)
