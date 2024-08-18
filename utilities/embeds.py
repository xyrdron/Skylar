import discord

def embedCreate(title: str, description: str, color: discord.Color = discord.Color.default(), **fields) -> tuple:
    embed = discord.Embed(title=title, description=description, color=color)
    for name, value in fields.items():
        embed.add_field(name=name, value=value, inline=False)
    return embed # type: ignore

# this is how u make a goofy ahh embed
# message, embed = create_embed(
#     title="Example Embed",
#     description="This is an example embed.",
#     color=discord.Color.blue(),
#     msg_before="This is a message before the embed.",
#     Field1="This is field 1",
#     Field2="This is field 2"
# )
# print(message)  # This is a message before the embed.
# print(embed)    # <discord.embeds.Embed object at 0x...>
