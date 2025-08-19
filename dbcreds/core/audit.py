# dbcreds/core/audit.py
"""
Git-based audit trail for credential operations.

Provides version control and cryptographic signatures
for all credential changes, enabling audit trails and rollback.
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger
from pydantic import BaseModel, Field

from dbcreds.core.exceptions import AuditError


class AuditEntry(BaseModel):
    """Model for audit log entry."""
    
    timestamp: datetime
    action: str  # create, update, delete, access
    credential_id: str
    user: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    commit_hash: Optional[str] = None
    signature_valid: Optional[bool] = None


class GitAuditManager:
    """
    Git-based audit trail manager with signed commits.
    
    Features:
    - Automatic git commits for all credential operations
    - Cryptographic signatures for commit integrity
    - Rollback functionality
    - Comprehensive audit log queries
    """
    
    def __init__(self, 
                 audit_dir: Optional[Path] = None,
                 sign_commits: bool = True,
                 signing_key: Optional[str] = None):
        """
        Initialize git audit manager.
        
        Args:
            audit_dir: Directory for audit repository
            sign_commits: Whether to sign commits with GPG
            signing_key: GPG key for signing (uses default if None)
        """
        self.audit_dir = audit_dir or Path.home() / ".dbcreds" / "audit"
        self.sign_commits = sign_commits
        self.signing_key = signing_key
        
        # Initialize git repository if needed
        self._init_repo()
        
    def _init_repo(self) -> None:
        """Initialize git repository for audit trail."""
        try:
            self.audit_dir.mkdir(parents=True, exist_ok=True)
            
            # Check if already initialized
            git_dir = self.audit_dir / ".git"
            if not git_dir.exists():
                self._run_git("init")
                
                # Configure git
                self._run_git("config", "user.name", "DBCreds Audit")
                self._run_git("config", "user.email", "audit@dbcreds.local")
                
                if self.sign_commits:
                    self._run_git("config", "commit.gpgsign", "true")
                    if self.signing_key:
                        self._run_git("config", "user.signingkey", self.signing_key)
                
                # Create initial commit
                readme_path = self.audit_dir / "README.md"
                readme_path.write_text("# DBCreds Audit Log\n\nThis repository contains the audit trail for all credential operations.\n")
                self._run_git("add", "README.md")
                self._run_git("commit", "-m", "Initialize audit repository")
                
                logger.info(f"Initialized audit repository at {self.audit_dir}")
                
        except Exception as e:
            logger.error(f"Failed to initialize audit repository: {e}")
            raise AuditError(f"Audit initialization failed: {e}")
    
    def _run_git(self, *args: str) -> str:
        """
        Run git command in audit directory.
        
        Args:
            *args: Git command arguments
            
        Returns:
            Command output
        """
        try:
            result = subprocess.run(
                ["git"] + list(args),
                cwd=self.audit_dir,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {e.stderr}")
            raise AuditError(f"Git operation failed: {e.stderr}")
    
    def log_action(self,
                  action: str,
                  credential_id: str,
                  user: Optional[str] = None,
                  metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Log a credential action to audit trail.
        
        Args:
            action: Type of action (create, update, delete, access)
            credential_id: Identifier of the affected credential
            user: User who performed the action
            metadata: Additional metadata about the action
            
        Returns:
            Git commit hash
        """
        try:
            # Prepare audit entry
            entry = AuditEntry(
                timestamp=datetime.utcnow(),
                action=action,
                credential_id=credential_id,
                user=user or os.environ.get("USER", "unknown"),
                metadata=metadata or {}
            )
            
            # Write audit file
            audit_file = self.audit_dir / f"{credential_id}.json"
            
            # Load existing entries if file exists
            entries = []
            if audit_file.exists():
                try:
                    existing_data = json.loads(audit_file.read_text())
                    entries = existing_data.get("entries", [])
                except Exception:
                    pass
            
            # Append new entry
            entries.append(entry.dict())
            
            # Write updated audit log
            audit_data = {
                "credential_id": credential_id,
                "last_action": action,
                "last_modified": entry.timestamp.isoformat(),
                "entries": entries
            }
            
            audit_file.write_text(json.dumps(audit_data, indent=2, default=str))
            
            # Commit to git
            self._run_git("add", audit_file.name)
            
            commit_message = f"{action.upper()}: {credential_id}\n\n"
            commit_message += f"User: {entry.user}\n"
            commit_message += f"Timestamp: {entry.timestamp.isoformat()}\n"
            if metadata:
                commit_message += f"Metadata: {json.dumps(metadata, indent=2)}\n"
            
            commit_output = self._run_git("commit", "-m", commit_message)
            
            # Extract commit hash
            commit_hash = self._run_git("rev-parse", "HEAD")
            
            logger.info(f"Audit logged: {action} on {credential_id} (commit: {commit_hash[:8]})")
            return commit_hash
            
        except Exception as e:
            logger.error(f"Failed to log audit action: {e}")
            raise AuditError(f"Audit logging failed: {e}")
    
    def get_history(self, 
                   credential_id: Optional[str] = None,
                   limit: int = 100) -> List[AuditEntry]:
        """
        Get audit history for credentials.
        
        Args:
            credential_id: Specific credential to query (None for all)
            limit: Maximum number of entries to return
            
        Returns:
            List of audit entries
        """
        try:
            entries = []
            
            if credential_id:
                # Get history for specific credential
                audit_file = self.audit_dir / f"{credential_id}.json"
                if audit_file.exists():
                    data = json.loads(audit_file.read_text())
                    for entry_data in data.get("entries", [])[-limit:]:
                        entry = AuditEntry(**entry_data)
                        entries.append(entry)
            else:
                # Get history for all credentials
                for audit_file in self.audit_dir.glob("*.json"):
                    if audit_file.name == "README.md":
                        continue
                        
                    try:
                        data = json.loads(audit_file.read_text())
                        for entry_data in data.get("entries", []):
                            entry = AuditEntry(**entry_data)
                            entries.append(entry)
                    except Exception as e:
                        logger.warning(f"Failed to read audit file {audit_file}: {e}")
                
                # Sort by timestamp and limit
                entries.sort(key=lambda x: x.timestamp, reverse=True)
                entries = entries[:limit]
            
            return entries
            
        except Exception as e:
            logger.error(f"Failed to retrieve audit history: {e}")
            return []
    
    def verify_signatures(self, 
                         since: Optional[str] = None) -> Dict[str, bool]:
        """
        Verify GPG signatures for commits.
        
        Args:
            since: Git revision to start from (e.g., "HEAD~10")
            
        Returns:
            Dictionary mapping commit hashes to signature validity
        """
        try:
            results = {}
            
            # Get commit list
            rev_range = f"{since}..HEAD" if since else "HEAD"
            commits = self._run_git("rev-list", rev_range).split("\n")
            
            for commit in commits:
                if not commit:
                    continue
                    
                try:
                    # Verify signature
                    self._run_git("verify-commit", commit)
                    results[commit] = True
                except AuditError:
                    results[commit] = False
                    
            return results
            
        except Exception as e:
            logger.error(f"Failed to verify signatures: {e}")
            return {}
    
    def rollback(self, 
                commit_hash: str,
                create_backup: bool = True) -> bool:
        """
        Rollback to a specific commit.
        
        Args:
            commit_hash: Git commit hash to rollback to
            create_backup: Whether to create backup branch
            
        Returns:
            True if successful
        """
        try:
            # Create backup branch if requested
            if create_backup:
                backup_branch = f"backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                self._run_git("branch", backup_branch)
                logger.info(f"Created backup branch: {backup_branch}")
            
            # Perform rollback
            self._run_git("reset", "--hard", commit_hash)
            
            logger.info(f"Rolled back to commit: {commit_hash}")
            return True
            
        except Exception as e:
            logger.error(f"Rollback failed: {e}")
            return False
    
    def export_audit_log(self, 
                        output_file: Path,
                        format: str = "json") -> bool:
        """
        Export audit log to file.
        
        Args:
            output_file: Path to export file
            format: Export format (json, csv)
            
        Returns:
            True if successful
        """
        try:
            entries = self.get_history(limit=None)
            
            if format == "json":
                data = [entry.dict() for entry in entries]
                output_file.write_text(json.dumps(data, indent=2, default=str))
                
            elif format == "csv":
                import csv
                
                with open(output_file, "w", newline="") as f:
                    if entries:
                        fieldnames = ["timestamp", "action", "credential_id", "user", "metadata"]
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        
                        for entry in entries:
                            row = entry.dict()
                            row["metadata"] = json.dumps(row["metadata"])
                            writer.writerow(row)
            else:
                raise ValueError(f"Unsupported format: {format}")
                
            logger.info(f"Exported audit log to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export audit log: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get audit statistics.
        
        Returns:
            Dictionary with audit statistics
        """
        try:
            entries = self.get_history(limit=None)
            
            if not entries:
                return {
                    "total_actions": 0,
                    "credentials_tracked": 0
                }
            
            # Calculate statistics
            stats = {
                "total_actions": len(entries),
                "credentials_tracked": len(set(e.credential_id for e in entries)),
                "actions_by_type": {},
                "actions_by_user": {},
                "first_action": min(e.timestamp for e in entries).isoformat(),
                "last_action": max(e.timestamp for e in entries).isoformat(),
            }
            
            # Count by action type
            for entry in entries:
                stats["actions_by_type"][entry.action] = \
                    stats["actions_by_type"].get(entry.action, 0) + 1
                stats["actions_by_user"][entry.user] = \
                    stats["actions_by_user"].get(entry.user, 0) + 1
                    
            return stats
            
        except Exception as e:
            logger.error(f"Failed to calculate statistics: {e}")
            return {}