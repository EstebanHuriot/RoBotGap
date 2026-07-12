from pathlib import Path
import discord
import credentials as cr


bot = discord.Client(intents=discord.Intents.all())


@bot.event
async def on_ready():
    serv = cr.discord_channel # guild or server id
    chan = cr.discord_salon_vocal # channel id 

    print(f"Bot connecté : {bot.user}")

    guild = bot.get_guild(serv)
    channel = bot.get_channel(chan)

    print("Serveur :", guild)
    print("Salon :", channel)


@bot.event
async def on_message(message: discord.Message):

    if message.author.bot: # bot ne de déclenche pas lui même
        return

    if message.content.lower() == 'hello':
        channel = message.channel
        await channel.send('Hello')

    if message.content.lower() == 'test':
        author = message.author
        await author.send('I know what you are hiding')


bot.run(cr.discord_bot_token)

