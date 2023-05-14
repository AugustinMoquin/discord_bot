import discord
import asyncio

client = discord.Client()

TOKEN = config('TOKEN_DISCORD')

# Définir le canal pour l'historique
channel_id = 1091262168713924620

# Définir le nom du fichier d'historique
history_file = "history.txt"

# Définir la réaction pour avancer dans l'historique
next_emoji = "➡️"

# Définir la réaction pour reculer dans l'historique
prev_emoji = "⬅️"

# Définir la réaction pour supprimer un message de l'historique
delete_emoji = "❌"

# Définir les autorisations pour l'accès à l'historique
allowed_roles = ["Admin", "Modérateur"]

# Dictionnaire pour stocker l'historique des messages de chaque utilisateur
history = {}

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
                    embed = discord.Embed(title=f"Page {index+1}/{len(history[user_id])}", description=history[user_id][index], color=discord.Color.blue())
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
                embed = discord.Embed(title=f"Page {index+1}/{len(history[user_id])}", description=history[user_id][index], color=discord.Color.blue())
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
            embed = discord.Embed(title=f"Page 1/{len(history[user_id])}", description=history[user_id][0], color=discord.Color.blue())
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
client.run(TOKEN)