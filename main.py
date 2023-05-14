import chained_list as chained_list
import queues as queue
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
# import youtube_dl

DISCORD_TOKEN = os.getenv("discord_token")
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

# classe de stockage du message


class Message:
    def __init__(self, text, user):
        self.text = text
        self.user = user

    def __str__(self):
        text_str = "%s :\n%s" % (self.user, self.text)
        return text_str


# Déclaration des variables
history = chained_list.List_chained(Message("Welcome to the history", "Bot"))
first_node = queue.Node(None, None, None)
actual_history_node = history.first_node
actual_history_name = None
allowed_roles = ["Admin", "mod"]
history_file = "history.txt"

# class pour le help (a changer pour l'arbre binaire)


class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help")
        for cog, commands in mapping.items():
            command_signatures = [
                self.get_command_signature(c) for c in commands]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(
                    command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)


client.help_command = MyHelp()

# Fonction pour écrire l'historique dans un fichier texte


def write_history_to_file(message):
    f = open(history_file, "a")
    f.write(f"User {message.user}: {message.text} \n")
    f.close

# rajoute une réaction au message du bot pour naviguer dans l'historique


@client.event
async def on_reaction_add(reaction, user):
    emoji = reaction.emoji
    global actual_history_node
    global actual_history_name
    if user.bot == client.user:
        return
    elif emoji == "❌" and "mod" in [y.name.lower() for y in user.roles]:
        await reaction.message.delete()
        return
    elif emoji == "🔺" and "mod" in [y.name.lower() for y in user.roles]:
        if actual_history_node.previous_node is not None:
            actual_history_node = actual_history_node.previous_node
            await reaction.message.edit(content=str(actual_history_node.data))
        return
    elif emoji == "🔻" and "mod" in [y.name.lower() for y in user.roles]:
        if actual_history_node.following_node is not None:
            actual_history_node = actual_history_node.following_node
            await reaction.message.edit(content=str(actual_history_node.data))
        return
    elif emoji == "⏫" and "mod" in [y.name.lower() for y in user.roles]:
        if actual_history_node.previous_node is not None:
            actual_history_node = actual_history_node.previous_node
            while actual_history_node.data.user != actual_history_name:
                if actual_history_node.previous_node is not None:
                    actual_history_node = actual_history_node.previous_node
                    print(actual_history_node.data.user)
                    print(actual_history_name)
                else:
                    break
            if actual_history_node.data.user == actual_history_name:
                await reaction.message.edit(content=str(actual_history_node.data))
        return
    elif emoji == "⏬" and "mod" in [y.name.lower() for y in user.roles]:
        if actual_history_node.following_node is not None:
            actual_history_node = actual_history_node.following_node
            while actual_history_node.data.user != actual_history_name:
                if actual_history_node.following_node is not None:
                    actual_history_node = actual_history_node.following_node
                    print(actual_history_node.data.user)
                    print(actual_history_name)
                else:
                    break
            if actual_history_node.data.user == actual_history_name:
                await reaction.message.edit(content=str(actual_history_node.data))
        return

# sauvegarde du message


@client.command(pass_context=True)
async def save(ctx, *, arg):
    message = Message(arg, ctx.message.author.name)
    history.append(message)
    write_history_to_file(message)
    await ctx.message.add_reaction("✅")


# indique que le bot a démarré
@client.event
async def on_ready():
    print("Le bot est prêt !")


@client.command()
async def showH(ctx, arg):
    global actual_history_node
    if arg == "last":
        message = await ctx.send(str(history.view(history.length-1)))
    else:
        index = int(arg)
        actual_history_node = history.get(index)
        message = await ctx.send(str(history.view(index)))
    await message.add_reaction("🔺")
    await message.add_reaction("🔻")
    await message.add_reaction("❌")


@client.command()
async def userH(ctx, arg):
    name = str(arg)
    global actual_history_name
    global actual_history_node
    actual_history_node = history.get_from(name)
    actual_history_name = name
    message = await ctx.send(str(history.view_from(name)))
    await message.add_reaction("⏫")
    await message.add_reaction("🔺")
    await message.add_reaction("🔻")
    await message.add_reaction("⏬")
    await message.add_reaction("❌")


@client.command()
async def clear(ctx):
    history.clear(Message("First message", "Bot"))
    await ctx.message.add_reaction("✅")


@client.command()
async def lenght(ctx):
    await ctx.channel.send(str(history.length))
    await ctx.message.add_reaction("✅")

client.run("ODYyNDI0Njk0NTI3NDkyMTA2.Gy8R6w.V_XfvVA2rTE60FG6uIwi4SqEURoA5B_l-sy784")
