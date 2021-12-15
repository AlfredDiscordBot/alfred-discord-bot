from discord.ext import commands
import asyncio
import cloudscraper
import requests
import traceback
import os
import discord
from main_program import entr, re
from External_functions import cembed
from discord_slash import cog_ext, SlashContext


class Entrar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def entrar(self, ctx, *, num=re[6]):
        print("Entrar", str(ctx.author))
        re[0] = re[0] + 1
        lol = ""
        header = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/88.0.4324.182 Safari/537.36",
            "referer": "https://entrar.in",
        }
        suvzsjv = {
            "username": os.getenv("sjdoskenv"),
            "password": os.getenv("sjdoskenv1"),
            "captcha": "0",
        }
        announcement_data = dict({"announcementlist": "true", "session": "205"})
        re[6] = num
        announcement_data["session"] = str(num)
        # class="label-input100"
        try:
            with requests.Session() as s:
                scraper = cloudscraper.create_scraper(sess=s)
                r = scraper.get("https://entrar.in/login/login", headers=header)
                st = r.content.decode()
                start_captcha = st.find(
                    '<span class="label-input100" style="font-size: 18px;">'
                ) + len('<span class="label-input100" style="font-size: 20px;">')
                end_captcha = st.find("=", start_captcha)
                suvzsjv["captcha"] = str(eval(st[start_captcha:end_captcha]))
                url = "https://entrar.in/login/auth/"
                r = scraper.post(url, data=suvzsjv, headers=header)
                r = scraper.get("https://entrar.in/", headers=header)
                r = scraper.post(
                    "https://entrar.in/parent_portal/announcement", headers=header
                )
                r = scraper.get(
                    "https://entrar.in/parent_portal/announcement", headers=header
                )
                await asyncio.sleep(2)
                r = scraper.post(
                    "https://entrar.in/parent_portal/announcement",
                    data=announcement_data,
                    headers=header,
                )
                channel = discord.utils.get(ctx.guild.channels, name="announcement")
                if ctx.guild.id == 727061931373887531:
                    channel = discord.utils.get(ctx.guild.channels, name="bot")
                elif ctx.guild.id == 743323684705402951:
                    channel = self.bot.get_channel(868085346867490866)
                st = r.content.decode()
                for i in range(1, 5):
                    await asyncio.sleep(1)
                    a = st.find('<td class="text-wrap">' + str(i) + "</td>")
                    b = st.find('<td class="text-wrap">' + str(i + 1) + "</td>")
                    print(a, b)
                    le = len('<td class="text-wrap">' + str(i + 1) + "</td>") - 1
                    if b == -1:
                        await ctx.send(
                            embed=discord.Embed(
                                title="End Of List",
                                description="",
                                color=discord.Color(value=re[8]),
                            )
                        )
                        break
                    c = st.find("&nbsp;&nbsp; ", a, b) + len("&nbsp;&nbsp; ")
                    d = st.find("<", c, b)
                    out = st[c:d].strip()
                    e = a + le
                    f = st.find("<td>", e, e + 15) + len("<td>")
                    g = st.find("</td>", e, e + 45)
                    date = st[f:g]
                    h = st.find('<a target="_blank" href="', a, b) + len(
                        '<a target="_blank" href="'
                    )
                    j = st.find('"', h, b)
                    try:
                        link = str(st[h:j])
                        print(link)
                        if (
                                link
                                == 'id="simpletable" class="table table-striped table-bordered nowrap'
                        ):
                            continue
                        req = scraper.get(link)
                        k = out + date
                        if not str(ctx.guild.id) in entr:
                            entr[str(ctx.guild.id)] = []
                        if k in entr[str(ctx.guild.id)]:
                            continue
                        entr[str(ctx.guild.id)].append(str(k))
                        lol = lol + out + " Date:" + date + "\n"
                        with open((out + ".pdf"), "wb") as pdf:
                            pdf.write(req.content)
                            await channel.send(file=discord.File(out + ".pdf"))
                            pdf.close()
                        os.remove(out + ".pdf")
                    except Exception as e:
                        print(traceback.print_exc())
                if lol != "":
                    embed = discord.Embed(
                        title="New announcements",
                        description=lol,
                        color=discord.Color(value=re[8]),
                    )
                    embed.set_thumbnail(url="https://entrar.in/logo_dir/entrar_white.png")
                    await channel.send(embed=embed)
                    await ctx.send("Done")
                else:
                    await channel.send(
                        embed=discord.Embed(
                            title="Empty",
                            description="No new announcement",
                            color=discord.Color(value=re[8]),
                        )
                    )
                    await ctx.send("Done")
        except Exception as e:
            await ctx.send(
                embed=cembed(
                    title="Oops",
                    description="Something went wrong\n" + str(e),
                    color=re[8],
                    thumbnail="https://entrar.in/logo_dir/entrar_white.png",
                )
            )

    @cog_ext.cog_slash(name="entrar", description="Latest announcements from Entrar")
    async def yentrar(self, ctx: SlashContext, *, num=re[6]):
        await ctx.defer()
        await self.entrar(ctx)

def setup(client):
    client.add_cog(Entrar(client))
