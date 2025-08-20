# dbcreds/backends/windows.py
"""
Windows Credential Manager backend.

This backend provides secure credential storage using Windows Credential Manager
through the Windows API.
"""

import ctypes
import ctypes.wintypes
import json
import sys
from typing import Any, Dict, Optional, Tuple


from dbcreds.backends.base import CredentialBackend


class CREDENTIAL(ctypes.Structure):
    """Windows CREDENTIAL structure."""

    _fields_ = [
        ("Flags", ctypes.wintypes.DWORD),
        ("Type", ctypes.wintypes.DWORD),
        ("TargetName", ctypes.wintypes.LPWSTR),
        ("Comment", ctypes.wintypes.LPWSTR),
        ("LastWritten", ctypes.wintypes.FILETIME),
        ("CredentialBlobSize", ctypes.wintypes.DWORD),
        ("CredentialBlob", ctypes.POINTER(ctypes.c_char)),
        ("Persist", ctypes.wintypes.DWORD),
        ("AttributeCount", ctypes.wintypes.DWORD),
        ("Attributes", ctypes.c_void_p),
        ("TargetAlias", ctypes.wintypes.LPWSTR),
        ("UserName", ctypes.wintypes.LPWSTR),
    ]


class WindowsCredentialBackend(CredentialBackend):
    """
    Windows Credential Manager backend.

    Uses the Windows API to securely store credentials in the Windows
    Credential Manager.
    """

    CRED_TYPE_GENERIC = 1
    CRED_PERSIST_LOCAL_MACHINE = 2

    def __init__(self):
        """Initialize Windows API functions."""
        if sys.platform != "win32":
            raise RuntimeError("Windows Credential Manager is only available on Windows")

        self.advapi32 = ctypes.windll.advapi32

        # CredReadW
        self.advapi32.CredReadW.argtypes = [
            ctypes.wintypes.LPCWSTR,
            ctypes.wintypes.DWORD,
            ctypes.wintypes.DWORD,
            ctypes.POINTER(ctypes.POINTER(CREDENTIAL)),
        ]
        self.advapi32.CredReadW.restype = ctypes.wintypes.BOOL

        # CredWriteW
        self.advapi32.CredWriteW.argtypes = [ctypes.POINTER(CREDENTIAL), ctypes.wintypes.DWORD]
        self.advapi32.CredWriteW.restype = ctypes.wintypes.BOOL

        # CredDeleteW
        self.advapi32.CredDeleteW.argtypes = [
            ctypes.wintypes.LPCWSTR,
            ctypes.wintypes.DWORD,
            ctypes.wintypes.DWORD,
        ]
        self.advapi32.CredDeleteW.restype = ctypes.wintypes.BOOL

        # CredFree
        self.advapi32.CredFree.argtypes = [ctypes.c_void_p]

    def is_available(self) -> bool:
        """Check if Windows Credential Manager is available."""
        return sys.platform == "win32"

    def get_credential(self, key: str) -> Optional[Tuple[str, str, Dict[str, Any]]]:
        """Retrieve credential from Windows Credential Manager."""
        cred_ptr = ctypes.POINTER(CREDENTIAL)()

        success = self.advapi32.CredReadW(key, self.CRED_TYPE_GENERIC, 0, ctypes.byref(cred_ptr))

        if not success:
            return None

        try:
            cred = cred_ptr.contents
            username = cred.UserName if cred.UserName else ""

            # Extract credential blob
            blob_size = cred.CredentialBlobSize
            if blob_size > 0:
                # Credential blob contains JSON with password and metadata
                blob_data = ctypes.string_at(cred.CredentialBlob, blob_size)
                blob_str = blob_data.decode("utf-16le", errors="ignore").rstrip("\x00")

                try:
                    data = json.loads(blob_str)
                    password = data.pop("password", "")
                    return (username, password, data)
                except json.JSONDecodeError:
                    # Fallback for old format (password only)
                    return (username, blob_str, {})
            else:
                return (username, "", {})
        finally:
            self.advapi32.CredFree(cred_ptr)

    def set_credential(self, key: str, username: str, password: str, metadata: Dict[str, Any]) -> bool:
        """Store credential in Windows Credential Manager."""
        # First delete any existing credential
        self.delete_credential(key)

        # Prepare credential data as JSON
        data = {"password": password, **metadata}
        blob_str = json.dumps(data)
        blob_bytes = blob_str.encode("utf-16le")

        # Create credential structure
        cred = CREDENTIAL()
        cred.Type = self.CRED_TYPE_GENERIC
        cred.Persist = self.CRED_PERSIST_LOCAL_MACHINE
        cred.TargetName = ctypes.c_wchar_p(key)
        cred.UserName = ctypes.c_wchar_p(username)
        cred.CredentialBlobSize = len(blob_bytes)
        cred.CredentialBlob = ctypes.cast(
            ctypes.create_string_buffer(blob_bytes), ctypes.POINTER(ctypes.c_char)
        )

        success = self.advapi32.CredWriteW(ctypes.byref(cred), 0)
        return bool(success)

    def delete_credential(self, key: str) -> bool:
        """Delete credential from Windows Credential Manager."""
        success = self.advapi32.CredDeleteW(key, self.CRED_TYPE_GENERIC, 0)
        return bool(success)
