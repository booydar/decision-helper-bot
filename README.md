# Decision Helper Bot

A lightweight Telegram bot that helps you make decisions by providing creative "Yes" or "No" responses from pre-defined lists.

## Features

- `/start` - Welcome message with instructions
- `/yes_or_no` - Get a random yes or no answer with creative phrasing
- Responds to text, voice messages, and images with random yes/no answers
- Uses pre-defined lists of creative "yes" and "no" synonyms
- Lightweight and fast - no AI model required!

## Requirements

- Python 3.8+
- Minimal RAM requirements (~50MB)
- Works on any hardware (no GPU/CPU-intensive operations)

## Setup

### Option 1: Docker (Recommended)

1. Build the Docker image:
```bash
docker build -t decision-helper-bot .
```

2. Run the container:
```bash
docker run -d \
  --name decision-helper-bot \
  --restart unless-stopped \
  -e BOT_TOKEN="your_bot_token_here" \
  decision-helper-bot
```

To view logs:
```bash
docker logs -f decision-helper-bot
```

To stop the bot:
```bash
docker stop decision-helper-bot
docker rm decision-helper-bot
```

### Option 2: Manual Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your bot token as an environment variable:
```bash
export BOT_TOKEN="your_bot_token_here"
```

3. Run the bot:
```bash
python bot.py
```

## Usage

1. Start a chat with your bot on Telegram
2. Send `/start` to get started
3. Use `/yes_or_no` or send any message (text, voice, or image) to get a random yes/no answer
4. The bot will respond with creative phrases like:
   - **Yes phrases**: "Absolutely!", "Go for it!", "Full steam ahead!", "You bet!", etc.
   - **No phrases**: "Not a chance!", "Hard pass.", "Abort mission!", "Better not.", etc.

## Technical Details

- **No AI/ML models**: Uses pre-defined lists for instant responses
- **Lightweight**: Only requires the pyTelegramBotAPI library
- **Fast**: Instant responses with no model loading time
- **Resource-efficient**: Uses minimal CPU and RAM (~50MB)
- **Docker image**: Based on `python:3.11-slim` (~150MB total)

## Customization

You can easily customize the bot by editing the `YES_PHRASES` and `NO_PHRASES` lists in `bot.py` to add your own creative responses!

## Docker Details

The Docker setup includes:
- **Dockerfile**: Uses Python 3.11 slim image (~150MB)
- **Auto-restart**: Container restarts automatically on failure
- **Memory usage**: Approximately 50MB RAM

Optional: Add memory limits to the docker run command:
```bash
docker run -d \
  --name decision-helper-bot \
  --restart unless-stopped \
  --memory="256m" \
  --memory-reservation="128m" \
  -e BOT_TOKEN="your_token" \
  decision-helper-bot
```
