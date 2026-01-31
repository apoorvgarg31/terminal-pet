"""Git activity tracker using watchdog."""

import os
import subprocess
import threading
import time
from pathlib import Path
from typing import Callable, Optional, List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent


class GitEventHandler(FileSystemEventHandler):
    """Handle git-related file system events."""
    
    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback
        self._last_event_time = 0
        self._debounce_seconds = 2
    
    def on_modified(self, event: FileSystemEvent):
        if event.is_directory:
            return
        
        # Debounce rapid events
        now = time.time()
        if now - self._last_event_time < self._debounce_seconds:
            return
        self._last_event_time = now
        
        path = Path(event.src_path)
        
        # Check for git events
        if ".git" in path.parts:
            if path.name == "COMMIT_EDITMSG":
                # A commit is being made
                self.callback("commit")
            elif path.name == "FETCH_HEAD":
                # A pull/fetch happened
                self.callback("pull")
            elif "refs/remotes" in str(path):
                # A push might have happened
                self.callback("push")


class GitTracker:
    """Track git activity across repositories."""
    
    def __init__(self, callback: Callable[[str], None], repos: Optional[List[Path]] = None):
        self.callback = callback
        self.repos = repos or self._find_repos()
        self.observer = Observer()
        self._running = False
    
    def _find_repos(self) -> List[Path]:
        """Find git repositories in common locations."""
        repos = []
        home = Path.home()
        
        # Common project directories
        search_dirs = [
            home / "projects",
            home / "code",
            home / "dev",
            home / "work",
            home / "repos",
            home / "src",
            home / "Documents" / "projects",
            home / "Documents" / "code",
        ]
        
        # Also check current directory
        cwd = Path.cwd()
        if (cwd / ".git").exists():
            repos.append(cwd)
        
        for search_dir in search_dirs:
            if search_dir.exists():
                # Look for .git directories
                for item in search_dir.iterdir():
                    if item.is_dir() and (item / ".git").exists():
                        repos.append(item)
        
        return repos[:20]  # Limit to 20 repos to avoid too many watchers
    
    def start(self):
        """Start tracking git activity."""
        if self._running:
            return
        
        handler = GitEventHandler(self.callback)
        
        for repo in self.repos:
            git_dir = repo / ".git"
            if git_dir.exists():
                self.observer.schedule(handler, str(git_dir), recursive=True)
        
        self.observer.start()
        self._running = True
    
    def stop(self):
        """Stop tracking."""
        if self._running:
            self.observer.stop()
            self.observer.join()
            self._running = False
    
    @staticmethod
    def get_recent_commits(repo_path: Path, since_hours: int = 24) -> int:
        """Get the number of commits in the last N hours."""
        try:
            result = subprocess.run(
                ["git", "log", f"--since={since_hours} hours ago", "--oneline"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0
        except Exception:
            pass
        return 0
    
    @staticmethod
    def check_for_new_commits(repo_path: Path, last_check: float) -> bool:
        """Check if there are commits newer than last_check timestamp."""
        try:
            result = subprocess.run(
                ["git", "log", "-1", "--format=%ct"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0 and result.stdout.strip():
                commit_time = int(result.stdout.strip())
                return commit_time > last_check
        except Exception:
            pass
        return False


def poll_for_commits(pet, interval: int = 60):
    """Poll for new commits periodically (backup to file watching)."""
    from .pet import Pet
    
    tracker = GitTracker(lambda _: None)  # Dummy callback
    
    while True:
        for repo in tracker.repos:
            if GitTracker.check_for_new_commits(repo, pet.state.last_activity):
                pet.on_activity("commit")
                break
        time.sleep(interval)
