# https://discordpy.readthedocs.io/en/stable/ext/commands/index.html
# https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be

import os
import discord
import json 
from utils.common import *
from voice_generator.common import *
from discord.ext import commands
from discord.utils import get
from discord.ext.commands.errors import CommandNotFound, ExpectedClosingQuoteError

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DEBUG_CHANNEL_ID = 1212207389793714266 # MUST BE AN INT
DEBUG_MODE = False

# set up bot with prefix and permissions 
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

#################################################
#####           ON EVENT BEHAVIOR           #####
#################################################

@bot.event
async def on_ready():
    global debug_channel
    debug_channel = bot.get_channel(DEBUG_CHANNEL_ID)
    await debug_channel.send("AI Voice Bot is ready for action! This is my debug channel. Use !debug to turn on debug mode.")
    await debug_channel.send(init_str)

@bot.event
async def on_command_error(ctx, error):
    
    caller = ctx.message.author.id
    caller_text_channel = ctx.message.channel
    debug_list = [f"Caller was {caller} from {caller_text_channel}"]

    if isinstance(error, CommandNotFound):
        await caller_text_channel.send(uwu(f"<@{caller}> it looks like the command you sent wasn't a valid one! Try using !help to see a list of commands."))
    elif isinstance(error, ExpectedClosingQuoteError):
        await caller_text_channel.send(uwu(f"<@{caller}> it looks like you forgot a closing double quotes! Be sure to wrap all your text in double quotes. :grin:"))
    else:
        await caller_text_channel.send(uwu(f"<@{caller}> I don't know what broke but here is the error message:\n ```{error}```"))

#################################################
#####           START OF COMMANDS           #####
#################################################

### CONNECT ###
@bot.command(name='connect', aliases=['summon','join'], description="Connects bot to voice channel of the command author")
async def _connect(ctx):
    
    caller = ctx.message.author.id
    caller_text_channel = ctx.message.channel
    debug_list = [f"Caller was {caller} from {caller_text_channel}"]

    try:
        caller_voice_channel = ctx.message.author.voice.channel
        debug_list.append(f"Caller voice channel was {caller_voice_channel}")
    except:
        await caller_text_channel.send(uwu(f"Are you sure you're in a voice channel? <@{caller}>"))

    try:
        is_already_connected = get(ctx.bot.voice_clients, guild=ctx.guild).is_connected()
        debug_list.append(f"Connected status was {is_already_connected}")
    except:
        is_already_connected = False
        debug_list.append(f"Voice connected status could not be fetched, forced to {is_already_connected}")

    if is_already_connected:
        await caller_text_channel.send("I am already connected! Disconnect me first and then reconnect me to move me to a new channel")
        debug_list.append("Bot was already connected, could not move channels")
    else:
        await caller_voice_channel.connect()

    if DEBUG_MODE:
        await debug_channel.send(debug_formatter(debug_list, "connect"))

### DISCONNECT ###
@bot.command(name='disconnect', aliases=['leave','fuckoff'], description="Disconnects bot from any voice channel it is currently in")
async def _disconnect(ctx):

    caller = ctx.message.author.id
    caller_text_channel = ctx.message.channel
    debug_list = [f"Caller was {caller} from {caller_text_channel}"]

    try:
        is_already_connected = get(ctx.bot.voice_clients, guild=ctx.guild).is_connected()
        debug_list.append(f"Voice channel connection status is {is_already_connected}")
    except Exception as e:
        is_already_connected = False
        await caller_text_channel.send(uwu("I can't get my voice channel connection status; try restarting me."))
        debug_list.append(f"Disconnect request recieved but errored out with {repr(e)}")
    
    if DEBUG_MODE:
        await debug_channel.send(debug_formatter(debug_list, "disconnect"))

    if is_already_connected:
        await ctx.voice_client.disconnect()

