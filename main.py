import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv("bot.env")
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
raise RuntimeError("Lipsește DISCORD_TOKEN din fișierul bot.env!")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
await bot.tree.sync()
print(f"RevengeSMP Bot online: {bot.user}")

@bot.tree.command(name="ping", description="Verifică dacă botul este online")
async def ping(interaction: discord.Interaction):
await interaction.response.send_message(
"⚔️ RevengeSMP Bot este online!",
ephemeral=True
)

@bot.tree.command(name="server", description="Informații despre RevengeSMP")
async def server(interaction: discord.Interaction):
embed = discord.Embed(
title="⚔️ RevengeSMP",
description="SURVIVE. FIGHT. DOMINATE.",
color=discord.Color.red()
)
embed.add_field(name="Versiune", value="1.8–1.21.11+", inline=True)
embed.add_field(name="Tip", value="SMP", inline=True)
await interaction.response.send_message(embed=embed)

@bot.tree.command(name="clear", description="Șterge mesaje")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]):
if not isinstance(interaction.channel, discord.TextChannel):
await interaction.response.send_message(
"Comanda poate fi folosită doar într-un canal text.",
ephemeral=True
)
return

await interaction.response.defer(ephemeral=True)
deleted = await interaction.channel.purge(limit=amount)
await interaction.followup.send(
    f"🧹 Am șters {len(deleted)} mesaje.",
    ephemeral=True
)

@bot.tree.command(name="kick", description="Dă kick unui membru")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(
interaction: discord.Interaction,
member: discord.Member,
reason: str = "Fără motiv"
):
await member.kick(reason=reason)
await interaction.response.send_message(
f"🔨 {member.mention} a primit kick. Motiv: {reason}"
)

@bot.tree.command(name="ban", description="Banează un membru")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(
interaction: discord.Interaction,
member: discord.Member,
reason: str = "Fără motiv"
):
await member.ban(reason=reason)
await interaction.response.send_message(
f"🔨 {member.mention} a primit ban. Motiv: {reason}"
)

@bot.tree.command(name="userinfo", description="Informații despre un membru")
async def userinfo(
interaction: discord.Interaction,
member: discord.Member | None = None
):
member = member or interaction.user

embed = discord.Embed(
    title=f"Informatii: {member}",
    color=discord.Color.blue()
)
embed.add_field(name="ID", value=str(member.id), inline=False)
embed.add_field(
    name="Cont creat",
    value=discord.utils.format_dt(member.created_at, style="D"),
    inline=False
)

if member.joined_at:
    embed.add_field(
        name="A intrat pe server",
        value=discord.utils.format_dt(member.joined_at, style="D"),
        inline=False
    )

await interaction.response.send_message(embed=embed)

@bot.tree.error
async def on_app_command_error(
interaction: discord.Interaction,
error: app_commands.AppCommandError
):
if isinstance(error, app_commands.MissingPermissions):
message = "❌ Nu ai permisiunile necesare pentru această comandă."
else:
message = "❌ A apărut o eroare. Verifică consola botului."

if interaction.response.is_done():
    await interaction.followup.send(message, ephemeral=True)
else:
    await interaction.response.send_message(message, ephemeral=True)

bot.run(TOKEN)
