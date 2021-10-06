import requests
import traceback
import json
from typing import List, Dict, Union
from functools import lru_cache


class CodeExecutor:
    """
    Base class for code executing utilities.
    """

    def __init__(self) -> None:
        self.runtimes = self.get_runtimes()

    @staticmethod
    def get_runtimes() -> List[Dict[str, Union[str, List[str]]]]:
        """
        Returns a list of all available runtimes in the piston api.
        """
        try:
            runtime_url = "https://emkc.org/api/v2/piston/runtimes"
            r = requests.get(runtime_url)
            data = json.loads(r.text)
            runtimes: List[Dict[str, Union[str, List[str]]]] = []
            for langs in data:
                runtimes.append(
                    {
                        "language": langs["language"],
                        "version": langs["version"],
                        "aliases": [i for i in langs["aliases"]],
                    }
                )

            return runtimes

        except Exception as e:
            traceback.print_exc(e)

    @lru_cache(maxsize=50)
    def execute_code(self, language: str, code: str) -> str:
        """
        Executes the given code in the given language and version.
        """
        try:
            execute_url = "https://emkc.org/api/v2/piston/execute"
            all_langs = [runtime["language"] for runtime in self.runtimes]
            _aliases = [runtime["aliases"] for runtime in self.runtimes]
            aliases = [i for sublist in _aliases for i in sublist]

            if language not in all_langs and language not in aliases:
                return f"Language {language} is not supported."

            for runtime in self.runtimes:
                if runtime["language"] == language or language in runtime["aliases"]:
                    version = runtime["version"]
                    break

            payload = {
                "language": language,
                "version": version,
                "files": [
                    {
                        "name": "prog",
                        "content": code,
                    }
                ],
            }

            resp = requests.post(execute_url, json=payload)

            if resp.status_code == 200:
                data = json.loads(resp.text)

                run_data = data["run"]

                return f"""
Exit Code: {run_data["code"]}

Output:
```
{run_data["output"]}
```
                """

            else:
                return f"Error: {resp.status_code}"

        except Exception as e:
            traceback.print_exc(e)
            return "Couldn't connect at the moment."


history = {}


def filter_graves(code):
    actual_code = ""
    for i in code.split("\n"):
        if not i.startswith("```"):
            actual_code += i + "\n"
    return actual_code


def requirements():
    return ["re[8]"]


def main(client, color):
    rce = CodeExecutor()
    import discord

    @client.command()
    async def code(ctx, lang, *, code):
        actual_code = filter_graves(code)
        output = rce.execute_code(language=lang, code=actual_code)
        embed = discord.Embed(
            title="Result", description=output, color=discord.Color(value=color)
        )
        embed.set_thumbnail(url=client.user.avatar_url_as(format="png"))
        embed.set_footer(text="Result from https://emkc.org/")
        await ctx.send(embed=embed)

    @client.event
    async def on_message_edit(message_before, message_after):
        if message_after.content.startswith("'code"):
            a = message_after.content.split("\n")[0]
            language = a[a.find("'code") + len("'code ") :]
            actual_code = filter_graves(
                message_after.content[message_after.content.find("\n") + 1 :]
            )
            output = rce.execute_code(language=language, code=actual_code)
            embed = discord.Embed(
                title="Result", description=output, color=discord.Color(value=color)
            )
            embed.set_thumbnail(url=client.user.avatar_url_as(format="png"))
            embed.set_footer(text="Result from https://emkc.org/")
            await message_after.channel.send(embed=embed)


# if __name__ == "__main__":
#     rce = CodeExecutor()
#     # print(rce.runtimes)
#     print(rce.execute_code(language="vlang", code="println('hello')"))
#     print(rce.execute_code(language="vlang", code="println('hello')"))
