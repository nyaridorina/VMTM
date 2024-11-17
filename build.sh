#!/bin/bash

# Update package list and install system dependencies
apt-get update && apt-get install -y portaudio19-dev mpg123

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt
