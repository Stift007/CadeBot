import discord
from discord.ext import commands
import DiscordUtils
from DiscordUtils.Music import MusicPlayer,Song
import discord
import json
from time import strftime
from loguru import logger

from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

client = commands.AutoShardedBot(command_prefix='c!',case_insensitive=True)#shard_count=100)
slash = SlashCommand(client,sync_commands=True)
music = DiscordUtils.Music()

with open("config.json") as f:
    cfg = json.load(f)

SuggestionChannelID = cfg["Suggestion_Channel_ID"]
SupportChannelID = cfg["Support_Channel_ID"]
HttpOAuthToken = cfg["Token"]
ShardlogChannelID = cfg["Shards_Channel_ID"]


@client.event
async def on_shard_connect(shard_id):
    logger.warning("Shard Connect - BETA")
    embed = discord.Embed(title="Shard Connection - BETA",description=f"""
✔ | Shard `{shard_id}` has successfully connected!!
:link: | [Discord Status](https://discordstatus.com)
:robot: | `{client.command_prefix}ping`
    """,color=0x00ff00)
    embed.add_field(name="Shard Information",value=f"""
    🌐 | Shard `{shard_id}`
    :date: | Time & Date: `{strftime('%H:%M:%S')}`-`{strftime('%D')}`
    """)
    await client.get_channel(ShardlogChannelID).send(embed=embed)

    
@slash.slash(name="ping",description="Wanna play PING PONG ;)")
async def ping(ctx):
    await ctx.send(f'My ping is** {round(client.latency*1000)} Ms**')

@client.event
async def on_shard_disconnect(shard_id):
    logger.warning("Shard Down - BETA")
    embed = discord.Embed(title="Shard Outage - BETA",description=f"""
❌ | Shard `{shard_id}` is currently having an outage!
:link: | [Discord Status](https://discordstatus.com)
:robot: | `{client.command_prefix}ping`
    """,color=discord.Color.red())
    embed.add_field(name="Shard Information",value=f"""
    🌐 | Shard `{shard_id}`
    :date: | Time & Date: `{strftime('%H:%M:%S')}`-`{strftime('%D')}`
    """)
    await client.get_channel(ShardlogChannelID).send(embed=embed)

    
from discord.ext import tasks
import asyncio

@client.event
async def on_ready():
  await statusCycle.start()

@tasks.loop(seconds=2)
async def statusCycle():
    stats = [f"{len(client.guilds)} Servers!"]
    for s in stats:
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=s),status=discord.Status.dnd)
      await asyncio.sleep(20)

@slash.slash(name="suggest",description="Suggest a feature/Command",options=[
    create_option(name="suggestion",description="Your Suggestion",option_type=3, required=True)
])
async def suggest(ctx,suggestion):
    embed = discord.Embed(title="New Suggestion!",description=f"Suggestion by {ctx.author} ({ctx.author.id})")
    embed.add_field(name="Suggestion",value=suggestion)
    await client.get_channel(SuggestChannelID).send(embed=embed)
    await ctx.send("Your suggestion has been posted!",hidden=True)

@slash.slash(name="serversupport",description="Gets a server representative to join the server",options=[
create_option(name="invite",description="discord.gg/",option_type=3,required=True),
create_option(name="reason",description="Why you need a Support Member in your server",option_type=3, required=True)
])
async def serversupport(ctx,invite, reason):
    embed = discord.Embed(title="Support Request",description=f"Suggestion by {ctx.author} ({ctx.author.id})")
    embed.add_field(name="Invite",value=invite)
    embed.add_field(name="Reason",value=reason)
    await client.get_channel(SupportChannelID).send(embed=embed)
    await ctx.send("Sent request: This may take up to 1-2 Working Days!",hidden=True)
        
 
@slash.slash(name="join",description="Joins your VC")
async def join(ctx):
    voice = ctx.author.voice
    if not voice:
        return await ctx.send("You're not in a voice channel!")
    await ctx.author.voice.channel.connect()
    await ctx.send('Joined!')

@slash.slash(name="commands",description="View a command list!")
async def cmds(ctx):
    embed = discord.Embed(title="CadeBot Help")
    embed.add_field(name="Play",value="/play <query> [optn:bettersearch (True|False)]")
    embed.add_field(name="Stop",value="/stop")
    embed.add_field(name="Nowplaying",value="/nowplaying")
    embed.add_field(name="Grab",value="/grab")
    embed.add_field(name="Queue",value="/queue")
    embed.add_field(name="Volume",value="/volume <new-volume>")
    embed.add_field(name="Skip",value="/skip")
    embed.add_field(name="PING",value="/ping")
    embed.add_field(name="Join",value="/join")
    embed.add_field(name="Leave",value="/leave")
    embed.add_field(name="Pause",value="/pause")
    embed.add_field(name="Resume",value="/resume")
    embed.add_field(name="Loop",value="/loop")
    await ctx.send(embed=embed,hidden=True)
    
