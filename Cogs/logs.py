import discord
import asyncio
import json

from discord.ext import commands
from discord.utils import get
from discord.ext.commands import has_permissions

# ------------------------ COGS ------------------------ #


class LogsCog(commands.Cog, name="change setting from logs command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #

    @commands.command(name='logs',
                      aliases=["log", "setlog", "setlogs", "logchannel"],
                      usage="<true/false>",
                      description="ログシステムを有効にするかどうか設定します")
    @has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def logs(self, ctx, logChannel):

        logChannel = logChannel.lower()

        if logChannel == "true":
            # Create channel
            logChannel = await ctx.guild.create_text_channel(f"{self.bot.user.name}-logs")
            await logChannel.set_permissions(ctx.guild.default_role, read_messages=False)

            # Edit configuration.json
            with open("configuration.json", "r") as config:
                data = json.load(config)
                # Add modifications
                data["logChannel"] = logChannel.id
                newdata = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(
                title=f"**設定しました**", description=f"ログを出すチャンネルを設定しました。", color=0x2fa737)  # Green
        else:
            # Read configuration.json
            with open("configuration.json", "r") as config:
                data = json.load(config)

            # Delete
            logChannel = self.bot.get_channel(data["logChannel"])
            await logChannel.delete()

            # Add modifications
            data["logChannel"] = False
            newdata = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(
                title=f"**解除しました**", description=f"ログを出すチャンネルの設定を解除しました", color=0xe00000)  # Red

        await ctx.channel.send(embed=embed)

        with open("configuration.json", "w") as config:
            config.write(newdata)

# ------------------------ BOT ------------------------ #


def setup(bot):
    bot.add_cog(LogsCog(bot))