### GENERATE ###
@bot.command(name='generate', aliases=['speak'], description='Generates audio of the specified text in the specified voice')
async def _generate(
    ctx, 
    request_voice: str = commands.parameter(default="spongebob", description="The voice to be used to generate audio"), 
    request_text: str = commands.parameter(default="It looks like you forgot to include text to generate audio of, you silly goose!", description="Text to generate audio of")
):

    caller = ctx.message.author.id
    caller_text_channel = ctx.message.channel
    caller_voice_channel = ctx.message.author.voice.channel
    request_voice = request_voice.lower()
    debug_list = [f"Caller was {caller} from {caller_text_channel}", f"Trying to generate text with {request_voice}"]
    debug_list.append(f"Request text: {request_text}")

    #Step 1: If the user is not in a voice channel, send them a message telling them so
    if caller_voice_channel is None:
        await caller_text_channel.send(uwu(f"<@{caller}> you're not in a voice channel silly! I can't generate audio for you if you're not in a voice channel."))

    #Step 2: Try and generate the audio file we are going to play
    #TODO: Program behaviors based off exception type
    try:
        output_dict = generate_and_save(input_text = request_text, request_voice = request_voice, requester=caller)
        debug_list.append(output_dict['debug-string'])
    except KeyError:
        await caller_text_channel.send(uwu(f"Sorry! I couldn't generate your audio for you because {request_voice} is not a voice I know yet; use !list_voices to see which ones I know!"))
    except Exception as e:
        await caller_text_channel.send(uwu(f"Sorry! I couldn't generate the audio for you but I'm not sure why. Use the !debug command to turn on debug mode and get more details."))
        debug_list.append(f"Saving audio failed because of: {repr(e)}")

    #Step 3a: try and fetch the bots current connection status
    #I think the get().is_connect() should tell us if the bot is connected to ANY voice channel in the given server
    try:
        is_already_connected = get(ctx.bot.voice_clients, guild=ctx.guild).is_connected()
        debug_list.append(f"Connected status was {is_already_connected}")
    except:
        is_already_connected = False
        debug_list.append(f"Voice connected status could not be fetched, forced to {is_already_connected}")

    # Step 3b: if the bot is not connected, try to connect it to the VC
    if not is_already_connected:
        try:
            await caller_voice_channel.connect()
            debug_list.append(f"Connected to {caller_voice_channel} by {caller}")
        except Exception as e:
            await caller_text_channel.send(uwu(f"<@{caller}> I tried to automatically join your channel but failed :sob: can you try using the !connect command to get me into your voice channel?"))
            debug_list.append(f"Failed to join voice at {caller_voice_channel} with error: {repr(e)}")

    # Step 4: play audio
    try:
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        audio_source = discord.FFmpegPCMAudio(output_dict['full-path'])
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
    except Exception as e:
        await caller_text_channel.send(uwu(f"<@{caller}> Sorry! It looks like I was able to generate your audio but not play it. Try turning on debug mode using !debug to get more details."))
        debug_list.append(f"Failed to play audio with error: {repr(e)}")

    if DEBUG_MODE:
        await debug_channel.send(debug_formatter(debug_list, "generate"))

### LIST VOICES ###
@bot.command(name='list_voices', aliases=['listvoices','all_voices','allvoices', 'what_voices', 'whatvoices'], description='Lists all of the available voices to generate audio with')
async def _list_voices(ctx):

    caller = ctx.message.author.id
    caller_text_channel = ctx.message.channel
    debug_list = [f"Caller was {caller} from {caller_text_channel}"]
    
    print_str = "```\nA list of currently available voices:\n"
    for _voice in voice_mappings.keys():
        print_str += f"  - {voice_mappings[_voice]['full-name']} ({_voice}) : {voice_mappings[_voice]['description']}\n"
    print_str += "```"

    await caller_text_channel.send(print_str)

    if DEBUG_MODE:
        await debug_channel.send(debug_formatter(debug_list, "list_voices"))

### DEBUG MODE ### 
@bot.command(name='debug', aliases=['debug_mode','debugmode','uwu_mode', 'uwumode'], description='Enables debug mode which displays additional information on command execution in the assigned debug channel')
async def _debug_mode(ctx):
    global DEBUG_MODE

    if DEBUG_MODE:
        await debug_channel.send("Debug mode has been turned OFF")
        DEBUG_MODE = False
    else:
        await debug_channel.send("Debug mode has been turned ON")
        DEBUG_MODE = True
    
    return None

@bot.command(name='roadmap', aliases=['road_map', 'upcoming', 'whats_next', 'patchnotes', 'patch_notes', 'notes'], description='Provides a roadmap of upcoming features and voices')
async def _roadmap(ctx):
    
    caller = ctx.message.author.id
    caller_text_channel = ctx.message.channel
    debug_list = [f"Caller was {caller} from {caller_text_channel}"]

    await caller_text_channel.send(print_roadmap_str())

    if DEBUG_MODE:
        await debug_channel.send(debug_formatter(debug_list, "roadmap"))

@bot.command(name='voice_help', aliases=['voicehelp','add_voice', 'addvoice', 'faq'], description='A command to given hints on how to make a voice and make better audio from the available voices')
async def _voice_help(ctx):

    caller = ctx.message.author.id
    caller_text_channel = ctx.message.channel
    debug_list = [f"Caller was {caller} from {caller_text_channel}"]

    await caller_text_channel.send(print_voice_help_str())

    if DEBUG_MODE:
        await debug_channel.send(debug_formatter(debug_list, "voice_help"))

@bot.command(name='github', aliases=['git_hub', 'git', 'version_control', 'contribute'], description='Link to Github repo so folks can contribute if they want.')
async def _github(ctx):
    
    caller = ctx.message.author.id
    caller_text_channel = ctx.message.channel
    await caller_text_channel.send("Want to contribute? Check out the [Github repo](https://github.com/Gasperino11/mimus-polyglottos)!")

    if DEBUG_MODE:
        await debug_channel.send(debug_formatter([f"Caller was {caller} from {caller_text_channel}"], "github"))

@bot.command(name='usage', aliases=['used', 'characters_used', 'charactersused', 'characters'])
async def _usage(ctx):

    caller = ctx.message.author.id
    caller_text_channel = ctx.message.channel
    usage_info = get_usage()
    await caller_text_channel.send(f"This account has a {usage_info['limit']:,} character limit and has used {usage_info['used']:,} characters thus far and has {usage_info['available']:,} characters available until next month.")

    if DEBUG_MODE:
        await debug_channel.send(debug_formatter([f"Caller was {caller} from {caller_text_channel}"], "usage"))

bot.run(DISCORD_TOKEN)