@slash.slash(name="play",description="Play Music!",options=[
  create_option(name="query",description="Search Query",option_type=3,required=False),
  create_option(name="bettersearch",description="Use BetterSearch?",option_type=5,required=False),
])
async def play(ctx, query=None,bettersearch=False):
    if not query:
        return await ctx.send("Please specify a search query...")
    if not ctx.guild.voice_client:
        return await ctx.send("I am not connected to any Voice channel!")
    player = music.get_player(guild_id=ctx.guild.id)
    if not player:
        player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
        await player.queue(query,search=True,bettersearch=bettersearch)
        song = await player.play()
        
        await ctx.send(f'Now playing: {song.name}')
    else:
        song = await player.queue(query,search=True,bettersearch=bettersearch)
        await ctx.send(f'Queued: {song.name}')

@slash.slash(name="queue",description="View the Queue")
async def queue(ctx):
    try:
        player = music.get_player(guild_id=ctx.guild.id)
        await ctx.send(",".join(song.name for song in player.current_queue()))
    except:
        await ctx.send(":open_mouth: Kinda quiet here....")

@slash.slash(name="stop",description="Stop the Player")
async def stop(ctx):
    try:
        player:MusicPlayer = music.get_player(guild_id=ctx.guild.id)
        await player.stop()
        await ctx.send("⏹ Killed the Player!",hidden=True)
    except:
        await ctx.send(":open_mouth: Nah, nothing playing rn...")

@slash.slash(name="loop",description="Toggle Loop")
async def loop(ctx):
    try:
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.toggle_song_loop()
        await ctx.send("🔂 Loop Toggled!")
    except Exception as error:
        await ctx.send(error)

@slash.slash(name="skip",description="Skip the Song")
async def skip(ctx):
    try:
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.skip()
        await ctx.send(f"⏩ Skipped from {song[0].name} to {song[1].name}!")
    except Exception as error:
        await ctx.send(f":x: {error}")

@slash.slash(name="grab",description="Save the Song!")
async def grab(ctx):
    try:
        player:MusicPlayer = music.get_player(guild_id=ctx.guild.id)
        song:Song = player.now_playing()
        embed = discord.Embed(title=song.name,url=song.url)
        embed.add_field(name="⌛ Duration:",value=f'`{song.duration}`')
        embed.add_field(name="🎵 Creator:",value=f'[`{song.channel}`]({song.channel_url})')
        embed.add_field(name="▶ Play it:",value=f'`/play {song.url}`',inline=False)
        embed.set_thumbnail(url=song.thumbnail)
        await ctx.author.send(embed=embed)
        await ctx.send("Check your DMs!",hidden=True)
    except:
        await ctx.send(":open_mouth: Wow, such empty...",hidden=True)
        
@slash.slash(name="nowplaying",description="Currently playing Song")
async def nowplaying(ctx):
    try:
        player = music.get_player(guild_id=ctx.guild.id)
        song = player.now_playing()
        await ctx.send(song.name)
    except:
        await ctx.send(":open_mouth: Wow, such empty...")

@slash.slash(name="volume",description="Adjust the Volume",options=[
  create_option(name="volume",description='New Volume',option_type=4,required=False)
])
async def volume(ctx,volume:int=100):
    try:
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.change_volume(volume)
        await ctx.send(f'🔊 Volume is now {volume}')
    except Exception as error:
        await ctx.send(error)    

@slash.slash(name="pause",description="Pause the Player")
async def pause(ctx):
    try:
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.pause()
        await ctx.send(f"⏸ Paused {song.name}")
    except Exception as error:
        await ctx.send(error)

@slash.slash(name="resume",description="Resume the Player")
async def resume(ctx):
    try:
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.resume()
        await ctx.send(f"⏯ Resumed {song.name}")

    except Exception as error:
        await ctx.send(error)

@slash.slash(name="leave",description="Leave the Voice Channel")
async def leave(ctx):
    voice = ctx.author.voice
    myvoice = ctx.guild.me.voice
    if not voice or not myvoice:
        return await ctx.send("Either me or you aren't in a voice channel!",hidden=True)
    await ctx.voice_client.disconnect()
    await ctx.send('Left!')


client.run(HttpOAuthToken,reconnect=True)
