import discord
from discord.ext import commands
from decouple import config
from chained_list import *

def createH(ctx):
    f = open( ctx.author.id + ".txt", "x")


#pour nommer des variables dynamiquement on ajoute des nos valeurs et leur noms dans un dictionnaire
def creatIndH(member, allHistory):
    key = member.id
    value = list_chained("bienvenue dans l'historique")
    allHistory[key] = value     
