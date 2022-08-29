from dataclasses import dataclass
from io import BytesIO

import nextcord
from nextcord import SlashOption
from nextcord.ext import commands

import datetime

from PIL import Image, ImageDraw, ImageFont

from utils.External_functions import get_async, cembed


@dataclass
class Theme:
    background: str
    text: str
    meta: str
    grade4: str
    grade3: str
    grade2: str
    grade1: str
    grade0: str


themes = {
    "standard": Theme(
        background="#ffffff",
        text="#000000",
        meta="#666666",
        grade4="#216e39",
        grade3="#30a14e",
        grade2="#40c463",
        grade1="#9be9a8",
        grade0="#ebedf0",
    ),
    "classic": Theme(
        background="#ffffff",
        text="#000000",
        meta="#666666",
        grade4="#196127",
        grade3="#239a3b",
        grade2="#7bc96f",
        grade1="#c6e48b",
        grade0="#ebedf0",
    ),
    "github_dark": Theme(
        background="#101217",
        text="#ffffff",
        meta="#dddddd",
        grade4="#27d545",
        grade3="#10983d",
        grade2="#00602d",
        grade1="#003820",
        grade0="#161b22",
    ),
    "halloween": Theme(
        background="#ffffff",
        text="#000000",
        meta="#666666",
        grade4="#03001C",
        grade3="#FE9600",
        grade2="#FFC501",
        grade1="#FFEE4A",
        grade0="#ebedf0",
    ),
    "teal": Theme(
        background="#ffffff",
        text="#000000",
        meta="#666666",
        grade4="#458B74",
        grade3="#66CDAA",
        grade2="#76EEC6",
        grade1="#7FFFD4",
        grade0="#ebedf0",
    ),
    "left_pad": Theme(
        background="#000000",
        text="#ffffff",
        meta="#999999",
        grade4="#F6F6F6",
        grade3="#DDDDDD",
        grade2="#A5A5A5",
        grade1="#646464",
        grade0="#2F2F2F",
    ),
    "dracula": Theme(
        background="#181818",
        text="#f8f8f2",
        meta="#666666",
        grade4="#ff79c6",
        grade3="#bd93f9",
        grade2="#6272a4",
        grade1="#44475a",
        grade0="#282a36",
    ),
    "blue": Theme(
        background="#181818",
        text="#C0C0C0",
        meta="#666666",
        grade4="#4F83BF",
        grade3="#416895",
        grade2="#344E6C",
        grade1="#263342",
        grade0="#222222",
    ),
    "panda": Theme(
        background="#2B2C2F",
        text="#E6E6E6",
        meta="#676B79",
        grade4="#FF4B82",
        grade3="#19f9d8",
        grade2="#6FC1FF",
        grade1="#34353B",
        grade0="#242526",
    ),
    "sunny": Theme(
        background="#ffffff",
        text="#000000",
        meta="#666666",
        grade4="#a98600",
        grade3="#dab600",
        grade2="#e9d700",
        grade1="#f8ed62",
        grade0="#fff9ae",
    ),
    "pink": Theme(
        background="#ffffff",
        text="#000000",
        meta="#666666",
        grade4="#61185f",
        grade3="#a74aa8",
        grade2="#ca5bcc",
        grade1="#e48bdc",
        grade0="#ebedf0",
    ),
    "YlGnBu": Theme(
        background="#ffffff",
        text="#000000",
        meta="#666666",
        grade4="#253494",
        grade3="#2c7fb8",
        grade2="#41b6c4",
        grade1="#a1dab4",
        grade0="#ebedf0",
    ),
    "solarized_dark": Theme(
        background="#002b36",
        text="#93a1a1",
        meta="#586e75",
        grade4="#d33682",
        grade3="#b58900",
        grade2="#2aa198",
        grade1="#268bd2",
        grade0="#073642",
    ),
    "solarized_light": Theme(
        background="#fdf6e3",
        text="#586e75",
        meta="#93a1a1",
        grade4="#6c71c4",
        grade3="#dc322f",
        grade2="#cb4b16",
        grade1="#b58900",
        grade0="#eee8d5",
    ),
}


def requirements():
    return []


