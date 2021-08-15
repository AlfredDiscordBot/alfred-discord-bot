def requirements():
    return ""


def main(client):
    import discord
    from discord.ext import commands, tasks

    @client.command()
    async def getch(ctx, user_id):
        try:
            user = await client.fetch_user(user_id)
            await ctx.send(str(user))
        except Exception as e:
            await ctx.send(str(e))
