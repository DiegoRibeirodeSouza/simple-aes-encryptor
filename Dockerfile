FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-tk \
    xvfb \
    zenity \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip install customtkinter cryptography

# Create app directory
WORKDIR /app

# Copy source
COPY simple-encryptor/usr/bin/simple-encryptor /app/simple-encryptor

# Test script
RUN echo "import os\n\
    import sys\n\
    try:\n\
    os.environ['DISPLAY'] = ':99'\n\
    import subprocess\n\
    subprocess.Popen(['Xvfb', ':99'])\n\
    import time\n\
    time.sleep(2)\n\
    from simple_encryptor import ModernEncryptorApp\n\
    print('Import successful during test')\n\
    except Exception as e:\n\
    print(f'Test Failed: {e}')\n\
    sys.exit(1)\n\
    " > /app/test_run.py

# Rename for import
RUN cp /app/simple-encryptor /app/simple_encryptor.py

CMD ["python3", "/app/test_run.py"]
