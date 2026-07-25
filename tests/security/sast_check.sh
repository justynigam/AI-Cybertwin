#!/usr/bin/env bg
# Security Static Analysis (SAST) Scanner Script for CyberTwin AI

echo "=== Running Bandit Security Vulnerability Scanner ==="

if ! command -v bandit &> /dev/null; then
    echo "Bandit is not installed. Installing bandit..."
    pip install bandit
fi

bandit -r backend/ ml/ graph_engine/ behavior_twin/ -ll -ii

echo "=== SAST Security Scan Complete ==="
