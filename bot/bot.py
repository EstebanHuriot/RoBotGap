from pathlib import Path
import discord
import credentials as cr


bot = discord.Client(intents=discord.Intents.all())

DEATH_SOUND = Path(__file__).parent / "sounds" / "death.mp3"


async def play_death_sound(guild_id:int, voice_channel_id:int):
    
    guild = bot.get_guild(guild_id) # server
    if guild is None :
        print('Cant find discord server')

    channel = guild.get_channel(voice_channel_id) # channel
    if channel is None:
        print('Cant find discord channel')


    voice_client = guild.voice_client

    if voice_client is None: # bot is not connected to a voice chat
        voice_client = await channel.connect()

    elif voice_client.channel.id != channel.id: # bot is connected to another voicechat
        await voice_client.move_to(channel)

    if voice_client.is_playing(): # if already playing a song, stops  (keeping it ??)
        voice_client.stop()

    source = discord.FFmpegPCMAudio(str(DEATH_SOUND))

    voice_client.play(
        source,
        after=lambda error: print(f"Erreur audio : {error}") if error else None,
    )




@bot.event
async def on_ready():
    print('bot ready')

@bot.event
async def on_message(message: discord.Message):
    if message.content == 'Hello':
        channel = message.channel
        await channel.send('Hey')


bot.run(cr.discord_bot_token)

