import discord
import logging
import json
import random
import os
from discord.ext import commands
from cogs import inventory
from open_case import open_case

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix="=", description="A new bot made by Nexus Novaz#0862")

# ON READY PRINT
@bot.event
async def on_ready():
	print(f'''
-------------------------------------------------
|		Logged In!
|		Name: {bot.user}
|		ID: {bot.user.id}
|		Discord Version: {discord.__version__}
|		Im Online!
-------------------------------------------------
	''')
# END ON READY PRINT

# ON MEMBER JOIN
@bot.listen()
async def on_member_join(member):
    await member.edit(nick="LVL 1 | "+ member.name)
# END ON MEMBER JOIN

# COGS

class Member():
	@commands.command()
	async def joined(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.message.author

		await ctx.send(f'{member} joined at {member.joined_at}')

#class Mod():

#class Admin():

#class Owner():

# END OF COGS

# COMMANDS

# MY COMMANDS ONLY

#@bot.

# END OF MY COMMANDS

@bot.command()
async def myinv(ctx, page = 1):
	# await client.say(inventory.get_price("AK-47", "Frontside Misty", "Minimal Wear"))
	await ctx.send(embed = inventory.get_embed(ctx.message.author.id, page) )

@bot.command()
async def openCase(ctx, case=""):
	if case.lower() == "list" or case == "":
		cases = os.listdir("cases")
		case_str = ""
		for casename in cases:
			if casename != "blank.json":
				case_str += casename[:-5] + "\n"
		await ctx.send(case_str)
	else:
		weapon = open_case(case.lower())
		if isinstance(weapon, str):
			await ctx.send(weapon)
		else:
			inventory.write(ctx.message.author.id, weapon)
			if weapon["StatTrack"] == True:
				drop = discord.Embed(title = "@" + ctx.message.author.name + " unboxed:", description=weapon["weapon"] + " | " + weapon["skin"] + "\n" + "StatTrack", color = int(weapon["color"], 16))
			else:
				drop = discord.Embed(title = "@" + ctx.message.author.name + " unboxed:", description=weapon["weapon"] + " | " + weapon["skin"], color = int(weapon["color"], 16))

			drop.set_image(url = weapon["icon"])
			drop.add_field(name = "**Condition**", value = weapon["condition"], inline = True)
			drop.add_field(name = "**Float**", value = weapon["float"]["value"], inline = True)
			drop.add_field(name = "**Case:**", value = weapon["case"], inline = True)
			# drop.add_field(name = "**Price**", value = get_price(2, weapon["weapon"], weapon["skin"], weapon["condition"])["lowest_price"] + " | " + get_price(3, weapon["weapon"], weapon["skin"], weapon["condition"])["lowest_price"])
			await ctx.send(embed = drop)

# END COMMANDS

bot.add_cog(Member())

bot.run(os.environ['TOKEN'])
