import discord
from discord import guild
from discord.ext import commands
from configparser import ConfigParser
import json
import os
import asyncio

token = input("Enter the bot token: ")

print("Starting...")


bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
bot.remove_command("help")

file = "config.ini"
config = ConfigParser()
config.read(file)

@bot.event
async def on_ready():
  print("Your bot is ready.")


@bot.event
async def on_message(msg):
    await bot.process_commands(msg)
    id = msg.author.id
    if msg.author != bot.user:
      if config["configuration"]["antilink"] == "enabled":
        if "https" or "www." or ".com" or "discord.gg" in msg.content:
          if msg.author.id != bot.user:
            if msg.author.id not in white:
              await msg.delete()
            elif white[id] == 0:
              await msg.delete()
            else:
              await bot.process_commands(msg)
          else:
            await bot.process_commands(msg)
        else:
          await bot.process_commands(msg)
      elif config["configuration"]["pingprotection"] == "enabled":
        if "@everyone" in msg.content:
            await msg.delete()
       
@bot.event
async def on_guild_channel_create(channel):
  if config["configuration"]["channelsecurity"] == "enabled":
    logs = await channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create).flatten()

    user_id = logs[0].user

    final_id = bot.get_user(user_id)

    await final_id.ban(reason="You are not allowed to create channels!")
  else:
    pass

@bot.event
async def on_member_join(user):
  if config["configuration"]["kickbot"] == "enabled":
    if user.bot:
      await user.kick(reason="You are a bot")
    else:
      pass
  else:
    pass

@bot.event
async def on_member_ban(member):
    if config["configuration"]["antiban"] == "enabled":
        logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
        if logs.member_id != bot.id:
          pass
            
@bot.command(pass_context=True)
async def lockdown(ctx, channel: discord.TextChannel):
    the_channel = bot.get_channel(channel.id)
    await the_channel.set_permissions(ctx.guild.default_role, send_messages=False)
    embed = discord.Embed(title="❌ This channel is now in lockdown ❌", color=0xff0000)
    await channel.send(embed=embed)

@bot.command(pass_context=True)
async def unlock(ctx, channel: discord.TextChannel):
    the_channel = bot.get_channel(channel.id)
    await the_channel.set_permissions(ctx.guild.default_role, send_messages=True)
    embed = discord.Embed(title="✅ This channel is now unlocked ✅", color=0x1dff00)
    await channel.send(embed=embed)
    
bot.run(token)
