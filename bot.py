import os
import random
import telebot
from telebot import types

# Get bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")

bot = telebot.TeleBot(BOT_TOKEN)

# Pre-defined lists of "yes" and "no" synonyms
YES_PHRASES = [
    "Absolutely!",
    "Yes!",
    "Definitely!",
    "Go for it!",
    "Without a doubt!",
    "Of course!",
    "Sure thing!",
    "Why not?",
    "You bet!",
    "Indeed!",
    "Certainly!",
    "For sure!",
    "Totally!",
    "All the way!",
    "I'm in!",
    "100%!",
    "Affirmative!",
    "Do it!",
    "By all means!",
    "You have my blessing!",
    "Make it happen!",
    "Full steam ahead!",
    "Green light!",
    "Go ahead!",
    "Yep!",
    "Yup!",
    "Yeah!",
    "Uh-huh!",
    "Roger that!",
    "Positive!",
    "Sounds good!",
    "I'm down!",
    "Count me in!",
    "Heck yeah!",
    "Hell yeah!",
    "Damn right!",
    "You should!",
    "It's a go!",
    "Thumbs up!",
    "Right on!",
]

NO_PHRASES = [
    "No.",
    "Nope.",
    "Absolutely not!",
    "Not a chance!",
    "No way!",
    "I don't think so.",
    "Better not.",
    "Definitely not!",
    "Not today.",
    "Hard pass.",
    "Nah.",
    "Negative.",
    "Nope, nope, nope!",
    "Don't do it!",
    "I wouldn't.",
    "Maybe skip this one.",
    "Not recommended.",
    "Red flag!",
    "Abort mission!",
    "Think twice.",
    "Probably not.",
    "Not your best idea.",
    "Pass.",
    "No go.",
    "Thumbs down.",
    "Forget it.",
    "Not happening.",
    "No can do.",
    "Not on my watch!",
    "Don't even think about it!",
    "Step back.",
    "Denied.",
    "Sorry, no.",
    "Afraid not.",
    "Not this time.",
    "Hold off.",
    "Bad idea.",
    "Veto!",
    "Never!",
    "Not in a million years!",
]


def random_yes_or_no():
    """Return a random yes or no phrase from pre-defined lists"""
    decision = random.choice(["yes", "no"])
    if decision == "yes":
        return random.choice(YES_PHRASES)
    else:
        return random.choice(NO_PHRASES)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Handle the /start command"""
    welcome_text = "Ask me anything, I will help you decide! Or just press /yes_or_no"
    bot.reply_to(message, welcome_text)


@bot.message_handler(commands=['yes_or_no'])
def yes_or_no_command(message):
    """Handle the /yes_or_no command"""
    answer = random_yes_or_no()
    bot.reply_to(message, answer)


@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    """Handle voice messages"""
    answer = random_yes_or_no()
    bot.reply_to(message, answer)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    """Handle photo messages"""
    answer = random_yes_or_no()
    bot.reply_to(message, answer)


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    """Handle all text messages"""
    answer = random_yes_or_no()
    bot.reply_to(message, answer)


if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
