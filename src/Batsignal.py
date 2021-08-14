def requirements():
    return "re"
def main(client,re):
    from gi.repository import Notify
    @client.command()
    async def batsignal(ctx):
        #https://c.tenor.com/0GJ-XEcYLfcAAAAd/wongwingchun58.gif
        alvin=client.get_user(432801163126243328).mention        
        await ctx.send(str(alvin)+ "You've been summoned by "+ctx.author.name)
        await ctx.send("https://c.tenor.com/0GJ-XEcYLfcAAAAd/wongwingchun58.gif")
        ping(ctx)
    def ping(ctx):
        Notify.init("Alfred")
        notification=Notify.Notification.new("Ping from "+ctx.guild.name,"You've been summoned by "+ctx.author.name,"/home/alvinbengeorge/Desktop/Discord_Python/Emerald.png")
        notification.show()
        Notify.uninit()
                                             
        
