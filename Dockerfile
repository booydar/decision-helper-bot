# Use slim Python image for a lighter container
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code and dependencies
COPY bot.py .
COPY yes_no.py .
COPY data/ data/

# Run the bot
CMD ["python", "-u", "bot.py"]
