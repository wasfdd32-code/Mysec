import discord
from discord.ext import commands
from datetime import timedelta
import os

# إعدادات الـ Intents الضرورية جداً لعمل البوتات
intents = discord.Intents.default()
intents.members = True 
intents.message_content = True

# تعريف البوت بالبريفيكس !
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} متصل وجاهز للعمل!')

# --- أوامر الإدارة (Moderation Commands) ---

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="لا يوجد سبب"):
    await member.ban(reason=reason)
    await ctx.send(f"🚫 تم حظر {member.mention} بنجاح. السبب: {reason}")

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="لا يوجد سبب"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 تم طرد {member.mention} بنجاح. السبب: {reason}")

@bot.command(name="timeout")
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int, *, reason="لا يوجد سبب"):
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(f"🤐 تم إسكات {member.mention} لمدة {minutes} دقيقة. السبب: {reason}")

@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, *, reason="لا يوجد سبب"):
    # الميوت في ديسكورد الحديث هو عبارة عن Timeout طويل
    await member.timeout(timedelta(days=7), reason=reason)
    await ctx.send(f"🔇 تم ميوت {member.mention}!")

@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"✅ تم إلغاء الحظر عن {user.name}")

# تشغيل البوت
token = os.environ.get('TOKEN')
bot.run(token)
