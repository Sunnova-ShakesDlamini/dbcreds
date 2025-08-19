# dbcreds/core/clipboard.py
"""
Secure clipboard management with automatic clearing.

Provides secure clipboard operations with automatic timeout
to prevent sensitive data from remaining in clipboard.
"""

import platform
import threading
import time
from typing import Optional

import pyperclip
from loguru import logger

from dbcreds.core.exceptions import SecurityError


class SecureClipboard:
    """
    Secure clipboard manager with auto-clear functionality.
    
    Features:
    - Automatic clipboard clearing after timeout
    - Secure overwriting of clipboard contents
    - Platform-specific optimizations
    - Thread-safe operations
    """
    
    def __init__(self, default_timeout: int = 45):
        """
        Initialize secure clipboard manager.
        
        Args:
            default_timeout: Default timeout in seconds before clearing
        """
        self.default_timeout = default_timeout
        self._clear_timer: Optional[threading.Timer] = None
        self._lock = threading.Lock()
        self._original_content: Optional[str] = None
        
    def copy_sensitive(self, 
                      data: str, 
                      clear_after: Optional[int] = None,
                      restore_original: bool = True) -> bool:
        """
        Copy sensitive data to clipboard with auto-clear.
        
        Args:
            data: Sensitive data to copy
            clear_after: Seconds before clearing (default: self.default_timeout)
            restore_original: Whether to restore original clipboard content
            
        Returns:
            True if successful
        """
        try:
            with self._lock:
                # Cancel any existing timer
                self._cancel_timer()
                
                # Store original clipboard content if needed
                if restore_original:
                    try:
                        self._original_content = pyperclip.paste()
                    except Exception:
                        self._original_content = None
                
                # Copy sensitive data
                pyperclip.copy(data)
                
                # Set up auto-clear timer
                timeout = clear_after if clear_after is not None else self.default_timeout
                if timeout > 0:
                    self._clear_timer = threading.Timer(
                        timeout,
                        self._clear_clipboard_callback,
                        args=(restore_original,)
                    )
                    self._clear_timer.daemon = True
                    self._clear_timer.start()
                    
                logger.debug(f"Copied sensitive data to clipboard, will clear in {timeout}s")
                return True
                
        except Exception as e:
            logger.error(f"Failed to copy to clipboard: {e}")
            return False
    
    def _clear_clipboard_callback(self, restore_original: bool = False) -> None:
        """Callback for timer to clear clipboard."""
        try:
            self.clear_clipboard(restore_original=restore_original)
        except Exception as e:
            logger.error(f"Failed to clear clipboard: {e}")
    
    def clear_clipboard(self, 
                       restore_original: bool = False,
                       secure_overwrite: bool = True) -> bool:
        """
        Clear clipboard contents securely.
        
        Args:
            restore_original: Restore original clipboard content
            secure_overwrite: Overwrite with random data before clearing
            
        Returns:
            True if successful
        """
        try:
            with self._lock:
                # Cancel timer if active
                self._cancel_timer()
                
                if secure_overwrite:
                    # Overwrite with random data multiple times
                    import secrets
                    for _ in range(3):
                        random_data = secrets.token_hex(32)
                        pyperclip.copy(random_data)
                        time.sleep(0.01)  # Brief pause to ensure clipboard update
                
                # Final clear or restore
                if restore_original and self._original_content is not None:
                    pyperclip.copy(self._original_content)
                    logger.debug("Restored original clipboard content")
                else:
                    pyperclip.copy("")
                    logger.debug("Cleared clipboard")
                
                self._original_content = None
                return True
                
        except Exception as e:
            logger.error(f"Failed to clear clipboard: {e}")
            return False
    
    def _cancel_timer(self) -> None:
        """Cancel any active clear timer."""
        if self._clear_timer and self._clear_timer.is_alive():
            self._clear_timer.cancel()
            self._clear_timer = None
    
    def immediate_clear(self) -> bool:
        """
        Immediately clear clipboard without waiting for timeout.
        
        Returns:
            True if successful
        """
        return self.clear_clipboard(secure_overwrite=True)
    
    @staticmethod
    def is_available() -> bool:
        """
        Check if clipboard operations are available.
        
        Returns:
            True if clipboard is available
        """
        try:
            # Test clipboard availability
            original = pyperclip.paste()
            test_data = "test"
            pyperclip.copy(test_data)
            result = pyperclip.paste() == test_data
            pyperclip.copy(original)  # Restore
            return result
            
        except Exception:
            return False
    
    @staticmethod
    def get_platform_info() -> dict:
        """
        Get platform-specific clipboard information.
        
        Returns:
            Dictionary with platform clipboard details
        """
        info = {
            "platform": platform.system(),
            "clipboard_available": SecureClipboard.is_available(),
        }
        
        # Platform-specific details
        if platform.system() == "Darwin":  # macOS
            info["clipboard_type"] = "pbcopy/pbpaste"
        elif platform.system() == "Windows":
            info["clipboard_type"] = "Windows Clipboard API"
        elif platform.system() == "Linux":
            # Check for X11 or Wayland
            import os
            if os.environ.get("WAYLAND_DISPLAY"):
                info["clipboard_type"] = "Wayland (wl-copy/wl-paste)"
            elif os.environ.get("DISPLAY"):
                info["clipboard_type"] = "X11 (xclip/xsel)"
            else:
                info["clipboard_type"] = "No display server"
                
        return info


class ClipboardMonitor:
    """
    Monitor clipboard for security purposes.
    
    Can detect if sensitive data remains in clipboard
    and alert or auto-clear as needed.
    """
    
    def __init__(self, secure_clipboard: SecureClipboard):
        """
        Initialize clipboard monitor.
        
        Args:
            secure_clipboard: SecureClipboard instance to use
        """
        self.secure_clipboard = secure_clipboard
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._sensitive_patterns: list = []
        
    def add_sensitive_pattern(self, pattern: str) -> None:
        """
        Add a pattern to detect sensitive data.
        
        Args:
            pattern: Regular expression pattern for sensitive data
        """
        import re
        self._sensitive_patterns.append(re.compile(pattern))
        
    def start_monitoring(self, check_interval: int = 5) -> None:
        """
        Start monitoring clipboard for sensitive data.
        
        Args:
            check_interval: Seconds between clipboard checks
        """
        if self._monitoring:
            return
            
        self._monitoring = True
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(check_interval,),
            daemon=True
        )
        self._monitor_thread.start()
        logger.info("Started clipboard monitoring")
        
    def stop_monitoring(self) -> None:
        """Stop monitoring clipboard."""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=1)
        logger.info("Stopped clipboard monitoring")
        
    def _monitor_loop(self, check_interval: int) -> None:
        """
        Main monitoring loop.
        
        Args:
            check_interval: Seconds between checks
        """
        while self._monitoring:
            try:
                content = pyperclip.paste()
                if self._contains_sensitive_data(content):
                    logger.warning("Sensitive data detected in clipboard")
                    self.secure_clipboard.clear_clipboard(secure_overwrite=True)
                    
            except Exception as e:
                logger.debug(f"Clipboard monitoring error: {e}")
                
            time.sleep(check_interval)
            
    def _contains_sensitive_data(self, content: str) -> bool:
        """
        Check if content contains sensitive data.
        
        Args:
            content: Clipboard content to check
            
        Returns:
            True if sensitive data detected
        """
        if not content or not self._sensitive_patterns:
            return False
            
        for pattern in self._sensitive_patterns:
            if pattern.search(content):
                return True
                
        return False