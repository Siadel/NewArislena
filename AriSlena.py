# 기성 모듈
from sys import exit
import logging
import discord
from discord.ext import commands

# 사용자 정의 모듈
from AriCont import * # 여기서 이 모듈의 코드가 한 차례 실행됨

# 데이터 로딩
with open("./bases/token.json", "r") as tk:
    TOKEN = json.load(tk)["token"]
with open("./bases/helpmessages.json", "r", encoding="utf-8") as hl:
    ARIHELP = json.load(hl)

# 지역 데이터 클래스로 로딩
AriArea_data = dict()
for k, v in ari_area.items():
    AriArea_data[k] = AriArea()
    AriArea_data[k].port(**v)

# discord.log라는 파일에 시스템 로그 출력 (재시작하면 내용이 지워지고 처음부터 다시 작성됨)
handler = logging.FileHandler(filename='discord.log', encoding="utf-8", mode="w")

# 봇 권한 설정
intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True
# 봇 객체 생성
Ari = commands.Bot(command_prefix='!', intents=intents, help_command=None)
AriCl = discord.Client(intents=intents)

# 디스코드 데이터
roles = {
    "관리자" : 1027528936147648542,
    "오너" : 1027536463811842138
}

# 편의성 전역변수
DOUMI = ["관리자", "도우미"]

# static 변수
ENTER = "\n"
FIELDS_IN_ONE_EMBED = 9 # 임베드 하나에 들어갈 필드 제한+1 (실제 제한은 -1한 값)

# 유저 함수
def calc_embed(data_length): 
    # 몇 번째 임베드에 들어갈 데이터인지, 혹은 임베드 몇 개가 있어야 할지 계산
    return int((data_length-1) / FIELDS_IN_ONE_EMBED) + 1

def enumerate_fields(iterable) -> list[tuple[int, Any]]:
    res = []
    for i, it in enumerate(iterable):
        i += 1
        res.append((i - (FIELDS_IN_ONE_EMBED * (calc_embed(i) - 1)), it))
    return res

def initialize_embed(fields:int, embedn=1) -> tuple[discord.Embed, int]:
    # fields의 개수에 따라 임베드 몇 개가 있어야 할 지 계산 + 임베드 번호 붙이기
    embed = discord.Embed()
    embed.title = f"목록 : {embedn} 중 {calc_embed(fields)}"
    return embed, embedn+1

def fetch_member(member_name_disc:str, guild:discord.Guild) -> discord.Member:
    # 이름과 식별자를 모두 쳐야 검색 가능함
    (name, disc) = member_name_disc.split("#")
    for m in guild.members:
        if name == m.name and disc == m.discriminator:
            return m

def fetch_role(role_name:str, guild:discord.Guild) -> discord.Role:
    # 역할 이름을 쳐야 검색 가능함
    for r in guild.roles:
        if role_name == r.name:
            return r

def fetch_category(category_name:str, guild:discord.Guild) -> discord.CategoryChannel:
    # 카테고리 이름을 쳐야 검색 가능함
    for category in guild.categories:
        if category_name == category.name:
            return category

def fetch_text_channel(channel_name:str, guild:discord.Guild) -> discord.TextChannel:
    # 채널명을 쳐야 검색 가능함
    for tch in guild.text_channels:
        if channel_name == tch.name:
            return tch

@Ari.event
async def on_ready():
    Ari.activity = discord.Game("아리슬레나 운영")
    print(f"Login bot: {Ari.user}")
    print(f"Discord.py verision: {discord.__version__}")

@Ari.event
async def on_command_error(ctx:commands.Context, exception):
    # 오류문구 번역 (이외의 것들은 기본 오류 문구로 대체)
    # exception은 오류 객체 혹은 오류 메세지
    if isinstance(exception, commands.errors.MissingRole):
        exception = f"{exception.missing_role} 역할이어야 해요!"

    elif isinstance(exception, commands.errors.CommandNotFound):
        # Command "{command name}" is not found
        exception = f"{str(exception).split(' ')[1]} 명령어가 없어요..." 

    elif isinstance(exception, commands.errors.MissingRequiredArgument):
        # {argument name} is a required argument that is missing.
        #exception = f"{exception.param}"
        exception = f"{exception.param} 인자가 비어 있어요!"
    embed = discord.Embed(color=255)
    embed.add_field(name="짜잔~ 오류가 발생했어요!", 
                    value=f"{'' if type(exception) is str else str(type(exception))+ENTER}{exception}")
    await ctx.send(embed=embed)

@Ari.listen('on_member_join') # tq 이거 왜 작동 안 함  
async def on_member_join(member:discord.Member):
    m=f"{member.mention}\n{member.name}님! 아리슬레나+(베타)에 오신 것을 환영합니다~"
    for c in discord.Guild.text_channels:
        if c.name=="general":
            await c.send(m)
            break


