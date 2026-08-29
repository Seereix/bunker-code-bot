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
    1: "44032",
    2: "44032",

    3: "44396",
    4: "44396",

    5: "40684",
    6: "40684",

    7: "00179",
    8: "00179",

    9: "03132",
    10: "03132",

    11: "36379",
    12: "36379",

    13: "61926",
    14: "61926",

    15: "11822",
    16: "11822",

    17: "13763",
    18: "13763",

    19: "39346",
    20: "39346",

    21: "98797",
    22: "98797",

    23: "87221",
    24: "87221",

    25: "73293",
    26: "73293",

    27: "37669",
    28: "37669",

    29: "72423",
    30: "72423",

    31: "22936"
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


