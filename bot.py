import discord, dotenv, os
from datetime import datetime, timezone, timedelta
from discord import app_commands, ui
from discord.ext import commands
from callback.maple import get_character as maple_character
from callback.tfd import eta0_a, eta0_b
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
async def rolldice(interaction:discord.Interaction):    # 출력
    my_dice = roll_dice()
    await interaction.response.send_message(embed=discord.Embed(description=f"데굴데굴...🎲\n주사위 {my_dice.get('dice')}을(를) 얻었다!", color=my_dice.get('color')))

@bot.tree.command(name='메이플', description='캐릭터 기본 정보 조회')
@app_commands.describe(캐릭터명='검색할 캐릭터명을 입력해주세요')
async def maple_openapi(interaction:discord.Interaction, 캐릭터명:str):
    character_info = maple_character(캐릭터명)

    if character_info:
        embed = discord.Embed(title=character_info['character_name'], color=0x6098e1)
        embed.add_field(name="월드", value=character_info['world_name'], inline=True)
        embed.add_field(name="레벨", value=f"{character_info['character_level']} ({character_info['character_exp_rate'][:5]}%)", inline=True)
        embed.add_field(name="직업", value=character_info['character_class'], inline=True)
        embed.add_field(name="길드", value=character_info['character_guild_name'], inline=False)
        embed.add_field(name="캐릭터 생성일", value=character_info['character_date_create'][:10], inline=False)
        
        # API 제공처에서 2025년 8월부터 width/height 300 고정으로 사양 변경됨에 따라, 섬네일 가독성이 저하되어 임시 주석 처리
        # embed.set_thumbnail(url=f"{character_info['character_image']}")
        
        # 이용 약관 준수를 위한 데이터 출처 표시
        embed.set_footer(text=f"Powered by Nexon Open API")
        
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(content=f"캐릭터가 존재하지 않습니다.", ephemeral=True)

@bot.tree.command(name='행보관', description='이번 주 알비온 황금마차')
async def tfd_eta0(interaction):
    now = datetime.now(timezone.utc) - timedelta(hours=8) #황금마차는 PST 기준 매주 금~월요일간 운영하므로 UTC-8을 계산
    
    if now.weekday() >= 0 and now.weekday() <= 3: #현재 요일이 화~목인 경우
        await interaction.response.send_message(content="황금마차 운영 기간이 아닙니다 (매 주 금요일 16:00 ~ 매 주 화요일 16:00)")
    else:
        btn1 = discord.ui.Button(label="교환 목록", style=discord.ButtonStyle.primary)
        btn2 = discord.ui.Button(label="공식 사이트에서 확인하기", style=discord.ButtonStyle.gray, url='https://tfd.nexon.com/ko/library/eta-0')
        view = discord.ui.View()
        view.add_item(btn1)
        view.add_item(btn2)

        async def embed_eta0(interaction:discord.Interaction):
            await interaction.response.defer()
            trade_a = await eta0_a()
            trade_b = await eta0_b()

            embed = discord.Embed(title="이번주 ETA-0 교환 목록", color=0x6098e1)

            if trade_a:   
                embed.add_field(name="침투작전 보상", value='\n'.join(trade_a), inline=True)
            if trade_b:
                embed.add_field(name="물자 교환", value='\n'.join(trade_b), inline=True)

            if embed.fields:
                await interaction.followup.send(embed=embed)
                  
        btn1.callback = embed_eta0
        await interaction.response.send_message(view=view)

@bot.tree.command(name='파판날씨', description='파판 각 지역별 날씨')
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