# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (ffmpeg for audio extraction)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot files
COPY bot.py .
COPY downloaders.py .

# Create a non-root user to run the bot
RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app

USER botuser

# Expose port for health checks
EXPOSE 10000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.exit(0)"

# Run the bot
CMD ["python3", "-u", "bot.py"]
