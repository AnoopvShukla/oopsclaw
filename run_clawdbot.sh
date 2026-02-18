#!/bin/bash

# WhatsAppBot Core - Production Start Script
# 
# This script manages the startup of the WhatsAppBot Core application.
# It handles environment configuration, binary location discovery,
# and graceful fallback mechanisms.
#
# Author: AnoopvShukla
# Version: 2.0.0
# License: MIT

set -e  # Exit on error
set -u  # Exit on undefined variable

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
export WAB_NODE_DIR="${WAB_NODE_DIR:-/root/nodejs}"
export WAB_BOT_DIR="${WAB_BOT_DIR:-/root/.whatsappbot-bin}"
export PATH="$WAB_NODE_DIR/bin:$WAB_BOT_DIR:$PATH"

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case "$level" in
        INFO)
            echo -e "${GREEN}[INFO]${NC} [$timestamp] $message"
            ;;
        WARN)
            echo -e "${YELLOW}[WARN]${NC} [$timestamp] $message" >&2
            ;;
        ERROR)
            echo -e "${RED}[ERROR]${NC} [$timestamp] $message" >&2
            ;;
    esac
}

# Check if binary exists and is executable
check_binary() {
    local path="$1"
    if [ -f "$path" ] && [ -x "$path" ]; then
        return 0
    fi
    return 1
}

# Find the WhatsApp bot binary
find_bot_binary() {
    local binary_name="whatsappbot"
    
    # Priority 1: Dedicated bot directory
    if check_binary "$WAB_BOT_DIR/$binary_name"; then
        echo "$WAB_BOT_DIR/$binary_name"
        return 0
    fi
    
    # Priority 2: Node.js bin directory
    if check_binary "$WAB_NODE_DIR/bin/$binary_name"; then
        echo "$WAB_NODE_DIR/bin/$binary_name"
        return 0
    fi
    
    # Priority 3: System PATH
    if command -v "$binary_name" &> /dev/null; then
        echo "$(command -v $binary_name)"
        return 0
    fi
    
    # Priority 4: Legacy clawdbot name (backward compatibility)
    binary_name="clawdbot"
    if check_binary "$WAB_BOT_DIR/$binary_name"; then
        log WARN "Using legacy binary name 'clawdbot' - consider upgrading"
        echo "$WAB_BOT_DIR/$binary_name"
        return 0
    fi
    
    if check_binary "$WAB_NODE_DIR/bin/$binary_name"; then
        log WARN "Using legacy binary name 'clawdbot' - consider upgrading"
        echo "$WAB_NODE_DIR/bin/$binary_name"
        return 0
    fi
    
    if command -v "$binary_name" &> /dev/null; then
        log WARN "Using legacy binary name 'clawdbot' - consider upgrading"
        echo "$(command -v $binary_name)"
        return 0
    fi
    
    return 1
}

# Main execution
main() {
    log INFO "WhatsAppBot Core - Starting up..."
    log INFO "Node.js directory: $WAB_NODE_DIR"
    log INFO "Bot binary directory: $WAB_BOT_DIR"
    
    # Find the bot binary
    local bot_binary
    if ! bot_binary=$(find_bot_binary); then
        log ERROR "WhatsApp bot binary not found in any search location"
        log ERROR "Searched locations:"
        log ERROR "  - $WAB_BOT_DIR/whatsappbot"
        log ERROR "  - $WAB_NODE_DIR/bin/whatsappbot"
        log ERROR "  - System PATH"
        log ERROR "  - Legacy: $WAB_BOT_DIR/clawdbot (backward compatibility)"
        log ERROR "  - Legacy: $WAB_NODE_DIR/bin/clawdbot (backward compatibility)"
        exit 1
    fi
    
    log INFO "Found bot binary at: $bot_binary"
    
    # Execute the bot with all provided arguments
    log INFO "Executing bot with arguments: $*"
    exec "$bot_binary" "$@"
}

# Run main function
main "$@"
