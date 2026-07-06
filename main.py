import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta

intents = discord.Intents.default()
intents.members = True # مهم جداً لصلاحيات الـ Ban و Kick و Timeout
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync() # تفعيل الأوامر
    print(f'✅ البوت يعمل: {bot.user}')

# أمر الـ Ban
@bot.tree.command(name="ban", description="طرد عضو نهائياً من السيرفر")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "لا يوجد سبب"):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"🚫 تم حظر {member.mention} بنجاح!")

# أمر الـ Kick
@bot.tree.command(name="kick", description="طرد عضو من السيرفر")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "لا يوجد سبب"):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"👢 تم طرد {member.mention} بنجاح!")

# أمر الـ Timeout (زمن محدد)
@bot.tree.command(name="timeout", description="إسكات عضو لفترة محددة")
@app_commands.checks.has_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "لا يوجد سبب"):
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await interaction.response.send_message(f"🤐 تم إسكات {member.mention} لمدة {minutes} دقيقة!")

# أمر الـ Mute (إلغاء الكتابة)
# ملاحظة: أفضل طريقة حديثة للـ Mute هي إعطاء رتبة لا تملك صلاحية الكتابة أو استخدام الـ Timeout
@bot.tree.command(name="mute", description="منع العضو من الكتابة")
@app_commands.checks.has_permissions(moderate_members=True)
async def mute(interaction: discord.Interaction, member: discord.Member):
    # استخدام الـ Timeout كطريقة حديثة للـ Mute
    await member.timeout(timedelta(hours=24), reason="Muted by Admin")
    await interaction.response.send_message(f"🔇 تم ميوت {member.mention}!")

bot.run(os.environ['TOKEN'])