class Contribution(commands.Cog):
    def __init__(self, CLIENT):
        self.client = CLIENT
        self.contributions = Contributions()
        self.CACHE_DATA = {}

    @nextcord.slash_command(
        name="contribution", description="Get GitHub Contribution of a user"
    )
    async def contribution(
        self,
        inter: nextcord.Interaction,
        username: str = SlashOption(description="Github username"),
        theme: str = SlashOption(
            name="theme",
            required=False,
            description="The theme of the contribution graph",
            choices=dict((k, k) for k in themes.keys()),
        ),
    ):
        await inter.response.defer()
        theme = theme or "classic"
        data = await get_async(
            f"https://github-contributions.vercel.app/api/v1/{username}", kind="json"
        )
        self.contributions.new(data, themes[theme])
        self.contributions.draw_contributions(
            {
                "username": username,
                "footerText": f"Github Contributions Graph Provided by {str(self.client.user)}",
            }
        )

        with BytesIO() as img:
            self.contributions.image.save(img, format="PNG")
            description = []
            for year in data.get("years"):
                description.append(
                    "`{year}: ` {total} contributions".format(
                        year=year.get("year"), total=year.get("total")
                    )
                )
            img.seek(0)
            file = nextcord.File(fp=img, filename=f"{username}_contributions.png")
            await inter.send(
                embed=cembed(
                    title="Contributions",
                    image="attachment://{}_contributions.png".format(username),
                    color=self.client.color(inter.guild),
                    footer={
                        "text": "If you find any issue with this command, please use /feedback",
                        "icon_url": self.client.user.avatar,
                    },
                    author=inter.user,
                    description=description,
                ),
                file=file,
            )


def setup(client, **i):
    client.add_cog(Contribution(client, **i))


def start_week(date: datetime.datetime):
    return date + datetime.timedelta(days=date.weekday())


