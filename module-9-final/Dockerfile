# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including fonts and wget
RUN apt-get update && apt-get install -y \
    fonts-noto-cjk \
    wget \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create images directory
RUN mkdir -p /app/images

# Download sample images from googleapis
RUN cd /app/images && \
    wget -q https://storage.googleapis.com/generativeai-downloads/images/socks.jpg -O Socks.jpg && \
    wget -q https://storage.googleapis.com/generativeai-downloads/images/vegetables.jpg -O Vegetables.jpg && \
    wget -q https://storage.googleapis.com/generativeai-downloads/images/Japanese_Bento.png -O Japanese_bento.png && \
    wget -q https://storage.googleapis.com/generativeai-downloads/images/Cupcakes.jpg -O Cupcakes.jpg && \
    wget -q https://storage.googleapis.com/generativeai-downloads/images/origamis.jpg -O Origamis.jpg && \
    wget -q https://storage.googleapis.com/generativeai-downloads/images/fruits.jpg -O Fruits.jpg && \
    wget -q https://storage.googleapis.com/generativeai-downloads/images/cat.jpg -O Cat.jpg && \
    wget -q https://storage.googleapis.com/generativeai-downloads/images/pumpkins.jpg -O Pumpkins.jpg && \
    wget -q https://storage.googleapis.com/generativeai-downloads/images/breakfast.jpg -O Breakfast.jpg && \
    wget -q https://storage.googleapis.com/generativeai-downloads/images/bookshelf.jpg -O Bookshelf.jpg && \
    wget -q https://storage.googleapis.com/generativeai-downloads/images/spill.jpg -O Spill.jpg

# Copy application files
COPY . .

# Create output and logs directories
RUN mkdir -p /app/output /app/logs

# Set environment variables for Python
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Default command - run the standalone Python script
CMD ["python", "gemini_spatial_standalone.py"]