import discord
from discord.ext import commands
from datetime import timedelta
import os

# إعدادات الـ Intents الضرورية لعمل الأوامر
intents = discord.Intents.default()
intents.members = True 
intents.message_content = True

# تعريف البوت
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    # هنا كود حالة Do Not Disturb
    activity = discord.Activity(type=discord.ActivityType.listening, name="!help")
    await bot.change_presence(status=discord.Status.dnd, activity=activity)
    print(f'✅ البوت {bot.user} متصل بوضعية DND وجاهز للعمل!')

# نظام حماية لمنع الكرش عند حدوث خطأ
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ عذراً، لا تملك الصلاحية الكافية لهذا الأمر!")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("❌ لم أستطع العثور على هذا العضو!")
    else:
        print(f"خطأ: {error}")

# أمر المساعدة (Help)
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="📜 قائمة أوامر البوت", color=discord.Color.red())
    embed.add_field(name="🛡️ الإدارة", value="`!ban`, `!kick`, `!timeout`, `!mute`, `!unmute`", inline=False)
    embed.add_field(name="ℹ️ معلومات", value="`!userinfo`, `!serverinfo`", inline=False)
    await ctx.send(embed=embed)

# أوامر الإدارة الأساسية
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="لا يوجد سبب"):
    await member.ban(reason=reason)
    await ctx.send(f"🚫 تم حظر {member.mention}")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="لا يوجد سبب"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 تم طرد {member.mention}")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int, *, reason="لا يوجد سبب"):
    await member.timeout(timedelta(minutes=minutes), reason=reason)
    await ctx.send(f"🤐 تم إسكات {member.mention} لمدة {minutes} دقيقة.")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member):
    await member.timeout(timedelta(days=7), reason="Muted")
    await ctx.send(f"🔇 تم ميوت {member.mention}")

# تشغيل البوت
bot.run(os.environ.get('TOKEN'))
