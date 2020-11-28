import discord
import random
from discord.ext import commands

class Info(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(name='ping', aliases=['latency'], help='Pong!')
	async def ping(self, ctx):
		embed=discord.Embed(title='Pong!', 
			description=f'Ping = {round(self.client.latency * 1000)}ms', 
			colour=random.randint(0,0xffffff)
		)
		embed.set_footer(text=f'Requested by {ctx.author}')
		await ctx.send(embed=embed)

	@commands.command(name='avatar', aliases=['av','profile', 'pfp'], help='Sends the Avatar of the Mentioned User. If no one is mentioned then sends the Avatar of the Author.')
	async def avatar(self, ctx, *, target: discord.Member = None):
		embed=discord.Embed(title='Avatar', colour=random.randint(0,0xffffff))
		if target == None:
			pfp_url = ctx.message.author.avatar_url
			embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
		else:
			pfp_url = target.avatar_url
			embed.set_author(name=target, icon_url=target.avatar_url)
		embed.set_image(url=pfp_url)
		embed.set_footer(text="Requested by {}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
		await ctx.send(embed=embed)
	
	@commands.command(name='about', help='About the bot!')
	async def about(self, ctx):
		aboutEmbed = discord.Embed(title = "About SleepBot",
			description="SleepBot is a custom coded and open source bot made by <@!515097702057508882> for Clinify.in Discord Server. It is writen in Python and uses discord.py library.", 
			colour = random.randint(0, 0xffffff))
		aboutEmbed.set_thumbnail(url=self.client.user.avatar_url)
		aboutEmbed.add_field(name="Contribute to SleepBot!", 
			value="SleepBot is an Open Source bot with it's source code available [here](https://github.com/ZeusAbhijeet/SleepBot). You are free to contribute to it!",
			inline=False
		)
		aboutEmbed.add_field(name="Contributors!",
			value="**Thank you to the following people for contributing:**\n1. [itsCharmander](https://github.com/itsCharmander)\n2. [AryaKesharwani](https://github.com/AryaKesharwani)",
			inline=False
		)
		aboutEmbed.set_footer(text="Requested by {}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
		await ctx.send(embed=aboutEmbed)
		

def setup(client):
	client.add_cog(Info(client))
