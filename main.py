import chained_list as chained_list
import queues as queue
import tree as tree
import discord
# import discord_components
from discord.ext import commands
import os
import asyncio

DISCORD_TOKEN = os.getenv("discord_token")
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

######## DECLARATION VAR ########


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
history_node = history.first_node
history_name = None
allowed_roles = ["Admin", "mod"]
history_file = "history.txt"
isUsed = False
global isUsing


######## BINARY TREE ########

@client.command()
async def start(ctx):
    message1 = await ctx.send("Bienvenue ! Prêt à parler de recettes de desserts ? Réagissez avec ✅ pour commencer.")
    await message1.add_reaction("✅")

    def check(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) == '✅'
    
    

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
    except:
        await ctx.send("Délai d'attente dépassé. Veuillez réessayer.")
        return

    await ctx.send("Super ! Allons-y.")

    GChocolat = tree.TreeNode("Bievu le chocolat c'est trop bon", None, None, None, None, "chocolat")
    GVanille = tree.TreeNode("C'est aussi mon préferé (☞ﾟヮﾟ)☞", None, None, None, None, "vanille")

    GlaceChocolat = tree.TreeNode("Bievu le chocolat c'est trop bon", None, None, None, None, "chocolat")
    GlaceVanille = tree.TreeNode("C'est aussi mon préferé (☞ﾟヮﾟ)☞", None, None, None, None, "vanille")


    gateau = tree.TreeNode("Plutôt gâteau au chocolat ou vanille?", GChocolat, "🍫", GVanille, "⚪", "gateau")
    glace = tree.TreeNode("Plutôt glace au chocolat ou vanille?", GlaceChocolat, "🍫", GlaceVanille, "⚪", "glace")

    root = tree.TreeNode("Quel type de dessert préférez-vous ?",
           gateau, "🍰",
           glace, "🍦", "root")
    

    current_node = root

    while True: 
        await ctx.send(current_node.question)
        message2 = await ctx.send(f"{current_node.left.state} / {current_node.right.state}")
        await message2.add_reaction(current_node.symbolL)
        await message2.add_reaction(current_node.symbolR)

        
        def check_response(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in [current_node.symbolL, current_node.symbolR]

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check_response)
        except:
            await ctx.send("Délai d'attente dépassé. Veuillez réessayer.")
            return

        if str(reaction.emoji)  == current_node.symbolL:
            current_node = current_node.left
        elif str(reaction.emoji)  == current_node.symbolR:
            current_node = current_node.right
        else:
            await ctx.send("Je suis désolé, je ne comprends pas votre réponse.")
            continue

        if current_node is None:
            await ctx.send("C'est tout ce que j'ai pour le moment. Merci de votre participation !")
            break


######## FONCTION ########

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

######## EVENT ET COMMANDE ########

# rajoute une réaction au message du bot pour naviguer dans l'historiquE


@client.event
async def on_reaction_add(reaction, user):
    emoji = reaction.emoji
    global history_node
    isUsed = True
    isUsing = user.name

    if user.bot == client.user:
        return
    elif emoji == "❌" and "mod" in [y.name.lower() for y in user.roles]:
        await reaction.message.delete()
        isUsed = False
    elif emoji == "🔺" and "mod" in [y.name.lower() for y in user.roles]:
        if history_node.previous_node is not None:
            history_node = history_node.previous_node
            await reaction.message.edit(content=str(history_node.data))
    elif emoji == "🔻" and "mod" in [y.name.lower() for y in user.roles]:
        if history_node.following_node is not None:
            history_node = history_node.following_node
            await reaction.message.edit(content=str(history_node.data))
        

# sauvegarde du message


@client.command(pass_context=True)
async def save(ctx, *, arg):
    message = Message(arg, ctx.message.author.name)
    history.append(message)
    write_history_to_file(message)

# indique que le bot a démarré


@client.event
async def on_ready():
    print("Le bot est prêt !")


# @client.slash_command()  # Create a slash command
# async def button(ctx):
#     # Send a message with our View class that contains the button
#     await ctx.respond("This is a button!", view=MyView())


@client.command()
async def showH(ctx, arg):
    if isUsed == False:
        global history_node
        index = 0
        if arg == "last":
            index = int(history.length-1)
            message = await ctx.send(str(history.view(index)))
        else:
            index = int(arg)
            history_node = history.get(index)
            message = await ctx.send(str(history.view(index)))
        await message.add_reaction("🔺")
        await message.add_reaction("🔻")
        await message.add_reaction("❌")
    else:
        ctx.send(f"the history is in use by {isUsing}")


@client.command()
async def clear(ctx):
    history.clear(Message("First message", "Bot"))
    f = open(history_file, "w")
    f.write("")
    f.close


@client.command()
async def lenght(ctx):
    await ctx.channel.send(str(history.length))


@client.command()
async def play(ctx):
    if ctx.author.voice is None:
        await ctx.channel.send("You need to join a voice channel first.")
        return

        # Get the voice channel of the user who sent the command
    voice_channel = ctx.author.voice.channel

    # Join the voice channel
    voice_client = await voice_channel.connect()

    # Get the path to the MP3 file
    file_path = os.path.join(os.getcwd(), "mauvaiseFoiNocturne.mp3")

    # Play the MP3 file
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(file_path))
    voice_client.play(source)

    # Wait for the audio to finish playing
    while voice_client.is_playing():
        await asyncio.sleep(1)

        # Disconnect from the voice channel
    await voice_client.disconnect()

# permet de telechrager l'historique


@client.command()
async def dl(ctx, arg):
    user: discord.User
    #user = ctx.message.author.name
    user = arg
    history_node = history.get(0)
    if any(role.name in allowed_roles for role in ctx.author.roles) or user == ctx.author.name:
        if history_node.following_node is not None:
            history_node = history_node.following_node
            for i in history.length:
                if history_node.following_node is not None:
                    history_node = history_node.following_node
                    if history_node.data.user == user:
                        with open(f"{user}_history.txt", "w") as file:
                            file.write(f"{i}. {history_node.data.text}\n")
                else:
                    await ctx.send(f"No history found for user {user.mention}.")
                    break
            with open(f"{user}_history.txt", "rb") as file:
                await ctx.send(f"Here is the history for {user}.", file=discord.File(file, f"{user}_history.txt"))
    else:
        await ctx.send("You are not authorized to download histories.")


client.run("ODYyNDI0Njk0NTI3NDkyMTA2.Gy8R6w.V_XfvVA2rTE60FG6uIwi4SqEURoA5B_l-sy784")
