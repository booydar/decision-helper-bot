import os
import random
import telebot
from telebot import types
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Get bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")

bot = telebot.TeleBot(BOT_TOKEN)

# Load the SmolLM model
print("Loading SmolLM-360M-Instruct model...")
model_name = "HuggingFaceTB/SmolLM-360M-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32,  # Use float32 for CPU compatibility
    device_map="auto"
)
print("Model loaded successfully!")


def generate_yes_or_no_phrase(decision: str):
    """
    Generate a creative phrase that means yes or no using SmolLM
    
    Args:
        decision: Either "yes" or "no"
    
    Returns:
        A generated phrase with the same meaning
    """
    if decision.lower() == "yes":
        prompt = """Task: Give one short phrase meaning "yes". Start your answer with >>> symbol.

Examples:
>>> Absolutely!
>>> Go for it! I dare you!

Now give me a DIFFERENT one:"""
    else:
        prompt = """Task: Give one short phrase meaning "no". Start your answer with >>> symbol.

Examples:
>>> Not a chance!
>>> No freaking way!

Now give me a DIFFERENT one:"""
    
    # Format as chat message
    messages = [{"role": "user", "content": prompt}]
    input_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    # Tokenize and generate
    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=15,  # Even shorter
            temperature=1.6,
            top_p=0.4,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
    
    # Decode and extract the response
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Split by the marker symbol
    if ">>>" in generated_text:
        parts = generated_text.split(">>>")
        # Get the last occurrence (the generated one, not examples)
        response = parts[-1].strip()
    else:
        # Fallback: try to extract after "assistant" or just use the end
        response = generated_text.split("assistant")[-1].strip()
    
    # Clean up: take only first line and remove extra punctuation/quotes
    response = response.split('\n')[0].strip()
    response = response.strip('"\'.,;')
    
    # If response is empty, too long, or still contains instruction text, use fallback
    if not response or "Task:" in response or "Example" in response:
        return "Yes!" if decision.lower() == "yes" else "No."
    
    return response


def random_yes_or_no():
    """Return a random yes or no decision and generate a creative phrase"""
    decision = random.choice(["yes", "no"])
    return generate_yes_or_no_phrase(decision)


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

