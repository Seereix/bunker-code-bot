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
    1: "36826",

    2: "60006",
    3: "60006",

    4: "04667",
    5: "04667",

    6: "48879",
    7: "48879",

    8: "80388",
    9: "80388",

    10: "06282",
    11: "06282",

    12: "68097",
    13: "68097",

    14: "83669",
    15: "83669",

    16: "32769",
    17: "32769",

    18: "20874",
    19: "20874",

    20: "06892",
    21: "06892",

    22: "67989",
    23: "67989",

    24: "78629",
    25: "78629",

    26: "88670",
    27: "88670",

    28: "89790",
    29: "89790",

    30: "96997",
    31: "96997"
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


