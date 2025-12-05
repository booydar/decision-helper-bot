# Decision Helper Bot

A Telegram bot that helps you make decisions by generating creative "Yes" or "No" responses using AI (SmolLM-360M-Instruct).

## Features

- `/start` - Welcome message with instructions
- `/yes_or_no` - Get a random yes or no answer with AI-generated creative phrasing
- Responds to text, voice messages, and images with random yes/no answers
- Uses HuggingFace's SmolLM-360M-Instruct model for lightweight, creative responses

## Requirements

- Python 3.8+
- At least 2GB RAM (model is only 360M parameters)
- CPU is sufficient (no GPU required)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your bot token as an environment variable:
```bash
export BOT_TOKEN="your_bot_token_here"
```

3. Run the bot (first run will download the model ~700MB):
```bash
python bot.py
```

## Usage

1. Start a chat with your bot on Telegram
2. Send `/start` to get started
3. Use `/yes_or_no` or send any message (text, voice, or image) to get a random yes/no answer
4. The bot will generate creative phrases like "Absolutely!", "Not a chance", "Go for it!", etc.

## Technical Details

- Model: HuggingFaceTB/SmolLM-360M-Instruct (360M parameters)
- Optimized for CPU usage with float32 precision
- Lightweight enough to run on modest hardware

