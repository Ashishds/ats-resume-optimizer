#!/bin/bash

echo "Building ATS Resume Optimizer for Render..."

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Build React frontend
echo "Building React frontend..."
npm run build

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Build complete!"
