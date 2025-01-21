import os
import discord
import json

from discord.ext import commands

from syntax.badcop import syntax_badcop


client = commands.Bot(command_prefix="!", self_bot=True)
bot_is_ready: bool = False
global_settings: dict = {}

syntax: dict = {
    "badcop.txt": syntax_badcop
}

with open("settings.json", "r", encoding="utf-8") as f:
    bot_settings: dict = json.load(f)

with open(f"parameters/{bot_settings['core']}", "r", encoding="utf-8") as f:
    global_settings["prompt"] = f.read()

global_settings["original_message"] = None
global_settings["temp_messages"] = []


@client.event
async def on_ready():
    """
    Delete the clyde channel and create a new one.
    """

    channel: discord.TextChannel = client.get_channel(bot_settings["clyde_channel"])
    await channel.delete()

    guild = client.get_guild(bot_settings["guild_id"])
    clyde_channel = await guild.create_text_channel("clyde")

    bot_settings["clyde_channel"] = clyde_channel.id

    with open("settings.json", "w", encoding="utf-8") as f:
        json.dump(bot_settings, f, indent=4)



@client.event
async def on_message(message: discord.Message) -> None:
    print(global_settings["temp_messages"])
    if (not message.channel.id == bot_settings["clyde_channel"] and
        not message.author.id == bot_settings["self_id"] and 
        not message.author.id == bot_settings["clyde_id"]):

        # Temp memory reset.
        if len(global_settings["temp_messages"]) >= bot_settings["temp_reset"]:
            for i in range(len(global_settings["temp_messages"]) - 1):
                m: discord.Message = global_settings["temp_messages"].pop(i)
                m.delete()
            
            print(f"Array Now: {global_settings['temp_messages']}")

        global_settings["original_message"]: discord.Message = message
        clyde_channel = client.get_channel(bot_settings["clyde_channel"])

        prompt: str = global_settings['prompt'].replace('%prompt%', message.content)
        temp_message: discord.Message = await clyde_channel.send(f"<@{bot_settings['clyde_id']}> {prompt}")

        global_settings["temp_messages"].append(temp_message)
    
    elif message.author.id == bot_settings["clyde_id"]:
        if syntax.get(bot_settings["core"]):
            await global_settings["original_message"].reply(syntax[bot_settings['core']](message.content))

        else:
            await global_settings["original_message"].reply(message.content)



if __name__ == "__main__":
    client.run(bot_settings["client_token"])