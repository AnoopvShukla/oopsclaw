#!/bin/bash
set -e

# Load dynamic secrets
if [ -f /root/.clawdbot/gateway.env ]; then
    source /root/.clawdbot/gateway.env
fi

# Set up paths
export NODE_DIR=/root/nodejs
export CLAWDBOT_DIR=/root/.clawdbot-bin
export PATH="$NODE_DIR/bin:$CLAWDBOT_DIR:$PATH"

# Fix WhatsApp bug
echo "[supervisor-wrapper] Running WhatsApp fix..."
python3 /root/fix_whatsapp_registered.py 2>&1 || true

# Start gateway
echo "[supervisor-wrapper] Starting gateway on port 18789..."
exec /root/run_clawdbot.sh gateway --port 18789 --bind lan \
    --token "$CLAWDBOT_GATEWAY_TOKEN" --allow-unconfigured
