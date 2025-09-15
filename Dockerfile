# Use a lightweight Python image
FROM python:3.11-slim

# Install system dependencies required by PyMuPDF and Pillow
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libjpeg62-turbo \
    libpng16-16 \
    libfreetype6 \
    libharfbuzz0b \
    libfribidi0 \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your source code
COPY . .

# Default command (run your batch job)
CMD ["tail", "-f", "/dev/null"]
#CMD ["python", "process.py"]
