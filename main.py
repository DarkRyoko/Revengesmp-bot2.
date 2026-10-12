import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
await bot.tree.sync()
print(f"RevengeSMP Bot online: {bot.user}")

@bot.tree.command(name="ping", description="Verifica daca botul este online")
async def ping(interaction: discord.Interaction):
await interaction.response.send_message("⚔️ RevengeSMP Bot este online!", ephemeral=True)

@bot.tree.command(name="server", description="Informatii despre RevengeSMP")
async def server(interaction: discord.Interaction):
embed = discord.Embed(
title="⚔️ RevengeSMP",
description="SURVIVE. FIGHT. DOMINATE.",
color=discord.Color.red()
)
embed.add_field(name="Versiune", value="1.8–1.21.11+", inline=True)
embed.add_field(name="Tip", value="SMP", inline=True)
await interaction.response.send_message(embed=embed)

@bot.tree.command(name="clear", description="Sterge mesaje")
@commands.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
if amount < 1 or amount > 100:
await interaction.response.send_message(
"Alege un numar intre 1 si 100.",
ephemeral=True
)
return
await interaction.response.defer(ephemeral=True)
deleted = await interaction.channel.purge(limit=amount)
await interaction.followup.send(
f"Am sters {len(deleted)} mesaje.",
ephemeral=True
)

@bot.tree.command(name="kick", description="Da kick unui membru")
@commands.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Fara motiv"):
await member.kick(reason=reason)
await interaction.response.send_message(
f"🔨 {member.mention} a primit kick. Motiv: {reason}"
)

@bot.tree.command(name="ban", description="Baneaza un membru")
@commands.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Fara motiv"):
await member.ban(reason=reason)
await interaction.response.send_message(
f"🔨 {member.mention} a primit ban. Motiv: {reason}"
)

@bot.tree.command(name="userinfo", description="Informatii despre un membru")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
member = member or interaction.user
embed = discord.Embed(title=f"Informatii: {member}", color=discord.Color.blue())
embed.add_field(name="ID", value=str(member.id))
embed.add_field(name="Cont creat", value=discord.utils.format_dt(member.created_at, style="D"))
embed.add_field(name="A intrat pe server", value=discord.utils.format_dt(member.joined_at, style="D") if member.joined_at else "Necunoscut")
await interaction.response.send_message(embed=embed)

bot.run(TOKEN)
