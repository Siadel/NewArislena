# 기성 모듈
from sys import exit
import discord
from discord.ext import commands
from discord import Option

# 사용자 정의 모듈
from AriManage import * # 여기서 이 모듈의 코드가 한 차례 실행됨

# 데이터 로딩
with open("./bases/token.json", "r") as tk:
    TOKEN = json.load(tk)["token"]
with open("./bases/helpmessages.json", "r", encoding="utf-8") as hl:
    ARIHELP = json.load(hl)

# 지역 데이터 클래스로 로딩
AriA: dict[str, AriArea] = dict()
for k, v in ari_area.items():
    AriA[k] = AriArea()
    AriA[k].port(**v)

# 봇 권한 설정
intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True
# 봇 객체 생성
Ari = commands.Bot(command_prefix='아리야, ', intents=intents, help_command=None)

# 디스코드 데이터 (테스트 서버)
roles = {
    "관리자" : 1027528936147648542,
    "오너" : 1027536463811842138
}

# 왼쪽부터 테스트 서버, 아리슬레나 길드 ID
GUILD_IDS = [414798376522219520, 645257232895705090]


# 편의성 전역변수
DOUMI = ["관리자", "도우미"]

# static 변수
ENTER = "\n"
FIELDS_IN_ONE_EMBED = 9 # 임베드 하나에 들어갈 필드 제한+1 (실제 제한은 -1한 값)

# 유저 함수
def colon_param_value(param:str) -> str:
    # 입력된 파라미터를 ":" 문자를 기준으로 파싱
    # ":" 문자 오른쪽에 있었던 문자열을 반환
    return param.split(":")[1].strip()


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

def fetch_member_roles(member:discord.Member) -> list[str]:
    # 멤버의 역할 이름들을 반환
    return [r.name for r in member.roles]

# 커스텀 예외 클래스
class AllowedOnlyAdmin(commands.errors.CommandError):
    def __init__(self, message="관리자만 가능한 명령이에요!", *args):
        super().__init__(message, *args)

# 작동부
@Ari.event
async def on_ready():
    Ari.activity = discord.Game("명령어는 `아리`로 시작합니다~")
    print(f"Login bot: {Ari.user}")
    print(f"Api verision: {discord.__version__}")

    print(len(list(Ari.walk_application_commands())))
    for c in Ari.walk_application_commands():
        print(c)

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
    embed = discord.Embed(color=0xe67e22)
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
@Ari.slash_command(name="ping", description="아리의 핑을 확인합니다.", guild_ids=GUILD_IDS)
async def ping(ctx):
    await ctx.respond(f"핑: {round(Ari.latency*1000)}ms", ephemeral=True)

@Ari.slash_command(name="안녕", **ARIHELP["안녕"], guild_ids=GUILD_IDS) # 슬래시 커맨드 시험용 명령어
async def slashhello(ctx:discord.ApplicationContext,
                name:Option(str, "이름", required=False, default="익명")):
    author = ctx.author
    await ctx.respond(f"안녕하세요, {author.name}님! 당신의 이름은 {name}이군요!")
    await ctx.respond(f"2번 respond()할 수 있나 보네요.\n그리고 이 메세지는 당신에게만 보일 거에요.", ephemeral=True)

@Ari.command(name="안녕", **ARIHELP["안녕"]) # 명령어 시험용 명령어
async def hello(ctx:commands.Context, *args):
    author = ctx.message.author
    # 다른 사람에게는 보이지 않고 명령한 사람에게만 보이는 ephemeral 메세지를 출력
    # 그거 출력하려면 webhook을 만들어야 한다나 뭐라나
    # 잘 모르겠어요
    await ctx.send(f"{author.mention}\n안녕하세요, {author.name}님! 입력하신 내용은 {args}입니다!")

