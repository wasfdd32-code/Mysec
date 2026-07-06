import discord
from discord import app_commands
from discord.ext import commands
import os  # تم حل مشكلة الكرش بإضافة هذا السطر

# إعدادات البوت
intents = discord.Intents.default()
intents.members = True 
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # مزامنة الأوامر مع ديسكورد لتظهر كـ Slash Commands
    await bot.tree.sync()
    print(f'✅ البوت يعمل الآن كـ {bot.user}')

# --- أوامر الموديريشن المودرن ---

@bot.tree.command(name="ban", description="حظر عضو نهائياً من السيرفر")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "لا يوجد سبب"):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"🚫 تم حظر {member.mention} بنجاح!")

@bot.tree.command(name="kick", description="طرد عضو من السيرفر")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "لا يوجد سبب"):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"👢 تم طرد {member.mention} بنجاح!")

@bot.tree.command(name="timeout", description="إسكات عضو لفترة محددة")
@app_commands.checks.has_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "لا يوجد سبب"):
    from datetime import timedelta
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await interaction.response.send_message(f"🤐 تم إسكات {member.mention} لمدة {minutes} دقيقة!")

@bot.tree.command(name="mute", description="منع العضو من الكتابة (Timeout لمدة 24 ساعة)")
@app_commands.checks.has_permissions(moderate_members=True)
async def mute(interaction: discord.Interaction, member: discord.Member):
    from datetime import timedelta
    await member.timeout(timedelta(hours=24), reason="Muted by Admin")
    await interaction.response.send_message(f"🔇 تم ميوت {member.mention}!")

# تشغيل البوت باستخدام متغير البيئة TOKEN
token = os.environ.get('TOKEN')
if not token:
    print("❌ خطأ: لم يتم العثور على TOKEN في المتغيرات!")
else:
    bot.run(token)
