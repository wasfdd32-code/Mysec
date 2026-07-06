import discord
from discord.ext import commands
from datetime import timedelta
import os

# إعدادات الـ Intents الضرورية لعمل الأوامر والترحيب
intents = discord.Intents.default()
intents.members = True 
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# ضع ID القناة هنا
WELCOME_CHANNEL_ID = 1523325683890389082  # استبدله بـ ID قناة الترحيب

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="!help")
    await bot.change_presence(status=discord.Status.dnd, activity=activity)
    print(f'✅ البوت {bot.user} متصل وجاهز للعمل!')

# --- نظام الترحيب الجديد ---
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        # حساب ترتيب العضو
        member_count = len(member.guild.members)
        
        # تصميم الـ Embed
        embed = discord.Embed(
            title=f"مرحباً بك في السيرفر {member.name}!",
            description=f"يا أهلاً بك في **{member.guild.name}**!\n\nأنت العضو رقم **{member_count}**.",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="📍 ملاحظة", value="الرجاء قراءة القوانين لتجنب العقوبات.", inline=False)
        embed.set_footer(text=f"ID: {member.id}")
        
        await channel.send(content=f"أهلاً بك {member.mention}", embed=embed)

# --- بقية الأوامر (كما هي في كودك) ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ عذراً، لا تملك الصلاحية الكافية لهذا الأمر!")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("❌ لم أستطع العثور على هذا العضو!")
    else:
        print(f"خطأ: {error}")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="📜 قائمة أوامر البوت", color=discord.Color.red())
    embed.add_field(name="🛡️ الإدارة", value="`!ban`, `!kick`, `!timeout`, `!mute`, `!unmute`", inline=False)
    embed.add_field(name="ℹ️ معلومات", value="`!userinfo`, `!serverinfo`", inline=False)
    await ctx.send(embed=embed)

# (أضف أوامر الـ ban و kick و timeout و mute هنا كما كانت في كودك)

bot.run(os.environ.get('TOKEN'))
