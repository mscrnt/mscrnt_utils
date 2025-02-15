FROM python:3.10-slim-bullseye

# Set non-interactive mode to avoid warnings
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies
RUN apt-get -qy update && \
    apt-get -qy install --no-install-recommends \
    apt-utils \
    libgl1 \
    libglib2.0-0 \  
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "/app/agent.py" ]
