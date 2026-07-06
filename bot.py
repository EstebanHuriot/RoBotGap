import discord
import credentials as cr

bot = discord.Client(intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('bot ready')

@bot.event
async def on_message(message: discord.Message):
    if message.content == 'Hello':
        channel = message.channel
        await channel.send('Hey')


bot.run(cr.discord_bot_token)

