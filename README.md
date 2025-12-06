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

### Option 1: Docker (Recommended)

1. Build the Docker image:
```bash
docker build -t decision-helper-bot .
```

2. Create a Docker volume for model caching:
```bash
docker volume create decision-bot-cache
```

3. Run the container:
```bash
docker run -d \
  --name decision-helper-bot \
  --restart unless-stopped \
  -e BOT_TOKEN="your_bot_token_here" \
  -v decision-bot-cache:/app/model_cache \
  decision-helper-bot
```

The model (~700MB) will be downloaded on first run and cached in the Docker volume for future use.

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
- Docker image based on `python:3.11-slim` for minimal size
- Model cache persisted in Docker volume to avoid re-downloading

## Docker Details

The Docker setup includes:
- **Dockerfile**: Uses Python 3.11 slim image (~150MB base)
- **Persistent storage**: Model cache stored in Docker volume
- **Auto-restart**: Container restarts automatically on failure
- **Memory usage**: Approximately 2-3GB RAM

Optional: Add memory limits to the docker run command:
```bash
docker run -d \
  --name decision-helper-bot \
  --restart unless-stopped \
  --memory="3g" \
  --memory-reservation="2g" \
  -e BOT_TOKEN="your_token" \
  -v decision-bot-cache:/app/model_cache \
  decision-helper-bot
```

