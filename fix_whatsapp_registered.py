#!/usr/bin/env python3
"""Fix Baileys registered=false bug"""
import json
from pathlib import Path

CREDS_FILE = Path.home() / ".clawdbot/credentials/whatsapp/default/creds.json"

def fix_registered_flag():
    if not CREDS_FILE.exists():
        print(f"[fix-whatsapp] No creds at {CREDS_FILE}")
        return False
    try:
        with open(CREDS_FILE, 'r') as f:
            creds = json.load(f)
        has_account = bool(creds.get("account"))
        has_me = bool(creds.get("me", {}).get("id"))
        registered = creds.get("registered", False)
        print(f"[fix-whatsapp] account={has_account}, me={has_me}, registered={registered}")
        if has_account and has_me and not registered:
            print("[fix-whatsapp] FIXING registered=false -> true")
            creds["registered"] = True
            with open(CREDS_FILE, 'w') as f:
                json.dump(creds, f)
            return True
    except Exception as e:
        print(f"[fix-whatsapp] Error: {e}")
    return False

if __name__ == "__main__":
    fix_registered_flag()
