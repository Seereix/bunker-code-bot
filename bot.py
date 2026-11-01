import os
import datetime
import time
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands


# ==========================================
# BUNKER CODES
# ==========================================

codes = {
    1: "66847",
    2: "66847",
    3: "67729",
    4: "67729",
    5: "79792",
    6: "79792",
    7: "98996",
    8: "98996",
    9: "82900",
    10: "82900",
    11: "73407",
    12: "73407",
    13: "79276",
    14: "79276",
    15: "99978",
    16: "99978",
    17: "94995",
    18: "94995",
    19: "42020",
    20: "42020",
    21: "29067",
    22: "29067",
    23: "99700",
    24: "99700",
    25: "90776",
    26: "90776",
    27: "00968",
    28: "00968",
    29: "07280",
    30: "07280",
    31: "No Code"
}



# ==========================================
# GET TODAY'S BUNKER CODE
# ==========================================

def bunker_code():

    # Get the current day using Algeria's timezone
    current_day = datetime.datetime.now(
        datetime.timezone.utc
    ).day

    # Find the code for today's day
    return codes[current_day]


# ==========================================
# ANTI-SPAM SETTINGS
# ==========================================

cooldowns = {}

# Users must wait 30 seconds between requests
COOLDOWN_SECONDS = 30


# ==========================================
# DISCORD BOT SETTINGS
# ==========================================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# ==========================================
# BOT READY
# ==========================================

@bot.event
async def on_ready():

    print(f"Logged in as {bot.user}")
    print("Bot is ready!")


# ==========================================
# MESSAGE HANDLER
# ==========================================

@bot.event
async def on_message(message):

    # Don't respond to the bot's own messages
    if message.author == bot.user:
        return


    # Check if the user typed "code"
    if message.content.lower().strip() == "code":

        user_id = message.author.id
        current_time = time.time()


        # ==========================================
        # CHECK ANTI-SPAM COOLDOWN
        # ==========================================

        if user_id in cooldowns:

            time_passed = current_time - cooldowns[user_id]

            if time_passed < COOLDOWN_SECONDS:

                remaining = int(COOLDOWN_SECONDS - time_passed) + 1

                

                return


        # ==========================================
        # RESET USER COOLDOWN
        # ==========================================

        cooldowns[user_id] = current_time


        # ==========================================
        # GET TODAY'S CODE
        # ==========================================

        code = bunker_code()


        # ==========================================
        # SEND CODE
        # ==========================================

        await message.channel.send(
            f"🔐 **BUNKER CODE:** `{code}`"
        )


    # Keep normal Discord commands working
    await bot.process_commands(message)


# ==========================================
# START BOT
# ==========================================

bot.run(os.getenv("DISCORD_TOKEN"))