class Contributions:
    DATE_FORMAT = "%Y-%m-%d"
    BOX_WIDTH = 15
    BOX_MARGIN = 5
    TEXT_HEIGHT = 15
    HEADER_HEIGHT = 60
    CANVAS_MARGIN = 20
    YEAR_HEIGHT = TEXT_HEIGHT + (BOX_MARGIN + BOX_WIDTH) * 8 + CANVAS_MARGIN
    SCALE_FACTOR = 1

    def __init__(self):
        self.data = None
        self.theme = themes["classic"]
        self.height = 0
        self.width = 0
        self.image = None
        self.draw = None
        self.year_font = ImageFont.truetype(
            "utils/fonts/SourceCodePro-Semibold.ttf", 10
        )
        self.username_font = ImageFont.truetype(
            "utils/fonts/SourceCodePro-Semibold.ttf", 20
        )

    def new(self, _data, theme: Theme):
        self.data = _data
        self.theme = theme
        self.height = (
            len(self.data["years"]) * self.YEAR_HEIGHT
            + self.CANVAS_MARGIN
            + self.HEADER_HEIGHT
            + self.BOX_WIDTH
        )
        self.width = 53 * (self.BOX_WIDTH + self.BOX_MARGIN) + self.CANVAS_MARGIN * 2
        self.image = Image.new("RGBA", (self.width, self.height), self.theme.background)
        self.draw = ImageDraw.Draw(self.image)

    def get_date_info(self, date: str):
        h = list(filter(lambda x: x["date"] == date, self.data["contributions"]))
        return h[0] if h else None

    @staticmethod
    def get_contribution_count(entries):
        row_total = 0
        for row in entries:
            total = 0
            for col in row:
                total += col["info"]["count"] if col["info"] else 0
            row_total += total
        return row_total

    def draw_year(self, opts):
        year, offset_x, offset_y = opts["year"], opts["offsetX"], opts["offsetY"]

        today = datetime.datetime.today()
        this_year = str(today.year)
        last_date = (
            today
            if year["year"] == this_year
            else datetime.datetime.fromisoformat(year["range"]["end"])
        )
        first_real_date = datetime.datetime.fromisoformat(f"{year['year']}-01-01")
        first_date = start_week(first_real_date)

        next_date = first_date

        first_row_entries = []
        graph_entries = []

        while next_date <= last_date:
            next_date_str = next_date.strftime(self.DATE_FORMAT)
            first_row_entries.append(
                {"date": next_date_str, "info": self.get_date_info(next_date_str)}
            )

            next_date += datetime.timedelta(weeks=1)

        graph_entries.append(first_row_entries)

        def map_dates(date_obj, d):
            my_date = datetime.datetime.fromisoformat(date_obj["date"])
            monday = my_date - datetime.timedelta(days=my_date.weekday())
            my_date = (monday + datetime.timedelta(days=d)).strftime(self.DATE_FORMAT)
            return {"date": my_date, "info": self.get_date_info(my_date)}

        for i in range(1, 7):
            graph_entries.append(
                list(map(lambda x: map_dates(x, i), first_row_entries))
            )

        count = self.get_contribution_count(graph_entries)

        self.draw.text(
            (offset_x, offset_y - 17),
            f"{year['year']}: {count} Contribution{'' if year['total'] == 1 else 's'}{' (so far) ' if this_year == year['year'] else ''}",
            fill=self.theme.text,
            font=self.year_font,
        )

        for y in range(0, len(graph_entries)):
            for x in range(0, len(graph_entries[y])):
                day = graph_entries[y][x]
                cell_date = datetime.datetime.fromisoformat(day["date"])
                if cell_date >= last_date or not day["info"]:
                    continue

                color = getattr(self.theme, f"grade{day['info']['intensity']}", None)

                w, h = offset_x + x * (
                    self.BOX_WIDTH + self.BOX_MARGIN
                ), offset_y + self.TEXT_HEIGHT + y * (self.BOX_WIDTH + self.BOX_MARGIN)
                self.draw.rounded_rectangle(
                    (w, h, w + self.BOX_WIDTH, h + self.BOX_WIDTH), 1, fill=color
                )

        last_counted_month = 0
        for y in range(len(graph_entries[0])):
            date = datetime.datetime.fromisoformat(graph_entries[0][y]["date"])
            month = date.month
            first_month_is_dec = month == 12 and y == 0
            month_changed = month != last_counted_month

            if month_changed and not first_month_is_dec:
                self.draw.text(
                    (offset_x + y * (self.BOX_WIDTH + self.BOX_MARGIN), offset_y),
                    f"{date.strftime('%b')}",
                    fill=self.theme.text,
                    font=self.year_font,
                )
                last_counted_month = month

    def draw_metadata(self, opts):
        username, footer_text = opts["username"], opts["footerText"]
        self.draw.rectangle((0, 0, self.width, self.height), fill=self.theme.background)

        if footer_text:
            self.draw.text(
                (self.CANVAS_MARGIN, self.height - 5 - self.TEXT_HEIGHT),
                footer_text,
                fill=self.theme.meta,
                font=self.year_font,
            )

        theme_grades = 5
        self.draw.text(
            (
                self.width
                - self.CANVAS_MARGIN
                - (self.BOX_WIDTH + self.BOX_MARGIN) * theme_grades
                - 55,
                self.BOX_WIDTH + self.TEXT_HEIGHT,
            ),
            "Less",
            fill=self.theme.text,
            font=self.year_font,
        )
        self.draw.text(
            (self.width - self.CANVAS_MARGIN - 25, self.BOX_WIDTH + self.TEXT_HEIGHT),
            "More",
            fill=self.theme.text,
            font=self.year_font,
        )

        for i, grade in enumerate(range(theme_grades)):
            fill = getattr(self.theme, f"grade{grade}", None)
            w, h = (
                self.width
                - self.CANVAS_MARGIN
                - (self.BOX_WIDTH + self.BOX_MARGIN) * (theme_grades - i)
                - 27,
                self.TEXT_HEIGHT + self.BOX_WIDTH,
            )
            self.draw.rounded_rectangle(
                (w, h, w + self.BOX_WIDTH, h + self.BOX_WIDTH), 1, fill
            )

        self.draw.text(
            (self.CANVAS_MARGIN, self.CANVAS_MARGIN),
            f"@{username} on GitHub",
            fill=self.theme.text,
            font=self.username_font,
        )
        self.draw.line(
            [(self.CANVAS_MARGIN, 55), (self.width - self.CANVAS_MARGIN, 55)],
            fill=self.theme.grade0,
        )

    def draw_contributions(self, opts):
        self.draw_metadata({**opts, "width": self.width, "height": self.height})

        for i, year in enumerate(self.data["years"]):
            offset_y = self.YEAR_HEIGHT * i + self.CANVAS_MARGIN + self.HEADER_HEIGHT
            offset_x = self.CANVAS_MARGIN
            self.draw_year(
                {**opts, "year": year, "offsetX": offset_x, "offsetY": offset_y}
            )
