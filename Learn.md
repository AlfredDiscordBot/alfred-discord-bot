# Information

Hey guys, I've build this bot for a good cause and if you want to contribute to this, you may need to know one or two things about Nextcord and a lot about Python

We try to make Alfred fully async, and sometimes couldn't succeed because of certain errors and limitations in the aiohttp module(Use for async requests). But it is a must to make sure that all the functions you create must be asynchronous as much as possible


## Files and folder structure

- In requirements.txt, nextcord is set in a way that it updates whenever there's a restart without specifying the version
- External Functions, this file has been moved to the Utils folder for a purpose, this file is just a support to the main_program.py, so basically all the support functions and classes can go into this, like if you see the class Meaning or ProtonDB, this can be accessed as
- Assets.py is a new file created, which currently contains interaction components and emotes class, So if you want to pick let's say something like the upvote emoji, you can use assets.Emotes(client).upvote
- Helping hand has the help page embeds, you can go through it, it's not much to know about
- Post.py and spotify clients are helpers, post.py is for instagram

## Here are some important functions that you'll see

- cembed()  Easier way for creating an embed, you can give title, color(value or nextcord.Color), etc
- pa1()     Made a function for pages, this function is used in help and FUN APIs. Pass in embeds, ctx as parameters

## Commands and slash commands

### Here's how you create a normal command
```py
@client.command(aliases = ['b'])
async def command_name(ctx, arg1, arg2, arg3, *, args):
  '''
  Ctx or as people call it, context is an important parameter
  It's compulsory and it comes in the beginning
  It has most of the info like channel/user IDS, if you're a developer of Alfred
  Check it out using dir(ctx)
  '''
  #to send a message
  await ctx.send("text")
  await ctx.send(embed=cembed(description='Hello'))
  #over here, you can do anything and the function will be called
```

### Here's how you create a slash command

```py
@client.slash_command(name="name",description="This is a slash command")
async def sl(ctx: nextcord.Interaction, arg1, default_arg = "Here"):
  '''
  We may have named it ctx,
  but this is not the same as context in the regular command as you've seen above
  This is a little different from that, this is Interaction
  User is used instead of author
  Has an attribute called response
  and original message
  '''
  await ctx.send("Hellow world")
  #To edit a message
  await ctx.response.edit_message("Hello world")
```

**WARNING: PLEASE DON'T COPY PASTE THIS CODE AS IT'S INDENTATION IS ONLY 2 SPACES, ALFRED BY DEFAULT USES 4 AND IF YOU DO, IT COULD MESS YOUR EDIT AND WILL HAVE TO REMOVE THE LINES OR RESET** 
