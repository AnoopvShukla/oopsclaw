#!/usr/bin/env python3
"""
WhatsAppBot Core - Credential Recovery Utility

This module provides utilities to fix and validate WhatsApp credentials
for the Baileys protocol implementation. It specifically addresses the
common issue where the 'registered' flag is incorrectly set to false
despite valid account credentials being present.

Author: AnoopvShukla
License: MIT
Version: 2.0.0
"""

import json
import logging
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_CREDS_PATH = Path.home() / ".whatsappbot" / "credentials" / "whatsapp" / "default" / "creds.json"
BACKUP_SUFFIX = ".backup"


class CredentialManager:
    """Manages WhatsApp credential validation and recovery."""
    
    def __init__(self, creds_path: Optional[Path] = None):
        """
        Initialize the credential manager.
        
        Args:
            creds_path: Path to credentials file. Uses default if not provided.
        """
        self.creds_path = creds_path or DEFAULT_CREDS_PATH
        logger.info(f"Initialized CredentialManager with path: {self.creds_path}")
    
    def validate_credentials(self) -> Tuple[bool, str]:
        """
        Validate that credential file exists and is accessible.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.creds_path.exists():
            msg = f"Credentials file not found at {self.creds_path}"
            logger.warning(msg)
            return False, msg
        
        if not self.creds_path.is_file():
            msg = f"Path exists but is not a file: {self.creds_path}"
            logger.error(msg)
            return False, msg
        
        try:
            # Verify file is readable and contains valid JSON
            with open(self.creds_path, 'r') as f:
                json.load(f)
            return True, "Credentials file is valid"
        except json.JSONDecodeError as e:
            msg = f"Invalid JSON in credentials file: {e}"
            logger.error(msg)
            return False, msg
        except Exception as e:
            msg = f"Error reading credentials: {e}"
            logger.error(msg)
            return False, msg
    
    def load_credentials(self) -> Optional[Dict]:
        """
        Load credentials from file.
        
        Returns:
            Credentials dictionary or None if loading fails.
        """
        try:
            with open(self.creds_path, 'r') as f:
                creds = json.load(f)
            logger.info("Successfully loaded credentials")
            return creds
        except Exception as e:
            logger.error(f"Failed to load credentials: {e}")
            return None
    
    def save_credentials(self, creds: Dict, create_backup: bool = True) -> bool:
        """
        Save credentials to file.
        
        Args:
            creds: Credentials dictionary to save.
            create_backup: Whether to create a backup of existing file.
        
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Create backup if requested and file exists
            if create_backup and self.creds_path.exists():
                backup_path = self.creds_path.with_suffix(self.creds_path.suffix + BACKUP_SUFFIX)
                import shutil
                shutil.copy2(self.creds_path, backup_path)
                logger.info(f"Created backup at {backup_path}")
            
            # Ensure parent directory exists
            self.creds_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write credentials
            with open(self.creds_path, 'w') as f:
                json.dump(creds, f, indent=2)
            
            logger.info("Successfully saved credentials")
            return True
        except Exception as e:
            logger.error(f"Failed to save credentials: {e}")
            return False
    
    def check_registration_status(self, creds: Dict) -> Dict[str, bool]:
        """
        Check the registration status indicators in credentials.
        
        Args:
            creds: Credentials dictionary.
        
        Returns:
            Dictionary with status indicators.
        """
        has_account = bool(creds.get("account"))
        has_me = bool(creds.get("me", {}).get("id"))
        registered = creds.get("registered", False)
        
        status = {
            "has_account": has_account,
            "has_me": has_me,
            "registered": registered,
            "needs_fix": has_account and has_me and not registered
        }
        
        logger.info(
            f"Registration status: account={has_account}, "
            f"me={has_me}, registered={registered}"
        )
        
        return status
    
    def fix_registration_flag(self) -> bool:
        """
        Fix the registration flag if needed.
        
        Returns:
            True if fix was applied or not needed, False on error.
        """
        # Validate credentials exist
        valid, msg = self.validate_credentials()
        if not valid:
            logger.error(f"Cannot fix credentials: {msg}")
            return False
        
        # Load credentials
        creds = self.load_credentials()
        if creds is None:
            return False
        
        # Check status
        status = self.check_registration_status(creds)
        
        if not status["needs_fix"]:
            logger.info("No fix needed - credentials are already correct")
            return True
        
        # Apply fix
        logger.warning("Detected registered=false bug - applying fix")
        creds["registered"] = True
        
        # Save updated credentials
        if self.save_credentials(creds, create_backup=True):
            logger.info("Successfully fixed registration flag: false -> true")
            return True
        else:
            logger.error("Failed to save fixed credentials")
            return False


def main():
    """
    Main entry point for the credential recovery utility.
    """
    logger.info("="*60)
    logger.info("WhatsAppBot Core - Credential Recovery Utility")
    logger.info("="*60)
    
    # Allow custom path from command line argument
    creds_path = None
    if len(sys.argv) > 1:
        creds_path = Path(sys.argv[1])
        logger.info(f"Using custom credentials path: {creds_path}")
    
    # Initialize manager
    manager = CredentialManager(creds_path)
    
    # Attempt to fix credentials
    try:
        success = manager.fix_registration_flag()
        
        if success:
            logger.info("✓ Credential recovery completed successfully")
            sys.exit(0)
        else:
            logger.error("✗ Credential recovery failed")
            sys.exit(1)
    
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
