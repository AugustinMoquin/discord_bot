import discord
from discord.ext import commands
from decouple import config
from chained_list import *
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



# ---------------------------------------------------------------------------------------------------------------------------------------------

import discord
import asyncio
from discord.ext import commands
from decouple import config

# client = discord.Client()

# TOKEN = config('TOKEN_DISCORD')

# Définir le canal pour l'historique
channel_id = 1091262168713924620
# Dictionnaire pour stocker l'historique des messages de chaque utilisateur
history = {}

# Définir le nom du fichier d'historique
history_file = "history.txt"
next_emoji = "➡️"
prev_emoji = "⬅️"
delete_emoji = "❌"
allowed_roles = ["Admin", "Modérateur"]


intents = discord.Intents.all()
client = commands.Bot(command_prefix="&", intents=intents)

# Fonction pour ajouter un message à l'historique d'un utilisateur


def add_to_history(message):
    user_id = str(message.author.id)
    if user_id not in history:
        history[user_id] = []
    history[user_id].append(message.content)


# Fonction pour écrire l'historique dans un fichier texte
def write_history_to_file():
    with open(history_file, "w") as file:
        for user_id, messages in history.items():
            file.write(f"User {user_id}:\n")
            for i, message in enumerate(messages):
                file.write(f"{i+1}. {message}\n")
            file.write("\n")

# Fonction pour charger l'historique depuis un fichier texte


def load_history_from_file():
    with open(history_file, "r") as file:
        user_id = ""
        for line in file:
            if line.startswith("User "):
                user_id = line.split()[1].rstrip(":")
                history[user_id] = []
            elif user_id:
                history[user_id].append(line.rstrip())

# Événement pour récupérer les messages et les ajouter à l'historique


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id == channel_id:
        add_to_history(message)

# Événement pour réagir aux réactions et afficher les messages de l'historique


@client.event
async def on_reaction_add(reaction, user):
    # Vérifier que la réaction est ajoutée sur un message du bot et que l'utilisateur est autorisé à accéder à l'historique
    if user != client.user and reaction.message.author == client.user and any(role.name in allowed_roles for role in user.roles):
        message = reaction.message
        user_id = str(message.embeds[0].footer.text.split(": ")[1])
        if reaction.emoji == next_emoji:
            if user_id in history:
                if message.embeds[0].title.startswith("Page "):
                    index = int(message.embeds[0].title.split()[1])
                else:
                    index = 0
                if index < len(history[user_id]) - 1:
                    index += 1
                    embed = discord.Embed(
                        title=f"Page {index+1}/{len(history[user_id])}", description=history[user_id][index], color=discord.Color.blue())
                    embed.set_footer(text=f"User ID: {user_id}")
                    await message.edit(embed=embed)
        elif reaction.emoji == prev_emoji:
            if user_id in history:
                if message.embeds[0].title.startswith("Page "):
                    index = int(message.embeds[0].title.split()[1])
            else:
                index = len(history[user_id]) - 1
            if index > 0:
                index -= 1
                embed = discord.Embed(
                    title=f"Page {index+1}/{len(history[user_id])}", description=history[user_id][index], color=discord.Color.blue())
                embed.set_footer(text=f"User ID: {user_id}")
                await message.edit(embed=embed)
        elif reaction.emoji == delete_emoji:
            if user_id in history:
                if message.embeds[0].title.startswith("Page "):
                    index = int(message.embeds[0].title.split()[1]) - 1
                    del history[user_id][index]
                    write_history_to_file()
                    if len(history[user_id]) == 0:
                        del history[user_id]
                        await message.delete()
                else:
                    await message.add_reaction(delete_emoji)

# Commande pour afficher l'historique d'un utilisateur


@client.command()
async def history(ctx, user: discord.User):
    user_id = str(user.id)
    if any(role.name in allowed_roles for role in ctx.author.roles) or user_id == str(ctx.author.id):
        if user_id in history:
            embed = discord.Embed(
                title=f"Page 1/{len(history[user_id])}", description=history[user_id][0], color=discord.Color.blue())
            embed.set_footer(text=f"User ID: {user_id}")
            message = await ctx.send(embed=embed)
            if len(history[user_id]) > 1:
                await message.add_reaction(prev_emoji)
                await message.add_reaction(next_emoji)
                await message.add_reaction(delete_emoji)
            else:
                await ctx.send(f"No history found for user {user.mention}.")

# Commande pour télécharger l'historique d'un utilisateur


@client.command()
async def download(ctx, user: discord.User):
    user_id = str(user.id)
    if any(role.name in allowed_roles for role in ctx.author.roles) or user_id == str(ctx.author.id):
        if user_id in history:
            with open(f"{user.name}_history.txt", "w") as file:
                for i, message in enumerate(history[user_id]):
                    file.write(f"{i+1}. {message}\n")
            with open(f"{user.name}_history.txt", "rb") as file:
                await ctx.send(f"Here is the history for {user.mention}.", file=discord.File(file, f"{user.name}_history.txt"))
        else:
            await ctx.send(f"No history found for user {user.mention}.")
    else:
        await ctx.send("You are not authorized to download histories.")


@client.event
async def on_ready():
    print("Le bot est prêt !")

# Chargement de l'historique depuis le fichier texte au démarrage
load_history_from_file()

# Boucle principale du bot
client.run("ODYyNDI0Njk0NTI3NDkyMTA2.Gy8R6w.V_XfvVA2rTE60FG6uIwi4SqEURoA5B_l-sy784")
