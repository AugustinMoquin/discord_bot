import discord
from discord.ext import commands
from decouple import config
from lists.chained_list import *
from lists.create_history import *

# get token from .env
TOKEN = config('TOKEN_DISCORD')

allHistory = {}
value = list_chained("bienvenue dans l'historique")
allHistory[363344729791922177] = value


intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_member_join(member):
    general_channel = client.get_channel(1099965926876663869)
    await general_channel.send("Bienvenue sur le serveur ! " + member.name)
    creatIndH(member, allHistory)


@client.command
async def size(ctx):
    # create_history.createH()
    await ctx.channel.send(allHistory[ctx.author.id].size())


@client.event
async def on_message(message):
    node = Node(message.content)
    #allHistory == disctionaire , message.author.id == emplacement
    allHistory[message.author.id].append(message.content)


@client.command()
async def add(ctx, arg):

    # debut de l'historique
    # node = Node(arg)
    # myHistory.append(node.data)
    # await ctx.channel.send(allHistory.)
    # await message.channel.send(history.seeData)

    # fin de l'historique

    if ctx.author == client.user:
        return

    user_id = ctx.author.id
    await ctx.send(f"Votre ID utilisateur est : {user_id}")

    await ctx.message.add_reaction('✅')


# @client.command()
# async def historique(ctx):
#     allHistory.seeData()


@client.command()
async def delete(ctx):
    messages = await ctx.channel.history(limit=10)

    for each_message in messages:
        await each_message.delete()


@client.event
async def on_ready():
    print("Le bot est prêt !")

# @client.event
# async def on_typing(channel, user, when):
#      await channel.send(user.name+" is typing")


# @client.event
# async def on_member_join(member):
#     general_channel = client.get_channel(1091279491755683891)
#     await general_channel.send("Bienvenue sur le serveur ! " + member.name)


# @client.event
# async def on_message(message):
#     general_channel = client.get_channel(1091279491755683891)

#     if message.author == client.user:
#         return

#     message.content = message.content.lower()

#     if message.content.startswith("hello"):
#         # await message.channel.send("Hello")
#         return

#     if "cochon" in message.content:
#         await message.channel.send("pas de cul ici")

#     if message.content == "azerty":
#         await message.channel.send("qwerty")

#     await client.process_commands(message)

client.run(TOKEN)
