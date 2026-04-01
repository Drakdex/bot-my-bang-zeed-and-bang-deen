import discord
from discord import app_commands
from discord.ext import commands
import requests
from datetime import datetime, timezone
now = datetime.now().strftime("%d/%m/%Y %H:%M")

# ======================
# ⚙️ CONFIG
# ======================
TOKEN = "MTQyOTYwNjQ1ODUwODQ0Mzc0OA.GMJ01j.zQ4ScaMZ275kV2xZzRfEyZ9rBKBv185hh58zrE"
WEBHOOK_verify = "https://discord.com/api/webhooks/1488961555063111730/Sg-8YSSc9w-NbdBOPgIrxWUpiw9pcyP96wCW0vg3--vgkP5IbX75HBn--r_jVQ0s4gL_"
WEBHOOK_ANNOUNCE = "https://discord.com/api/webhooks/1488961555063111730/Sg-8YSSc9w-NbdBOPgIrxWUpiw9pcyP96wCW0vg3--vgkP5IbX75HBn--r_jVQ0s4gL_"
VERIFIED_ROLE_ID = 1415336672606032063

# ======================
# 🔧 INTENTS
# ======================
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ======================
# 🟢 VERIFY BUTTON
# ======================
class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="🔐 Verify เข้าเซิร์ฟ", style=discord.ButtonStyle.green)
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):

        role = interaction.guild.get_role(VERIFIED_ROLE_ID)

        if role in interaction.user.roles:
            return await interaction.response.send_message(
                "คุณยืนยันแล้วนะ ✅",
                ephemeral=True
            )
        if role is None:
            return await interaction.response.send_message(
        "❌ หา role ไม่เจอ (เช็ก Role ID)",
        ephemeral=True
    )

        await interaction.user.add_roles(role)

        await interaction.response.send_message(
            "🎉 Verify สำเร็จ!",
            ephemeral=True
        )

# ======================
# 📢 /verify
# ======================
@bot.tree.command(name="verify", description="ส่งหน้า Verify")
async def verify(interaction: discord.Interaction):

    embed = discord.Embed(
        title=" WELCOME TO AN SERVER",
        description="กดปุ่มด้านล่างเพื่อ Verify",
        color=0x2b2d31
    )

    embed.set_image(url="https://media.tenor.com/68Ad6sYP38cAAAAM/streched.gif")

    await interaction.response.send_message(embed=embed, view=VerifyView())

# ======================
# 📢 /announce
# ======================
@bot.tree.command(name="announce", description="ส่งประกาศ")
@app_commands.describe(
    title="หัวข้อ",
    message="ข้อความ",
    ping="แท็ก @everyone ไหม",
    link="ลิ้ง",
    image="รูป"
)
@app_commands.choices(color=[
    app_commands.Choice(name="🔴 แดง", value="red"),
    app_commands.Choice(name="🔵 น้ำเงิน", value="blue"),
    app_commands.Choice(name="🟢 เขียว", value="green"),
])
async def announce(
    interaction: discord.Interaction,
    title: str,
    message: str,
    color: app_commands.Choice[str],
    ping: bool,
    link: str = None,
    image: discord.Attachment = None
):
    await interaction.response.defer(ephemeral=True)

    embed = {
        "title": title,
        "description": message,
        "color": 0x3498db
    }

    if link:
        embed["url"] = link

    if image:
        embed["image"] = {"url": image.url}

    data = {
        "username": "ฝากบอก",
        "content": "@everyone" if ping else "",
        "embeds": [embed]
    }

    requests.post(WEBHOOK_ANNOUNCE, json=data)

    await interaction.followup.send("ส่งสำเร็จ ✅", ephemeral=True)

# ======================
# 🚀 READY
# ======================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

bot.run("MTQyOTYwNjQ1ODUwODQ0Mzc0OA.GMJ01j.zQ4ScaMZ275kV2xZzRfEyZ9rBKBv185hh58zrE")