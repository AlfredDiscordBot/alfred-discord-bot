import json

import requests

headers = {"Authorization": "Bearer api_AcOKHoiOVBdLvXfmDDPgOVGXasDmzgUkFF"}
API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"

def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))

data = query(
    {
        "inputs": {
            "past_user_inputs": ["die"],
            "generated_responses": ["no i wont"],
            "text": "Can you explain why ?",
        },
        
        "parameters": {"temperature":2.0, "repetition_penalty": 2.5},
    }
)

print(data)




print(len(re))

@client.command()
async def changeM(ctx, *, num):
    if str(ctx.author.id) in dev_users:
        num = int(num)

        if num == 1:
            re[10] = 1
            await ctx.send(
                        embed=discord.Embed(
                            title="Model change",
                            description="Changed to blenderbot",
                            color=discord.Color(value=re[8]),
                        ))
        elif num == 2:
            re[10]=2
            await ctx.send(
                        embed=discord.Embed(
                            title="Model change",
                            description="Changed to dialo-gpt",
                            color=discord.Color(value=re[8]),
                        ))
        else:

            await ctx.send(
                        embed=discord.Embed(
                            title="Model change",
                            description="Bruh thats not a valid option",
                            color=discord.Color(value=re[8]),
                        ))

    else:
        await ctx.send(
                        embed=discord.Embed(
                            title="Model change",
                            description="F off thout isn't un dev user",
                            color=discord.Color(value=re[8]),
                        ))