# 명령어 --------------------------------------------------------------------------------------------


@Ari.command(name="안녕", **ARIHELP["안녕"]) # 명령어 시험용 명령어
async def hello(ctx:commands.Context, *args):
    author = ctx.message.author
    await ctx.send(f"{author.mention}\n안녕하세요, {author.name}님! 입력하신 내용은 {args}입니다!")

# 관리자 명령어 : 직접적으로 게임 데이터에 영향을 주면서, 오/남용 소지가 있는 명령어들
@Ari.command(name="지역생성", **ARIHELP["지역생성"]) # 지역생성 명령어 (관리자)
@commands.has_role("관리자")
async def generate_area(ctx:commands.Context, name:str):
    area = AriArea.generate(name)
    emb = discord.Embed()
    emb.add_field(name="생성된 지역", value=str(area.info()))
    await ctx.send("지역 생성이 완료되었어요!", embed=emb)

# TODO: 나라 생성, 지역 삭제, 나라 삭제, 지역 생성(+int argument: 해당 숫자 만큼의 무명 지역을 생성), 야만인 생성,

@Ari.command(name="지역삭제", **ARIHELP["지역삭제"])
@commands.has_role("관리자")
async def remove_area(ctx:commands.Context, area_id):
    # 구현 안 됨
    pass

@Ari.command(name="나라삭제", **ARIHELP["나라삭제"])
@commands.has_role("관리자")
async def remove_nation(ctx:commands.Context, nation_id):
    # 구현 안 됨
    pass


# 도우미 명령어 : 관리자 명령어 중 행정처리에 특화된 명령어들

@Ari.command(name="역할부여", **ARIHELP["역할부여"]) # 관리자 혹은 관리자가 아닌 이에게, 관리자가 아닌 역할 부여
@commands.has_any_role(*DOUMI)
async def attach_role(ctx:commands.Context, member_name_disc:str, role_name:str):
    member = fetch_member(member_name_disc, ctx.guild)
    await member.add_roles(fetch_role(role_name, ctx.guild))
    await ctx.send(f"{member_name_disc}에게 {role_name} 역할을 부여했어요!")

@Ari.command(name="역할해제", **ARIHELP["역할해제"]) # 역할해제
@commands.has_any_role(*DOUMI)
async def detach_role(ctx:commands.Context, member_name_disc:str, role_name:str):
    member = fetch_member(member_name_disc, ctx.guild)
    await member.remove_roles(fetch_role(role_name, ctx.guild))
    await ctx.send(f"{member_name_disc}에게서 {role_name} 역할을 해제했어요!")

@Ari.command(name="채널생성", **ARIHELP["채널생성"])
@commands.has_any_role(*DOUMI)
async def create_channel(ctx:commands.Context, channel_name:str, category_name:str):
    await ctx.guild.create_text_channel(channel_name,
                                        category=fetch_category(category_name, ctx.guild))

@Ari.command(name="정지!", **ARIHELP["정지!"])
@commands.has_any_role(*DOUMI)
async def emergency_phase(ctx:commands.Context):
    Ari.status = discord.Status.dnd
    await ctx.send("아리가 정지돼요...!!")
    exit(0)

# TODO: 채널생성 

# 오너 명령어
@Ari.command(name="건국", **ARIHELP["건국"])
@commands.has_role("오너")
async def add_nation(ctx:commands.Context, nation_name:str):
    # 구현 안 됨
    pass


# 전체 명령어
@Ari.command(name="도움", **ARIHELP["도움"])
async def help(ctx:commands.Context, *command_names):
    
    cmds = list(Ari.commands)
    len_commands = len(cmds)
    if command_names:  # 인자가 있을 때
        len_commands = len(command_names)
        picked_cmds:list[commands.Command] = []
        for c in cmds:
            if c.name in command_names:
                picked_cmds.append(c)
        cmds = picked_cmds

    embed, embedn = initialize_embed(len_commands)
    for fieldn, command in enumerate_fields(cmds):
        if command_names:  # 인자가 있을 때
            value = f">>> **{command.description}** 사용 가능\n\n{command.usage}\n\n{command.help}"
            inline = False
        else:
            value = f">>> **{command.description}** 사용 가능\n\n{command.brief}"
            inline = True
        embed.add_field(name=command.name, value=value, inline=inline)
        if fieldn == FIELDS_IN_ONE_EMBED:  # 임베드 필드 수 제한 구현
            await ctx.send(embed=embed)
            embed, embedn = initialize_embed(len_commands, embedn)

    await ctx.send(embed=embed) # 남는 필드가 들어 있는 엠베드 출력

# 건들지 마세요~
Ari.run(TOKEN, log_handler=handler)