import discord
from pathlib import Path

BOT_FOLDER = Path(__file__).resolve().parent
PROJECT_FOLDER = BOT_FOLDER.parent

DEATH_SOUND_PATH = BOT_FOLDER / "sounds" / "death.mp3"
FFMPEG_PATH = PROJECT_FOLDER / "tools" / "ffmpeg.exe"


async def play_death_sound(bot:discord.Client ,guild_id:int, voice_channel_id:int):
    
    guild = bot.get_guild(guild_id) # server
    if guild is None :
        print('Cant find discord server')
        return

    channel = guild.get_channel(voice_channel_id) # channel
    if channel is None:
        print('Cant find discord channel')
        return

    voice_client = guild.voice_client

    if voice_client is None: # bot is not connected to a voice chat
        voice_client = await channel.connect()

    elif voice_client.channel.id != channel.id: # bot is connected to another voicechat
        await voice_client.move_to(channel)

    if voice_client.is_playing(): # if already playing a song, stops  (keeping it ??)
        voice_client.stop()

    source = discord.FFmpegPCMAudio(str(DEATH_SOUND_PATH),executable=FFMPEG_PATH)

    voice_client.play(source)