# 관리자 명령어 : 직접적으로 게임 데이터에 영향을 주면서, 오/남용 소지가 있는 명령어들
@Ari.slash_command(name="지역생성", **ARIHELP)
@commands.has_role("관리자")
async def generate_area(ctx:discord.ApplicationContext, *args):
    area = AriArea()
    area.generate()
    for arg in args:
        if "이름" in arg:
            area.name = colon_param_value(arg)
        elif "폐음절" in arg and colon_param_value(arg) == "아님":
            area.coda = False

    area.commit()
    AriA.setdefault(area.ID, area)
    AriS.save("area", "system")
    emb = discord.Embed()
    emb.add_field(name="생성된 지역", value=str(area.info()))
    await ctx.respond("지역 생성이 완료되었어요!", embed=emb)

# TODO: 나라 생성, 지역 삭제, 나라 삭제, 지역 생성(+int argument: 해당 숫자 만큼의 무명 지역을 생성), 야만인 생성,

@Ari.command(name="지역삭제", **ARIHELP["지역삭제"])
@commands.has_role("관리자")
async def remove_area(ctx:commands.Context, area_id:str):
    # 받은 area_id를 가진 지역을 삭제함
    # AriA에서도 삭제
    # AriS.remove_content()도 실행
    area_name = AriA[area_id].nominative()

    del AriA[area_id]
    AriS.remove_content(area_id, "area")
    await ctx.send(f"지역 {area_name} 삭제됐어요!")

@Ari.command(name="나라삭제", **ARIHELP["나라삭제"])
@commands.has_role("관리자")
async def remove_nation(ctx:commands.Context, nation_id):
    # 구현 안 됨
    pass


# 도우미 명령어 : 관리자 명령어 중 행정처리에 특화된 명령어들

@Ari.command(name="역할부여", **ARIHELP["역할부여"]) # 관리자 혹은 관리자가 아닌 이에게, 관리자가 아닌 역할 부여
@commands.has_any_role(*DOUMI)
async def attach_role(ctx:commands.Context, member_name_disc:str, role_name:str):
    rls = fetch_member_roles(ctx.author)
    if not "관리자" in rls and role_name in DOUMI:
        raise AllowedOnlyAdmin()
    member = fetch_member(member_name_disc, ctx.guild)
    await member.add_roles(fetch_role(role_name, ctx.guild))
    await ctx.send(f"{member_name_disc}에게 {role_name} 역할을 부여했어요!")

@Ari.command(name="역할해제", **ARIHELP["역할해제"]) # 역할해제
@commands.has_any_role(*DOUMI)
async def detach_role(ctx:commands.Context, member_name_disc:str, role_name:str):
    rls = fetch_member_roles(ctx.author)
    if not "관리자" in rls and role_name in DOUMI:
        raise AllowedOnlyAdmin()
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

@Ari.command(name="지역리스트", **ARIHELP["지역리스트"])
@commands.has_role("오너")
async def list_area(ctx:commands.Context):

    areas_length = len(AriA)
    embed, embedn = initialize_embed(areas_length)
    for fieldn, (k, v) in enumerate_fields(AriA.items()):
        value = ""
        value += f"지역 ID: {k}\n"
        embed.add_field(name=f"{v.name}", value=value, inline=True)
        if fieldn == FIELDS_IN_ONE_EMBED:
            await ctx.send(embed=embed)
            embed, embedn = initialize_embed(areas_length, embedn)

    await ctx.send(embed=embed)
    end_embed = discord.Embed()
    end_embed.title = f"지역 총 개수: {len(AriA)}개"
    await ctx.send(embed=end_embed)

# 전체 명령어
@Ari.command(name="도와줘", **ARIHELP["도와줘"])
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
    if not command_names:
        await ctx.send("더 자세한 명령어 설명은 `!도움 <명령어>`로 확인해주세요!")


@Ari.slash_command(name="도움", description="빗금 명령어에 정보를 출력합니다.", guild_ids=GUILD_IDS)
async def slashhelp(ctx:discord.ApplicationContext,
                    command_name = Option(str, "명령어", required=False)):
    d = dict()
    for command in Ari.application_commands:
        d.setdefault(command.name, [command.description])
    
    await ctx.respond(d)

# 건들지 마세요~
Ari.run(TOKEN)