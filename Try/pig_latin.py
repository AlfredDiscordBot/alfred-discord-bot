  
def requirements():
    return "re"
def main(client,re):
    import discord
    from discord.ext import commands
    @client.command()
    async def eng2pig(ctx,*, data):
      a = str(data)
      a = a.lower()
      a = a + a[0]+'ay'
      a = list(a)
      a.remove(a[0])

      a = ''.join(a)
      await ctx.send(embed=discord.Embed(title="igpay atinlay",description=eval(str(t.content.decode()))[a], color=discord.Color(value=re[8])))
   @client.command()
    async def pig2eng(ctx,*, data):
      b = data.lower()
      for i in range(1, 3):
          b = b[:-1]

      b =  b[len(b)-1]+b[0:len(b)-1]
      await ctx.send(embed=discord.Embed(title="English Again",description=eval(str(t.content.decode()))[a], color=discord.Color(value=re[8])))
