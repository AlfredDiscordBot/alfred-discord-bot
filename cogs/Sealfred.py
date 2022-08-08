import nextcord
import utils.External_functions as ef
from nextcord.ext import commands

# Use nextcord.slash_command()


def requirements():
    return []


class Sealfred(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    async def action(self, audit_log: list):
        if user := ef.audit_check(audit_log):
            await user.remove_roles(user.roles)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id in self.CLIENT.config["security"]:
            a = member.guild
            audit_log = await a.audit_logs(limit=10).flatten()
            await self.action(audit_log=audit_log)
            latest = audit_log[0]
            if latest.target == member:
                channel = self.CLIENT.get_channel(
                    self.CLIENT.config["security"][member.guild.id]
                )
                if latest.action == nextcord.AuditLogAction.ban:
                    await channel.send(
                        embed=ef.cembed(
                            title=f"Banned",
                            description=f"{latest.user.mention} banned {latest.target.name}",
                            color=self.CLIENT.color(a),
                            footer="Security alert by Alfred",
                            thumbnail=a.icon,
                        )
                    )
                elif latest.action == nextcord.AuditLogAction.kick:
                    await channel.send(
                        embed=ef.cembed(
                            title=f"Kicked",
                            description=f"{latest.user.mention} kicked {latest.target.name}",
                            color=self.CLIENT.color(a),
                            footer="Security alert by Alfred",
                            thumbnail=a.icon,
                        )
                    )

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if channel.guild.id in self.CLIENT.config["security"]:
            guild = channel.guild
            audit_log = await guild.audit_logs(limit=10).flatten()
            await self.action(audit_log=audit_log)
            await self.CLIENT.get_channel(
                self.CLIENT.config["security"][guild.id]
            ).send(
                embed=ef.cembed(
                    title="Channel Delete",
                    author=audit_log[0].user,
                    footer="Security alert by Alfred",
                    thumbnail=guild.icon,
                    description=f"{audit_log[0].user.mention} deleted the channel {channel.name}",
                    color=self.CLIENT.color(guild),
                )
            )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id in self.CLIENT.config["security"]:
            audit_log = await member.guild.audit_logs(limit=10).flatten()
            latest = audit_log[0]
            if member.bot:
                channel = self.CLIENT.get_channel(
                    self.CLIENT.config["security"][member.guild.id]
                )
                if channel:
                    await channel.send(
                        embed=ef.cembed(
                            title="Bot added",
                            description=f"{latest.target.mention} was added by {latest.user.mention}, please be careful while handling bots and try not to provide it with all the permissions as it can be dangerous",
                            color=self.CLIENT.color(member.guild),
                            author=latest.user,
                            footer="Security alert by Alfred",
                        )
                    )


def setup(client, **i):
    client.add_cog(Sealfred(client, **i))
