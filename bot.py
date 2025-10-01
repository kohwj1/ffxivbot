import discord, dotenv, os
from discord.ext import commands
from callback.ff14 import get_weather, get_et
from callback.etc import roll_dice
from data.helptext import help_text

dotenv.load_dotenv()

discord_token = os.getenv('discord_token')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    # status=discord.Status.online 추가하면 온라인 상태로 만들 수 있음
    await bot.change_presence(activity=discord.Game("월급 루팡"), status=discord.Status.online)
    await bot.tree.sync()
    print(bot.user.name + " 출근 완료")

@bot.tree.command(name='도움', description='명령어 까먹은 거 다 안다')
async def help_bin(interaction: discord.Interaction):
    user = await bot.fetch_user(interaction.user.id)
    await user.send(help_text)
    await interaction.response.send_message(f"{interaction.user.mention}님, 도움말을 DM으로 보내드렸습니다!", ephemeral=True)

@bot.tree.command(name='주사위', description='룰정굴')
async def rolldice(interaction:discord.Interaction):
    my_dice = roll_dice()
    await interaction.response.send_message(embed=discord.Embed(description=f"데굴데굴...🎲\n주사위 {my_dice.get('dice')}을(를) 얻었다!", color=my_dice.get('color')))

@bot.tree.command(name='날씨', description='파판 각 지역별 날씨')
async def ff14_weather(interaction):   
    btn_list = ["라노시아", "검은장막 숲", "다날란", "창천", "홍련", "칠흑", "효월", "황금", "하우징/기타"]
    view = discord.ui.View()

    async def embed_weather(interaction:discord.Interaction, fieldname):
        weather_list = get_weather(fieldname)

        embed = discord.Embed(title=f"{fieldname} 지역 날씨", color=0x6098e1)
        embed.add_field(name="에오르제아 시간", value=f"ET {get_et()}", inline=False)
        embed.add_field(name="맵", value='\n'.join(weather_list[0]), inline=True)
        embed.add_field(name="", value="", inline=True)
        embed.add_field(name="날씨 예보", value='\n'.join(weather_list[1]), inline=True)
        await interaction.response.send_message(embed=embed)

    for fieldname in btn_list:
        btn = discord.ui.Button(label=fieldname, style=discord.ButtonStyle.blurple)
        btn.callback = lambda interaction, fieldname=fieldname: embed_weather(interaction, fieldname)
        view.add_item(btn)
    
    await interaction.response.send_message(view=view)

if __name__ == '__main__':
    bot.run(discord_token)