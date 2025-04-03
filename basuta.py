import discord
from discord import app_commands

intents = discord.Intents.default() 
intents.message_content = True

global 黒
黒=0
global M
M=0
global J
J=0
global 丼
丼=0
global PB
PB=0
global 婆
婆=0
global 綾
綾=0
global 日野
日野=0
global 鬼玉
鬼玉=0
global 怒涛バグなし
怒涛バグなし=0
global 怒涛バグあり
怒涛バグあり=0
global 紅白
紅白=0
global TOB
TOB=0
global ねいら
ねいら=0
global peバグなし
peバグなし=0
global peバグあり
peバグあり=0
global ソロ疾風なし
ソロ疾風なし=0
global ソロ疾風あり
ソロ疾風あり=0
global ソロ紅白
ソロ紅白=0
global ソロTOB
ソロTOB=0
global ソロねいら
ソロねいら=0
global ソロピンクなし
ソロピンクなし=0
global ソロピンクあり
ソロピンクあり=0
global ソロ鬼玉
ソロ鬼玉=0
global sippuu
sippuu=0
global kouhaku
kouhaku=0
global neira
neira=0
global tob
tob=0
global pinku
pinku=0

MY_GUILD = discord.Object(id=1039402401788076042)  # id=ギルドid

class MyClient(discord.client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
client = MyClient()

@client.event
async def on_ready():
    print("起動")

@client.tree.command(name="記録変更",description="鯖内最速記録変更")
@app_commands.describe(種類="更新する記録の種類",記録="更新する記録")
@app_commands.choices(種類=[
    app_commands.Choice(name="黒", value="黒"),
    app_commands.Choice(name="J", value="J"),
    app_commands.Choice(name="M", value="M"),
    app_commands.Choice(name="丼", value="丼"),
    app_commands.Choice(name="PB", value="PB"),
    app_commands.Choice(name="婆", value="婆"),
    app_commands.Choice(name="綾", value="綾"),
    app_commands.Choice(name="日野", value="日野"),
    app_commands.Choice(name="鬼玉", value="鬼玉"),
    app_commands.Choice(name="怒涛バグなし", value="怒涛バグなし"),
    app_commands.Choice(name="怒涛バグあり", value="怒涛バグあり"),
    app_commands.Choice(name="紅白", value="紅白"),
    app_commands.Choice(name="TOB", value="TOB"),
    app_commands.Choice(name="ねいら", value="ねいら"),
    app_commands.Choice(name="peバグなし", value="peバグなし"),
    app_commands.Choice(name="peバグあり", value="peバグあり"),
])
async def change(interaction:discord.Interaction,種類:str,記録:str):
    global 黒,J,M,丼,PB,婆,綾,日野,鬼玉,怒涛バグなし,怒涛バグあり,紅白,TOB,ねいら,peバグなし,peバグあり
    if 種類=="黒":
        黒=記録
        embed = discord.Embed(title="現在の鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="黒鬼",value=黒,inline=False)
        embed.add_field(name="レッドJ",value=J,inline=False)
        embed.add_field(name="マイティードッグ",value=M,inline=False)
        embed.add_field(name="どんどろ",value=丼,inline=False)
        embed.add_field(name="プリズンブレイカー",value=PB,inline=False)
        embed.add_field(name="Gババーン",value=婆,inline=False)
        embed.add_field(name="あやとりさま",value=綾,inline=False)
        embed.add_field(name="日ノ神",value=日野,inline=False)
        embed.add_field(name="極鬼玉集め",value=鬼玉,inline=False)
        embed.add_field(name="疾風怒濤(バグなし)",value=怒涛バグなし,inline=False)
        embed.add_field(name="疾風怒濤(バグあり)",value=怒涛バグあり,inline=False)
        embed.add_field(name="紅白ボス合戦",value=紅白,inline=False)
        embed.add_field(name="TOB",value=TOB,inline=False)
        embed.add_field(name="大妖魔ぬらねいら",value=ねいら,inline=False)
        embed.add_field(name="ピンクエンペラー(バグなし)",value=peバグなし,inline=False)
        embed.add_field(name="ピンクエンペラー(バグあり)",value=peバグあり,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()
    if 種類=="M":
        M=記録
        embed = discord.Embed(title="現在の鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="黒鬼",value=黒,inline=False)
        embed.add_field(name="レッドJ",value=J,inline=False)
        embed.add_field(name="マイティードッグ",value=M,inline=False)
        embed.add_field(name="どんどろ",value=丼,inline=False)
        embed.add_field(name="プリズンブレイカー",value=PB,inline=False)
        embed.add_field(name="Gババーン",value=婆,inline=False)
        embed.add_field(name="あやとりさま",value=綾,inline=False)
        embed.add_field(name="日ノ神",value=日野,inline=False)
        embed.add_field(name="極鬼玉集め",value=鬼玉,inline=False)
        embed.add_field(name="疾風怒濤(バグなし)",value=怒涛バグなし,inline=False)
        embed.add_field(name="疾風怒濤(バグあり)",value=怒涛バグあり,inline=False)
        embed.add_field(name="紅白ボス合戦",value=紅白,inline=False)
        embed.add_field(name="TOB",value=TOB,inline=False)
        embed.add_field(name="大妖魔ぬらねいら",value=ねいら,inline=False)
        embed.add_field(name="ピンクエンペラー(バグなし)",value=peバグなし,inline=False)
        embed.add_field(name="ピンクエンペラー(バグあり)",value=peバグあり,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()
    if 種類=="J":

        J=記録
        embed = discord.Embed(title="現在の鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="黒鬼",value=黒,inline=False)
        embed.add_field(name="レッドJ",value=J,inline=False)
        embed.add_field(name="マイティードッグ",value=M,inline=False)
        embed.add_field(name="どんどろ",value=丼,inline=False)
        embed.add_field(name="プリズンブレイカー",value=PB,inline=False)
        embed.add_field(name="Gババーン",value=婆,inline=False)
        embed.add_field(name="あやとりさま",value=綾,inline=False)
        embed.add_field(name="日ノ神",value=日野,inline=False)
        embed.add_field(name="極鬼玉集め",value=鬼玉,inline=False)
        embed.add_field(name="疾風怒濤(バグなし)",value=怒涛バグなし,inline=False)
        embed.add_field(name="疾風怒濤(バグあり)",value=怒涛バグあり,inline=False)
        embed.add_field(name="紅白ボス合戦",value=紅白,inline=False)
        embed.add_field(name="TOB",value=TOB,inline=False)
        embed.add_field(name="大妖魔ぬらねいら",value=ねいら,inline=False)
        embed.add_field(name="ピンクエンペラー(バグなし)",value=peバグなし,inline=False)
        embed.add_field(name="ピンクエンペラー(バグあり)",value=peバグあり,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()
    if 種類=="丼":

        丼=記録
        embed = discord.Embed(title="現在の鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="黒鬼",value=黒,inline=False)
        embed.add_field(name="レッドJ",value=J,inline=False)
        embed.add_field(name="マイティードッグ",value=M,inline=False)
        embed.add_field(name="どんどろ",value=丼,inline=False)
        embed.add_field(name="プリズンブレイカー",value=PB,inline=False)
        embed.add_field(name="Gババーン",value=婆,inline=False)
        embed.add_field(name="あやとりさま",value=綾,inline=False)
        embed.add_field(name="日ノ神",value=日野,inline=False)
        embed.add_field(name="極鬼玉集め",value=鬼玉,inline=False)
        embed.add_field(name="疾風怒濤(バグなし)",value=怒涛バグなし,inline=False)
        embed.add_field(name="疾風怒濤(バグあり)",value=怒涛バグあり,inline=False)
        embed.add_field(name="紅白ボス合戦",value=紅白,inline=False)
        embed.add_field(name="TOB",value=TOB,inline=False)
        embed.add_field(name="大妖魔ぬらねいら",value=ねいら,inline=False)
        embed.add_field(name="ピンクエンペラー(バグなし)",value=peバグなし,inline=False)
        embed.add_field(name="ピンクエンペラー(バグあり)",value=peバグあり,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()
    if 種類=="PB":

        PB=記録
        embed = discord.Embed(title="現在の鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="黒鬼",value=黒,inline=False)
        embed.add_field(name="レッドJ",value=J,inline=False)
        embed.add_field(name="マイティードッグ",value=M,inline=False)
        embed.add_field(name="どんどろ",value=丼,inline=False)
        embed.add_field(name="プリズンブレイカー",value=PB,inline=False)
        embed.add_field(name="Gババーン",value=婆,inline=False)
        embed.add_field(name="あやとりさま",value=綾,inline=False)
        embed.add_field(name="日ノ神",value=日野,inline=False)
        embed.add_field(name="極鬼玉集め",value=鬼玉,inline=False)
        embed.add_field(name="疾風怒濤(バグなし)",value=怒涛バグなし,inline=False)
        embed.add_field(name="疾風怒濤(バグあり)",value=怒涛バグあり,inline=False)
        embed.add_field(name="紅白ボス合戦",value=紅白,inline=False)
        embed.add_field(name="TOB",value=TOB,inline=False)
        embed.add_field(name="大妖魔ぬらねいら",value=ねいら,inline=False)
        embed.add_field(name="ピンクエンペラー(バグなし)",value=peバグなし,inline=False)
        embed.add_field(name="ピンクエンペラー(バグあり)",value=peバグあり,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()
    if 種類=="婆":

        婆=記録
        embed = discord.Embed(title="現在の鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="黒鬼",value=黒,inline=False)
        embed.add_field(name="レッドJ",value=J,inline=False)
        embed.add_field(name="マイティードッグ",value=M,inline=False)
        embed.add_field(name="どんどろ",value=丼,inline=False)
        embed.add_field(name="プリズンブレイカー",value=PB,inline=False)
        embed.add_field(name="Gババーン",value=婆,inline=False)
        embed.add_field(name="あやとりさま",value=綾,inline=False)
        embed.add_field(name="日ノ神",value=日野,inline=False)
        embed.add_field(name="極鬼玉集め",value=鬼玉,inline=False)
        embed.add_field(name="疾風怒濤(バグなし)",value=怒涛バグなし,inline=False)
        embed.add_field(name="疾風怒濤(バグあり)",value=怒涛バグあり,inline=False)
        embed.add_field(name="紅白ボス合戦",value=紅白,inline=False)
        embed.add_field(name="TOB",value=TOB,inline=False)
        embed.add_field(name="大妖魔ぬらねいら",value=ねいら,inline=False)
        embed.add_field(name="ピンクエンペラー(バグなし)",value=peバグなし,inline=False)
        embed.add_field(name="ピンクエンペラー(バグあり)",value=peバグあり,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()
    if 種類=="綾":

        綾=記録
        embed = discord.Embed(title="現在の鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="黒鬼",value=黒,inline=False)
        embed.add_field(name="レッドJ",value=J,inline=False)
        embed.add_field(name="マイティードッグ",value=M,inline=False)
        embed.add_field(name="どんどろ",value=丼,inline=False)
        embed.add_field(name="プリズンブレイカー",value=PB,inline=False)
        embed.add_field(name="Gババーン",value=婆,inline=False)
        embed.add_field(name="あやとりさま",value=綾,inline=False)
        embed.add_field(name="日ノ神",value=日野,inline=False)
        embed.add_field(name="極鬼玉集め",value=鬼玉,inline=False)
        embed.add_field(name="疾風怒濤(バグなし)",value=怒涛バグなし,inline=False)
        embed.add_field(name="疾風怒濤(バグあり)",value=怒涛バグあり,inline=False)
        embed.add_field(name="紅白ボス合戦",value=紅白,inline=False)
        embed.add_field(name="TOB",value=TOB,inline=False)
        embed.add_field(name="大妖魔ぬらねいら",value=ねいら,inline=False)
        embed.add_field(name="ピンクエンペラー(バグなし)",value=peバグなし,inline=False)
        embed.add_field(name="ピンクエンペラー(バグあり)",value=peバグあり,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()
    if 種類=="日野":

        日野=記録
        embed = discord.Embed(title="現在の鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="黒鬼",value=黒,inline=False)
        embed.add_field(name="レッドJ",value=J,inline=False)
        embed.add_field(name="マイティードッグ",value=M,inline=False)
        embed.add_field(name="どんどろ",value=丼,inline=False)
        embed.add_field(name="プリズンブレイカー",value=PB,inline=False)
        embed.add_field(name="Gババーン",value=婆,inline=False)
        embed.add_field(name="あやとりさま",value=綾,inline=False)
        embed.add_field(name="日ノ神",value=日野,inline=False)
        embed.add_field(name="極鬼玉集め",value=鬼玉,inline=False)
        embed.add_field(name="疾風怒濤(バグなし)",value=怒涛バグなし,inline=False)
        embed.add_field(name="疾風怒濤(バグあり)",value=怒涛バグあり,inline=False)
        embed.add_field(name="紅白ボス合戦",value=紅白,inline=False)
        embed.add_field(name="TOB",value=TOB,inline=False)
        embed.add_field(name="大妖魔ぬらねいら",value=ねいら,inline=False)
        embed.add_field(name="ピンクエンペラー(バグなし)",value=peバグなし,inline=False)
        embed.add_field(name="ピンクエンペラー(バグあり)",value=peバグあり,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()
    if 種類=="鬼玉":

        鬼玉=記録
        embed = discord.Embed(title="現在の鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="黒鬼",value=黒,inline=False)
        embed.add_field(name="レッドJ",value=J,inline=False)
        embed.add_field(name="マイティードッグ",value=M,inline=False)
        embed.add_field(name="どんどろ",value=丼,inline=False)
        embed.add_field(name="プリズンブレイカー",value=PB,inline=False)
        embed.add_field(name="Gババーン",value=婆,inline=False)
        embed.add_field(name="あやとりさま",value=綾,inline=False)
        embed.add_field(name="日ノ神",value=日野,inline=False)
        embed.add_field(name="極鬼玉集め",value=鬼玉,inline=False)
        embed.add_field(name="疾風怒濤(バグなし)",value=怒涛バグなし,inline=False)
        embed.add_field(name="疾風怒濤(バグあり)",value=怒涛バグあり,inline=False)
        embed.add_field(name="紅白ボス合戦",value=紅白,inline=False)
        embed.add_field(name="TOB",value=TOB,inline=False)
        embed.add_field(name="大妖魔ぬらねいら",value=ねいら,inline=False)
        embed.add_field(name="ピンクエンペラー(バグなし)",value=peバグなし,inline=False)
        embed.add_field(name="ピンクエンペラー(バグあり)",value=peバグあり,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()
    if 種類=="怒涛バグなし":

        怒涛バグなし=記録
        embed = discord.Embed(title="現在の鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="黒鬼",value=黒,inline=False)
        embed.add_field(name="レッドJ",value=J,inline=False)
        embed.add_field(name="マイティードッグ",value=M,inline=False)
        embed.add_field(name="どんどろ",value=丼,inline=False)
        embed.add_field(name="プリズンブレイカー",value=PB,inline=False)
        embed.add_field(name="Gババーン",value=婆,inline=False)
        embed.add_field(name="あやとりさま",value=綾,inline=False)
        embed.add_field(name="日ノ神",value=日野,inline=False)
        embed.add_field(name="極鬼玉集め",value=鬼玉,inline=False)
        embed.add_field(name="疾風怒濤(バグなし)",value=怒涛バグなし,inline=False)
        embed.add_field(name="疾風怒濤(バグあり)",value=怒涛バグあり,inline=False)
        embed.add_field(name="紅白ボス合戦",value=紅白,inline=False)
        embed.add_field(name="TOB",value=TOB,inline=False)
        embed.add_field(name="大妖魔ぬらねいら",value=ねいら,inline=False)
        embed.add_field(name="ピンクエンペラー(バグなし)",value=peバグなし,inline=False)
        embed.add_field(name="ピンクエンペラー(バグあり)",value=peバグあり,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()
    if 種類=="怒涛バグあり":

        怒涛バグあり=記録
        embed = discord.Embed(title="現在の鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="黒鬼",value=黒,inline=False)
        embed.add_field(name="レッドJ",value=J,inline=False)
        embed.add_field(name="マイティードッグ",value=M,inline=False)
        embed.add_field(name="どんどろ",value=丼,inline=False)
        embed.add_field(name="プリズンブレイカー",value=PB,inline=False)
        embed.add_field(name="Gババーン",value=婆,inline=False)
        embed.add_field(name="あやとりさま",value=綾,inline=False)
        embed.add_field(name="日ノ神",value=日野,inline=False)
        embed.add_field(name="極鬼玉集め",value=鬼玉,inline=False)
        embed.add_field(name="疾風怒濤(バグなし)",value=怒涛バグなし,inline=False)
        embed.add_field(name="疾風怒濤(バグあり)",value=怒涛バグあり,inline=False)
        embed.add_field(name="紅白ボス合戦",value=紅白,inline=False)
        embed.add_field(name="TOB",value=TOB,inline=False)
        embed.add_field(name="大妖魔ぬらねいら",value=ねいら,inline=False)
        embed.add_field(name="ピンクエンペラー(バグなし)",value=peバグなし,inline=False)
        embed.add_field(name="ピンクエンペラー(バグあり)",value=peバグあり,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()
    if 種類=="紅白":

        紅白=記録
        embed = discord.Embed(title="現在の鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="黒鬼",value=黒,inline=False)
        embed.add_field(name="レッドJ",value=J,inline=False)
        embed.add_field(name="マイティードッグ",value=M,inline=False)
        embed.add_field(name="どんどろ",value=丼,inline=False)
        embed.add_field(name="プリズンブレイカー",value=PB,inline=False)
        embed.add_field(name="Gババーン",value=婆,inline=False)
        embed.add_field(name="あやとりさま",value=綾,inline=False)
        embed.add_field(name="日ノ神",value=日野,inline=False)
        embed.add_field(name="極鬼玉集め",value=鬼玉,inline=False)
        embed.add_field(name="疾風怒濤(バグなし)",value=怒涛バグなし,inline=False)
        embed.add_field(name="疾風怒濤(バグあり)",value=怒涛バグあり,inline=False)
        embed.add_field(name="紅白ボス合戦",value=紅白,inline=False)
        embed.add_field(name="TOB",value=TOB,inline=False)
        embed.add_field(name="大妖魔ぬらねいら",value=ねいら,inline=False)
        embed.add_field(name="ピンクエンペラー(バグなし)",value=peバグなし,inline=False)
        embed.add_field(name="ピンクエンペラー(バグあり)",value=peバグあり,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()
    if 種類=="TOB":

        TOB=記録
        embed = discord.Embed(title="現在の鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="黒鬼",value=黒,inline=False)
        embed.add_field(name="レッドJ",value=J,inline=False)
        embed.add_field(name="マイティードッグ",value=M,inline=False)
        embed.add_field(name="どんどろ",value=丼,inline=False)
        embed.add_field(name="プリズンブレイカー",value=PB,inline=False)
        embed.add_field(name="Gババーン",value=婆,inline=False)
        embed.add_field(name="あやとりさま",value=綾,inline=False)
        embed.add_field(name="日ノ神",value=日野,inline=False)
        embed.add_field(name="極鬼玉集め",value=鬼玉,inline=False)
        embed.add_field(name="疾風怒濤(バグなし)",value=怒涛バグなし,inline=False)
        embed.add_field(name="疾風怒濤(バグあり)",value=怒涛バグあり,inline=False)
        embed.add_field(name="紅白ボス合戦",value=紅白,inline=False)
        embed.add_field(name="TOB",value=TOB,inline=False)
        embed.add_field(name="大妖魔ぬらねいら",value=ねいら,inline=False)
        embed.add_field(name="ピンクエンペラー(バグなし)",value=peバグなし,inline=False)
        embed.add_field(name="ピンクエンペラー(バグあり)",value=peバグあり,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()
    if 種類=="ねいら":

        ねいら=記録
        embed = discord.Embed(title="現在の鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="黒鬼",value=黒,inline=False)
        embed.add_field(name="レッドJ",value=J,inline=False)
        embed.add_field(name="マイティードッグ",value=M,inline=False)
        embed.add_field(name="どんどろ",value=丼,inline=False)
        embed.add_field(name="プリズンブレイカー",value=PB,inline=False)
        embed.add_field(name="Gババーン",value=婆,inline=False)
        embed.add_field(name="あやとりさま",value=綾,inline=False)
        embed.add_field(name="日ノ神",value=日野,inline=False)
        embed.add_field(name="極鬼玉集め",value=鬼玉,inline=False)
        embed.add_field(name="疾風怒濤(バグなし)",value=怒涛バグなし,inline=False)
        embed.add_field(name="疾風怒濤(バグあり)",value=怒涛バグあり,inline=False)
        embed.add_field(name="紅白ボス合戦",value=紅白,inline=False)
        embed.add_field(name="TOB",value=TOB,inline=False)
        embed.add_field(name="大妖魔ぬらねいら",value=ねいら,inline=False)
        embed.add_field(name="ピンクエンペラー(バグなし)",value=peバグなし,inline=False)
        embed.add_field(name="ピンクエンペラー(バグあり)",value=peバグあり,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()
    if 種類=="peバグなし":

        peバグなし=記録
        embed = discord.Embed(title="現在の鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="黒鬼",value=黒,inline=False)
        embed.add_field(name="レッドJ",value=J,inline=False)
        embed.add_field(name="マイティードッグ",value=M,inline=False)
        embed.add_field(name="どんどろ",value=丼,inline=False)
        embed.add_field(name="プリズンブレイカー",value=PB,inline=False)
        embed.add_field(name="Gババーン",value=婆,inline=False)
        embed.add_field(name="あやとりさま",value=綾,inline=False)
        embed.add_field(name="日ノ神",value=日野,inline=False)
        embed.add_field(name="極鬼玉集め",value=鬼玉,inline=False)
        embed.add_field(name="疾風怒濤(バグなし)",value=怒涛バグなし,inline=False)
        embed.add_field(name="疾風怒濤(バグあり)",value=怒涛バグあり,inline=False)
        embed.add_field(name="紅白ボス合戦",value=紅白,inline=False)
        embed.add_field(name="TOB",value=TOB,inline=False)
        embed.add_field(name="大妖魔ぬらねいら",value=ねいら,inline=False)
        embed.add_field(name="ピンクエンペラー(バグなし)",value=peバグなし,inline=False)
        embed.add_field(name="ピンクエンペラー(バグあり)",value=peバグあり,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()        
    
    if 種類=="peバグあり":

        peバグあり=記録
        embed = discord.Embed(title="現在の鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="黒鬼",value=黒,inline=False)
        embed.add_field(name="レッドJ",value=J,inline=False)
        embed.add_field(name="マイティードッグ",value=M,inline=False)
        embed.add_field(name="どんどろ",value=丼,inline=False)
        embed.add_field(name="プリズンブレイカー",value=PB,inline=False)
        embed.add_field(name="Gババーン",value=婆,inline=False)
        embed.add_field(name="あやとりさま",value=綾,inline=False)
        embed.add_field(name="日ノ神",value=日野,inline=False)
        embed.add_field(name="極鬼玉集め",value=鬼玉,inline=False)
        embed.add_field(name="疾風怒濤(バグなし)",value=怒涛バグなし,inline=False)
        embed.add_field(name="疾風怒濤(バグあり)",value=怒涛バグあり,inline=False)
        embed.add_field(name="紅白ボス合戦",value=紅白,inline=False)
        embed.add_field(name="TOB",value=TOB,inline=False)
        embed.add_field(name="大妖魔ぬらねいら",value=ねいら,inline=False)
        embed.add_field(name="ピンクエンペラー(バグなし)",value=peバグなし,inline=False)
        embed.add_field(name="ピンクエンペラー(バグあり)",value=peバグあり,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()

@client.tree.command(name="記録変更_ソロ",description="鯖内最速記録変更")
@app_commands.describe(種類="更新する記録の種類",記録="更新する記録")
@app_commands.choices(種類=[
    app_commands.Choice(name="おとも疾風(バグなし)", value="おとも疾風バグなし"),
    app_commands.Choice(name="おとも疾風(バグあり)", value="おとも疾風バグあり"),
    app_commands.Choice(name="おとも紅白", value="おとも紅白"),
    app_commands.Choice(name="おともTOB", value="おともTOB"),
    app_commands.Choice(name="おともねいら", value="おともねいら"),
    app_commands.Choice(name="おともピンク(バグなし)", value="おともピンクバグなし"),
    app_commands.Choice(name="おともピンク(バグあり)", value="おともピンクバグあり"),
    app_commands.Choice(name="おとも鬼玉", value="おとも鬼玉"),
    app_commands.Choice(name="おともなし疾風", value="疾風"),
    app_commands.Choice(name="おともなし紅白", value="紅白"),
    app_commands.Choice(name="おともなしTOB", value="TOB"),
    app_commands.Choice(name="おともなしねいら", value="ねいら"),
    app_commands.Choice(name="おともなしピンク", value="ピンク"),
])
async def changesoro(interaction:discord.Interaction,種類:str,記録:str):
    global ソロ疾風なし,ソロ疾風あり,ソロ紅白,ソロTOB,ソロねいら,ソロピンクなし,ソロピンクあり,ソロ鬼玉,sippuu,kouhaku,neira,tob,pinku
    if 種類=="おとも疾風バグなし":
        ソロ疾風なし=記録
        embed = discord.Embed(title="現在のソロ鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="[おともあり]",value="",inline=False)
        embed.add_field(name="疾風バグなし",value=ソロ疾風なし,inline=False)
        embed.add_field(name="疾風バグあり",value=ソロ疾風あり,inline=False)
        embed.add_field(name="紅白",value=ソロ紅白,inline=False)
        embed.add_field(name="TOB",value=ソロTOB,inline=False)
        embed.add_field(name="ぬらねいら",value=ソロねいら,inline=False)
        embed.add_field(name="ピンクバグなし",value=ソロピンクなし,inline=False)
        embed.add_field(name="ピンクバグあり",value=ソロピンクあり,inline=False)
        embed.add_field(name="鬼玉",value=ソロ鬼玉,inline=False)
        embed.add_field(name="[おともなし]",value="",inline=False)
        embed.add_field(name="疾風",value=sippuu,inline=False)
        embed.add_field(name="紅白",value=紅白,inline=False)
        embed.add_field(name="TOB",value=tob,inline=False)
        embed.add_field(name="ぬらねいら",value=neira,inline=False)
        embed.add_field(name="ピンクエンペラー",value=pinku,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()

    if 種類=="おとも疾風バグあり":
        ソロ疾風あり=記録
        embed = discord.Embed(title="現在のソロ鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="[おともあり]",value="",inline=False)
        embed.add_field(name="疾風バグなし",value=ソロ疾風なし,inline=False)
        embed.add_field(name="疾風バグあり",value=ソロ疾風あり,inline=False)
        embed.add_field(name="紅白",value=ソロ紅白,inline=False)
        embed.add_field(name="TOB",value=ソロTOB,inline=False)
        embed.add_field(name="ぬらねいら",value=ソロねいら,inline=False)
        embed.add_field(name="ピンクバグなし",value=ソロピンクなし,inline=False)
        embed.add_field(name="ピンクバグあり",value=ソロピンクあり,inline=False)
        embed.add_field(name="鬼玉",value=ソロ鬼玉,inline=False)
        embed.add_field(name="[おともなし]",value="",inline=False)
        embed.add_field(name="疾風",value=sippuu,inline=False)
        embed.add_field(name="紅白",value=紅白,inline=False)
        embed.add_field(name="TOB",value=tob,inline=False)
        embed.add_field(name="ぬらねいら",value=neira,inline=False)
        embed.add_field(name="ピンクエンペラー",value=pinku,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()

    if 種類=="おとも紅白":
        ソロ紅白=記録
        embed = discord.Embed(title="現在のソロ鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="[おともあり]",value="",inline=False)
        embed.add_field(name="疾風バグなし",value=ソロ疾風なし,inline=False)
        embed.add_field(name="疾風バグあり",value=ソロ疾風あり,inline=False)
        embed.add_field(name="紅白",value=ソロ紅白,inline=False)
        embed.add_field(name="TOB",value=ソロTOB,inline=False)
        embed.add_field(name="ぬらねいら",value=ソロねいら,inline=False)
        embed.add_field(name="ピンクバグなし",value=ソロピンクなし,inline=False)
        embed.add_field(name="ピンクバグあり",value=ソロピンクあり,inline=False)
        embed.add_field(name="鬼玉",value=ソロ鬼玉,inline=False)
        embed.add_field(name="[おともなし]",value="",inline=False)
        embed.add_field(name="疾風",value=sippuu,inline=False)
        embed.add_field(name="紅白",value=紅白,inline=False)
        embed.add_field(name="TOB",value=tob,inline=False)
        embed.add_field(name="ぬらねいら",value=neira,inline=False)
        embed.add_field(name="ピンクエンペラー",value=pinku,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()

    if 種類=="おともTOB":
        ソロTOB=記録
        embed = discord.Embed(title="現在のソロ鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="[おともあり]",value="",inline=False)
        embed.add_field(name="疾風バグなし",value=ソロ疾風なし,inline=False)
        embed.add_field(name="疾風バグあり",value=ソロ疾風あり,inline=False)
        embed.add_field(name="紅白",value=ソロ紅白,inline=False)
        embed.add_field(name="TOB",value=ソロTOB,inline=False)
        embed.add_field(name="ぬらねいら",value=ソロねいら,inline=False)
        embed.add_field(name="ピンクバグなし",value=ソロピンクなし,inline=False)
        embed.add_field(name="ピンクバグあり",value=ソロピンクあり,inline=False)
        embed.add_field(name="鬼玉",value=ソロ鬼玉,inline=False)
        embed.add_field(name="[おともなし]",value="",inline=False)
        embed.add_field(name="疾風",value=sippuu,inline=False)
        embed.add_field(name="紅白",value=紅白,inline=False)
        embed.add_field(name="TOB",value=tob,inline=False)
        embed.add_field(name="ぬらねいら",value=neira,inline=False)
        embed.add_field(name="ピンクエンペラー",value=pinku,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()

    if 種類=="おともねいら":
        ソロねいら=記録
        embed = discord.Embed(title="現在のソロ鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="[おともあり]",value="",inline=False)
        embed.add_field(name="疾風バグなし",value=ソロ疾風なし,inline=False)
        embed.add_field(name="疾風バグあり",value=ソロ疾風あり,inline=False)
        embed.add_field(name="紅白",value=ソロ紅白,inline=False)
        embed.add_field(name="TOB",value=ソロTOB,inline=False)
        embed.add_field(name="ぬらねいら",value=ソロねいら,inline=False)
        embed.add_field(name="ピンクバグなし",value=ソロピンクなし,inline=False)
        embed.add_field(name="ピンクバグあり",value=ソロピンクあり,inline=False)
        embed.add_field(name="鬼玉",value=ソロ鬼玉,inline=False)
        embed.add_field(name="[おともなし]",value="",inline=False)
        embed.add_field(name="疾風",value=sippuu,inline=False)
        embed.add_field(name="紅白",value=紅白,inline=False)
        embed.add_field(name="TOB",value=tob,inline=False)
        embed.add_field(name="ぬらねいら",value=neira,inline=False)
        embed.add_field(name="ピンクエンペラー",value=pinku,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()

    if 種類=="おともピンクバグなし":
        ソロピンクなし=記録
        embed = discord.Embed(title="現在のソロ鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="[おともあり]",value="",inline=False)
        embed.add_field(name="疾風バグなし",value=ソロ疾風なし,inline=False)
        embed.add_field(name="疾風バグあり",value=ソロ疾風あり,inline=False)
        embed.add_field(name="紅白",value=ソロ紅白,inline=False)
        embed.add_field(name="TOB",value=ソロTOB,inline=False)
        embed.add_field(name="ぬらねいら",value=ソロねいら,inline=False)
        embed.add_field(name="ピンクバグなし",value=ソロピンクなし,inline=False)
        embed.add_field(name="ピンクバグあり",value=ソロピンクあり,inline=False)
        embed.add_field(name="鬼玉",value=ソロ鬼玉,inline=False)
        embed.add_field(name="[おともなし]",value="",inline=False)
        embed.add_field(name="疾風",value=sippuu,inline=False)
        embed.add_field(name="紅白",value=紅白,inline=False)
        embed.add_field(name="TOB",value=tob,inline=False)
        embed.add_field(name="ぬらねいら",value=neira,inline=False)
        embed.add_field(name="ピンクエンペラー",value=pinku,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()

    if 種類=="おともピンクバグあり":
        ソロピンクあり=記録
        embed = discord.Embed(title="現在のソロ鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="[おともあり]",value="",inline=False)
        embed.add_field(name="疾風バグなし",value=ソロ疾風なし,inline=False)
        embed.add_field(name="疾風バグあり",value=ソロ疾風あり,inline=False)
        embed.add_field(name="紅白",value=ソロ紅白,inline=False)
        embed.add_field(name="TOB",value=ソロTOB,inline=False)
        embed.add_field(name="ぬらねいら",value=ソロねいら,inline=False)
        embed.add_field(name="ピンクバグなし",value=ソロピンクなし,inline=False)
        embed.add_field(name="ピンクバグあり",value=ソロピンクあり,inline=False)
        embed.add_field(name="鬼玉",value=ソロ鬼玉,inline=False)
        embed.add_field(name="[おともなし]",value="",inline=False)
        embed.add_field(name="疾風",value=sippuu,inline=False)
        embed.add_field(name="紅白",value=紅白,inline=False)
        embed.add_field(name="TOB",value=tob,inline=False)
        embed.add_field(name="ぬらねいら",value=neira,inline=False)
        embed.add_field(name="ピンクエンペラー",value=pinku,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()

    if 種類=="ソロ鬼玉":
        ソロ鬼玉=記録
        embed = discord.Embed(title="現在のソロ鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="[おともあり]",value="",inline=False)
        embed.add_field(name="疾風バグなし",value=ソロ疾風なし,inline=False)
        embed.add_field(name="疾風バグあり",value=ソロ疾風あり,inline=False)
        embed.add_field(name="紅白",value=ソロ紅白,inline=False)
        embed.add_field(name="TOB",value=ソロTOB,inline=False)
        embed.add_field(name="ぬらねいら",value=ソロねいら,inline=False)
        embed.add_field(name="ピンクバグなし",value=ソロピンクなし,inline=False)
        embed.add_field(name="ピンクバグあり",value=ソロピンクあり,inline=False)
        embed.add_field(name="鬼玉",value=ソロ鬼玉,inline=False)
        embed.add_field(name="[おともなし]",value="",inline=False)
        embed.add_field(name="疾風",value=sippuu,inline=False)
        embed.add_field(name="紅白",value=紅白,inline=False)
        embed.add_field(name="TOB",value=tob,inline=False)
        embed.add_field(name="ぬらねいら",value=neira,inline=False)
        embed.add_field(name="ピンクエンペラー",value=pinku,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()

    if 種類=="疾風":
        sippuu=記録
        embed = discord.Embed(title="現在のソロ鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="[おともあり]",value="",inline=False)
        embed.add_field(name="疾風バグなし",value=ソロ疾風なし,inline=False)
        embed.add_field(name="疾風バグあり",value=ソロ疾風あり,inline=False)
        embed.add_field(name="紅白",value=ソロ紅白,inline=False)
        embed.add_field(name="TOB",value=ソロTOB,inline=False)
        embed.add_field(name="ぬらねいら",value=ソロねいら,inline=False)
        embed.add_field(name="ピンクバグなし",value=ソロピンクなし,inline=False)
        embed.add_field(name="ピンクバグあり",value=ソロピンクあり,inline=False)
        embed.add_field(name="鬼玉",value=ソロ鬼玉,inline=False)
        embed.add_field(name="[おともなし]",value="",inline=False)
        embed.add_field(name="疾風",value=sippuu,inline=False)
        embed.add_field(name="紅白",value=紅白,inline=False)
        embed.add_field(name="TOB",value=tob,inline=False)
        embed.add_field(name="ぬらねいら",value=neira,inline=False)
        embed.add_field(name="ピンクエンペラー",value=pinku,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()

    if 種類=="紅白":
        kouhaku=記録
        embed = discord.Embed(title="現在のソロ鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="[おともあり]",value="",inline=False)
        embed.add_field(name="疾風バグなし",value=ソロ疾風なし,inline=False)
        embed.add_field(name="疾風バグあり",value=ソロ疾風あり,inline=False)
        embed.add_field(name="紅白",value=ソロ紅白,inline=False)
        embed.add_field(name="TOB",value=ソロTOB,inline=False)
        embed.add_field(name="ぬらねいら",value=ソロねいら,inline=False)
        embed.add_field(name="ピンクバグなし",value=ソロピンクなし,inline=False)
        embed.add_field(name="ピンクバグあり",value=ソロピンクあり,inline=False)
        embed.add_field(name="鬼玉",value=ソロ鬼玉,inline=False)
        embed.add_field(name="[おともなし]",value="",inline=False)
        embed.add_field(name="疾風",value=sippuu,inline=False)
        embed.add_field(name="紅白",value=紅白,inline=False)
        embed.add_field(name="TOB",value=tob,inline=False)
        embed.add_field(name="ぬらねいら",value=neira,inline=False)
        embed.add_field(name="ピンクエンペラー",value=pinku,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()

    if 種類=="TOB":
        tob=記録
        embed = discord.Embed(title="現在のソロ鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="[おともあり]",value="",inline=False)
        embed.add_field(name="疾風バグなし",value=ソロ疾風なし,inline=False)
        embed.add_field(name="疾風バグあり",value=ソロ疾風あり,inline=False)
        embed.add_field(name="紅白",value=ソロ紅白,inline=False)
        embed.add_field(name="TOB",value=ソロTOB,inline=False)
        embed.add_field(name="ぬらねいら",value=ソロねいら,inline=False)
        embed.add_field(name="ピンクバグなし",value=ソロピンクなし,inline=False)
        embed.add_field(name="ピンクバグあり",value=ソロピンクあり,inline=False)
        embed.add_field(name="鬼玉",value=ソロ鬼玉,inline=False)
        embed.add_field(name="[おともなし]",value="",inline=False)
        embed.add_field(name="疾風",value=sippuu,inline=False)
        embed.add_field(name="紅白",value=紅白,inline=False)
        embed.add_field(name="TOB",value=tob,inline=False)
        embed.add_field(name="ぬらねいら",value=neira,inline=False)
        embed.add_field(name="ピンクエンペラー",value=pinku,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()

    if 種類=="ねいら":
        neira=記録
        embed = discord.Embed(title="現在のソロ鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="[おともあり]",value="",inline=False)
        embed.add_field(name="疾風バグなし",value=ソロ疾風なし,inline=False)
        embed.add_field(name="疾風バグあり",value=ソロ疾風あり,inline=False)
        embed.add_field(name="紅白",value=ソロ紅白,inline=False)
        embed.add_field(name="TOB",value=ソロTOB,inline=False)
        embed.add_field(name="ぬらねいら",value=ソロねいら,inline=False)
        embed.add_field(name="ピンクバグなし",value=ソロピンクなし,inline=False)
        embed.add_field(name="ピンクバグあり",value=ソロピンクあり,inline=False)
        embed.add_field(name="鬼玉",value=ソロ鬼玉,inline=False)
        embed.add_field(name="[おともなし]",value="",inline=False)
        embed.add_field(name="疾風",value=sippuu,inline=False)
        embed.add_field(name="紅白",value=紅白,inline=False)
        embed.add_field(name="TOB",value=tob,inline=False)
        embed.add_field(name="ぬらねいら",value=neira,inline=False)
        embed.add_field(name="ピンクエンペラー",value=pinku,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()

    if 種類=="ピンク":
        pinku=記録
        embed = discord.Embed(title="現在のソロ鯖内最速記録",color=0xb5ff4d)
        embed.add_field(name="[おともあり]",value="",inline=False)
        embed.add_field(name="疾風バグなし",value=ソロ疾風なし,inline=False)
        embed.add_field(name="疾風バグあり",value=ソロ疾風あり,inline=False)
        embed.add_field(name="紅白",value=ソロ紅白,inline=False)
        embed.add_field(name="TOB",value=ソロTOB,inline=False)
        embed.add_field(name="ぬらねいら",value=ソロねいら,inline=False)
        embed.add_field(name="ピンクバグなし",value=ソロピンクなし,inline=False)
        embed.add_field(name="ピンクバグあり",value=ソロピンクあり,inline=False)
        embed.add_field(name="鬼玉",value=ソロ鬼玉,inline=False)
        embed.add_field(name="[おともなし]",value="",inline=False)
        embed.add_field(name="疾風",value=sippuu,inline=False)
        embed.add_field(name="紅白",value=紅白,inline=False)
        embed.add_field(name="TOB",value=tob,inline=False)
        embed.add_field(name="ぬらねいら",value=neira,inline=False)
        embed.add_field(name="ピンクエンペラー",value=pinku,inline=False)
        await interaction.response.send_message(embed=embed)
        messages = []
        async for message in interaction.channel.history(limit=2):
            messages.append(message)
        if len(messages) > 1:
            await messages[1].delete()

client.run("MTM1NzE2MDcxNjY3NDc5MzY1Mw.Gz47rQ.GjHIxCvb-_yiVqdL85o6Erydbxb_0XR-V_Z1bc")
