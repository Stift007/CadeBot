import discord
from discord.ext import commands
import DiscordUtils
from DiscordUtils.Music import MusicPlayer,Song
import discord
from time import strftime
from loguru import logger

from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

client = commands.AutoShardedBot(command_prefix='c!',case_insensitive=True)#,shard_count=100)
slash = SlashCommand(client,sync_commands=True)
music = DiscordUtils.Music()


@client.event
async def on_shard_connect(shard_id):
    logger.warning("Shard Connected!")
    embed = discord.Embed(title="Shard Connection",description=f"""
✔ | Shard `{shard_id}` has successfully connected!!
:link: | [Discord Status](https://discordstatus.com)
:robot: | `{client.command_prefix}ping`
    """,color=0x00ff00)
    embed.add_field(name="Shard Information",value=f"""
    🌐 | Shard `{shard_id}`
    :date: | Time & Date: `{strftime('%H:%M:%S')}`-`{strftime('%D')}`
    """)
    await client.get_guild(942148719590113300).get_channel(942403453228048406).send(embed=embed)


@client.event
async def on_shard_reconnect(shard_id):
    logger.warning("Shard Reonnect!")

    embed = discord.Embed(title="Shard Reconnected",description=f"""
✔ | Shard `{shard_id}` has successfully reconnected!!
:link: | [Discord Status](https://discordstatus.com)
:robot: | `{client.command_prefix}ping`
    """,color=0x00ff00)
    embed.add_field(name="Shard Information",value=f"""
    🌐 | Shard `{shard_id}`
    :date: | Time & Date: `{strftime('%H:%M:%S')}`-`{strftime('%D')}`
    """)
    await client.get_guild(942148719590113300).get_channel(942403453228048406).send(embed=embed)


@client.event
async def on_shard_disconnect(shard_id):
    logger.warning("Shard Down!")
    embed = discord.Embed(title="Shard Outage",description=f"""
❌ | Shard `{shard_id}` is currently having an outage!
:link: | [Discord Status](https://discordstatus.com)
:robot: | `{client.command_prefix}ping`
    """,color=discord.Color.red())
    embed.add_field(name="Shard Information",value=f"""
    🌐 | Shard `{shard_id}`
    :date: | Time & Date: `{strftime('%H:%M:%S')}`-`{strftime('%D')}`
    """)
    await client.get_guild(942148719590113300).get_channel(942403453228048406).send(embed=embed)

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.listening,name=f"🎧 {len(client.guilds)} Servers listening!"))


@slash.slash(name="help",description="Help!",options=[
  create_option(
    name="command",
    description='Command',
    required=False,
    option_type=3
  )
])
async def help(ctx,command=None):
    if not command:
        embed = discord.Embed(color=discord.Color.random(),title="Help")
        for command in client.commands:
            embed.add_field(name=command.name,value=f'{command.help}\n`{command.usage}`',inline=False)
        await ctx.send(":ok_hand: Check your DMs!")
        await ctx.author.send(embed=embed)
    else:
        command = client.get_command(command)
        if command:
            embed = discord.Embed(title=command.name,description=f'{command.help}\n`{command.usage}`')
            await ctx.send(":ok_hand: Check your DMs!")
            await ctx.author.send(embed=embed)
        else:
            await ctx.send(":open_mouth: Wow, such empty...")

@slash.slash(name="join",description="Joins your VC")
async def join(ctx):
    voice = ctx.author.voice
    if not voice:
        return await ctx.send("You're not in a voice channel!")
    await ctx.author.voice.channel.connect()
    await ctx.send('Joined!')

@slash.slash(name="play",description="Play Music!",options=[
  create_option(name="query",description="Search Query",option_type=3,required=False),
  create_option(name="bettersearch",description="Use BetterSearch?",option_type=5,required=False),
])
async def play(ctx, query=None,bettersearch=False):
    if not query:
        return await ctx.send("Please specify a search query...")
    if not ctx.guild.voice_client:
        return await ctx.send("I am not connected to any VOice channel!")
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
        await ctx.send(":open_mouth: Wow, such empty...")

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
        embed.add_field(name="▶ Play it:",value=f'`hal.play {song.url}`',inline=False)
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
