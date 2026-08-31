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
1: "22936",
2: "26260",
3: "26260",
4: "64974",
5: "64974",
6: "49618",
7: "49618",
8: "92230",
9: "92230",
10: "29396",
11: "29396",
12: "96638",
13: "96638",
14: "62763",
15: "62763",
16: "23102",
17: "23102",
18: "36340",
19: "36340",
20: "67986",
21: "67986",
22: "71307",
23: "71307",
24: "13668",
25: "13668",
26: "39088",
27: "39088",
28: "93439",
29: "93439",
30: "36826",
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


