import os
import random
import json
import telebot
from telebot import types
import threading
import time

from yes_no import YES_PREFIXES, YES_CORES, YES_SUFFIXES
from yes_no import NO_PREFIXES, NO_CORES, NO_SUFFIXES

# Get bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")

bot = telebot.TeleBot(BOT_TOKEN)

# Store active chat IDs for periodic memory sending
active_chats = set()

# Load funny moments
FUNNY_MOMENTS_PATH = os.path.join(os.path.dirname(__file__), 'data', 'funny_moments.json')
funny_moments = []

try:
    with open(FUNNY_MOMENTS_PATH, 'r', encoding='utf-8') as f:
        funny_moments = json.load(f)
    print(f"Loaded {len(funny_moments)} funny moments from {FUNNY_MOMENTS_PATH}")
except FileNotFoundError:
    print(f"Warning: {FUNNY_MOMENTS_PATH} not found. /good_memory command will not work.")
except Exception as e:
    print(f"Error loading funny moments: {e}")

print(f"Total number of yes phrases: {len(YES_PREFIXES) * len(YES_CORES) * len(YES_SUFFIXES)}")
print(f"Total number of no phrases: {len(NO_PREFIXES) * len(NO_CORES) * len(NO_SUFFIXES)}")

def random_yes_or_no():
    """Return a random composite yes or no phrase built from prefix + core + suffix"""
    decision = random.choice(["yes", "no"])
    
    if decision == "yes":
        prefix = random.choice(YES_PREFIXES)
        core = random.choice(YES_CORES)
        suffix = random.choice(YES_SUFFIXES)
        # Build the phrase and clean up extra spaces
        phrase = f"{prefix} {core}{suffix}".strip()
        # Replace double spaces with single space
        phrase = " ".join(phrase.split())
        return phrase
    else:
        prefix = random.choice(NO_PREFIXES)
        core = random.choice(NO_CORES)
        suffix = random.choice(NO_SUFFIXES)
        # Build the phrase and clean up extra spaces
        phrase = f"{prefix} {core}{suffix}".strip()
        # Replace double spaces with single space
        phrase = " ".join(phrase.split())
        return phrase


def format_funny_moment(moment):
    """Format a funny moment as a text message"""
    if not moment:
        return "No funny moments available 😢"
    
    # Build the message
    header = f"Good Memory from {moment['date']}\n"
    header += "=" * 40 + "\n\n"
    
    # Add all messages
    messages_text = ""
    for msg in moment['messages']:
        messages_text += f"[{msg['time']}] {msg['sender']}: {msg['text']}\n"
    
    return header + messages_text


def get_random_funny_moment():
    """Get a random funny moment from the loaded list"""
    if not funny_moments:
        return None
    return random.choice(funny_moments)


def send_periodic_memories():
    """Send a nice memory to all active chats every 7 days"""
    # Wait 7 days (in seconds)
    SEVEN_DAYS = 7 * 24 * 60 * 60
    
    while True:
        time.sleep(SEVEN_DAYS)
        
        # Send a memory to all active chats
        for chat_id in list(active_chats):
            try:
                moment = get_random_funny_moment()
                if moment:
                    formatted_text = "🌟 Weekly Good Memory 🌟\n\n" + format_funny_moment(moment)
                    bot.send_message(chat_id, formatted_text)
                else:
                    bot.send_message(chat_id, "Time for a good memory, but none available 😢")
            except Exception as e:
                print(f"Error sending periodic memory to chat {chat_id}: {e}")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Handle the /start command"""
    # Add this chat to active chats for periodic memories
    active_chats.add(message.chat.id)
    print(f"Chat {message.chat.id} added to active chats. Total active chats: {len(active_chats)}")
    
    welcome_text = "Ask me anything, I will help you decide!\n\nCommands:\n/yes_or_no - Get a random yes/no answer\n/number_1_10 - Get a random number from 1 to 10\n/good_memory - Get a random fun moment from the past\n\n✨ You'll receive a nice memory every 7 days!"
    bot.reply_to(message, welcome_text)


@bot.message_handler(commands=['yes_or_no'])
def yes_or_no_command(message):
    """Handle the /yes_or_no command"""
    answer = random_yes_or_no()
    bot.reply_to(message, answer)


@bot.message_handler(commands=['number_1_10'])
def number_command(message):
    """Handle the /number_1_10 command"""
    number = random.randint(1, 10)
    bot.reply_to(message, str(number))


@bot.message_handler(commands=['good_memory'])
def good_memory_command(message):
    """Handle the /good_memory command"""
    moment = get_random_funny_moment()
    if moment:
        formatted_text = format_funny_moment(moment)
        bot.reply_to(message, formatted_text)
    else:
        bot.reply_to(message, "Sorry, no funny moments available 😢")


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
    
    # Start the periodic memory sender in a background thread
    memory_thread = threading.Thread(target=send_periodic_memories, daemon=True)
    memory_thread.start()
    print("Periodic memory sender started (will send every 7 days)")
    
    bot.infinity_polling()
