#!/bin/bash
export NODE_DIR=/root/nodejs
export CLAWDBOT_DIR=/root/.clawdbot-bin
export PATH="$NODE_DIR/bin:$CLAWDBOT_DIR:$PATH"

# Find clawdbot
if [ -f "$CLAWDBOT_DIR/clawdbot" ]; then
    exec "$CLAWDBOT_DIR/clawdbot" "$@"
elif [ -f "$NODE_DIR/bin/clawdbot" ]; then
    exec "$NODE_DIR/bin/clawdbot" "$@"
elif command -v clawdbot &> /dev/null; then
    exec clawdbot "$@"
else
    echo "ERROR: clawdbot not found" >&2
    exit 1
fi
