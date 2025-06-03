# @track_context("change_detector.md")
"""
Change detection module for identifying significant file modifications.
"""

import ast
import re
import hashlib
import json
import subprocess
from typing import Dict, List, Optional, Tuple, Set
from pathlib import Path
import logging

from .utils import read_file_content

logger = logging.getLogger(__name__)


class FileSignature:
    """Represents the structural signature of a file."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.content = read_file_content(file_path) or ""
        self.line_count = len(self.content.split('\n'))
        self.functions = set()
        self.classes = set()
        self.imports = set()
        self.content_hash = hashlib.md5(self.content.encode()).hexdigest()

        if file_path.endswith('.py'):
            self._analyze_python_structure()
        elif file_path.endswith(('.js', '.ts', '.jsx', '.tsx')):
            self._analyze_javascript_structure()

    def _analyze_python_structure(self):
        """Analyze Python file structure."""
        try:
            tree = ast.parse(self.content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Include function signature
                    args = [arg.arg for arg in node.args.args]
                    self.functions.add(f"{node.name}({', '.join(args)})")
                elif isinstance(node, ast.ClassDef):
                    self.classes.add(node.name)
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            self.imports.add(alias.name)
                    else:
                        module = node.module or ""
                        for alias in node.names:
                            self.imports.add(f"{module}.{alias.name}")
        except SyntaxError:
            logger.warning(f"Could not parse Python file: {self.file_path}")

    def _analyze_javascript_structure(self):
        """Analyze JavaScript/TypeScript file structure (basic regex-based)."""
        # Function declarations
        func_pattern = r'(?:function\s+(\w+)|(\w+)\s*=\s*(?:function|\([^)]*\)\s*=>)|(?:async\s+)?(\w+)\s*\([^)]*\)\s*{)'
        for match in re.finditer(func_pattern, self.content):
            func_name = match.group(1) or match.group(2) or match.group(3)
            if func_name:
                self.functions.add(func_name)

        # Class declarations
        class_pattern = r'class\s+(\w+)'
        for match in re.finditer(class_pattern, self.content):
            self.classes.add(match.group(1))

        # Import statements
        import_pattern = r'import\s+(?:{[^}]+}|\w+|\*\s+as\s+\w+)\s+from\s+[\'"]([^\'"]+)[\'"]'
        for match in re.finditer(import_pattern, self.content):
            self.imports.add(match.group(1))

    def to_dict(self) -> Dict:
        """Convert signature to dictionary for storage."""
        return {
            'file_path': self.file_path,
            'line_count': self.line_count,
            'functions': list(self.functions),
            'classes': list(self.classes),
            'imports': list(self.imports),
            'content_hash': self.content_hash,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'FileSignature':
        """Create signature from dictionary."""
        sig = cls.__new__(cls)
        sig.file_path = data['file_path']
        sig.line_count = data['line_count']
        sig.functions = set(data['functions'])
        sig.classes = set(data['classes'])
        sig.imports = set(data['imports'])
        sig.content_hash = data['content_hash']
        return sig


class ChangeAnalysis:
    """Represents the analysis of changes between two file signatures."""

    def __init__(self, old_sig: Optional[FileSignature], new_sig: FileSignature):
        self.old_sig = old_sig
        self.new_sig = new_sig
        self.file_path = new_sig.file_path

        if old_sig is None:
            # New file
            self.is_new_file = True
            self.is_significant = True
            self.changes = ["New tracked file"]
        else:
            self.is_new_file = False
            self.is_significant = self._analyze_significance()
            self.changes = self._describe_changes()

    def _analyze_significance(self) -> bool:
        """Determine if changes are significant enough to require doc update."""
        if not self.old_sig:
            return True

        # Check for structural changes
        if (self.old_sig.functions != self.new_sig.functions or
            self.old_sig.classes != self.new_sig.classes or
            self.old_sig.imports != self.new_sig.imports):
            return True

        # Check for significant line count changes (>20%)
        if self.old_sig.line_count > 0:
            change_ratio = abs(self.new_sig.line_count - self.old_sig.line_count) / self.old_sig.line_count
            if change_ratio > 0.2:  # 20% change threshold
                return True

        # Check content hash for ANY changes - stricter detection
        if self.old_sig.content_hash != self.new_sig.content_hash:
            # Flag ALL changes as potentially significant
            # Developers can mark as reviewed if not actually critical
            return True

        return False

    def _describe_changes(self) -> List[str]:
        """Describe what changed between signatures."""
        if not self.old_sig:
            return ["New file"]

        changes = []

        # Function changes
        added_funcs = self.new_sig.functions - self.old_sig.functions
        removed_funcs = self.old_sig.functions - self.new_sig.functions

        if added_funcs:
            changes.append(f"Added functions: {', '.join(added_funcs)}")
        if removed_funcs:
            changes.append(f"Removed functions: {', '.join(removed_funcs)}")

        # Class changes
        added_classes = self.new_sig.classes - self.old_sig.classes
        removed_classes = self.old_sig.classes - self.new_sig.classes

        if added_classes:
            changes.append(f"Added classes: {', '.join(added_classes)}")
        if removed_classes:
            changes.append(f"Removed classes: {', '.join(removed_classes)}")

        # Import changes
        added_imports = self.new_sig.imports - self.old_sig.imports
        removed_imports = self.old_sig.imports - self.new_sig.imports

        if added_imports:
            changes.append(f"Added imports: {', '.join(added_imports)}")
        if removed_imports:
            changes.append(f"Removed imports: {', '.join(removed_imports)}")

        # Line count changes
        line_diff = self.new_sig.line_count - self.old_sig.line_count
        if abs(line_diff) > 10:  # Only report significant line changes
            if line_diff > 0:
                changes.append(f"Added {line_diff} lines")
            else:
                changes.append(f"Removed {abs(line_diff)} lines")

        if not changes and self.old_sig.content_hash != self.new_sig.content_hash:
            changes.append("Content modified")

        return changes or ["File modified"]


class ChangeDetector:
    """Detects significant changes in tracked files."""

    def __init__(self, cache_file: str = "lore_cache.json"):
        self.cache_file = Path(cache_file)
        self.cached_signatures = self._load_cache()

    def _load_cache(self) -> Dict[str, FileSignature]:
        """Load cached file signatures."""
        if not self.cache_file.exists():
            return {}

        try:
            with open(self.cache_file, 'r') as f:
                data = json.load(f)
            return {
                path: FileSignature.from_dict(sig_data)
                for path, sig_data in data.items()
            }
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Could not load cache file: {e}")
            return {}

    def _save_cache(self):
        """Save cached file signatures."""
        try:
            data = {
                path: sig.to_dict()
                for path, sig in self.cached_signatures.items()
            }
            with open(self.cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save cache file: {e}")

    def analyze_changes(self, file_paths: List[str]) -> List[ChangeAnalysis]:
        """Analyze changes for a list of files."""
        analyses = []

        for file_path in file_paths:
            if not Path(file_path).exists():
                continue

            # Get current signature
            current_sig = FileSignature(file_path)

            # Get cached signature
            cached_sig = self.cached_signatures.get(file_path)

            # Analyze changes
            analysis = ChangeAnalysis(cached_sig, current_sig)
            analyses.append(analysis)

            # Update cache with current signature
            self.cached_signatures[file_path] = current_sig

        return analyses

    def mark_as_reviewed(self, file_paths: List[str]):
        """Mark files as reviewed, updating their cached signatures."""
        for file_path in file_paths:
            if Path(file_path).exists():
                current_sig = FileSignature(file_path)
                self.cached_signatures[file_path] = current_sig

        self._save_cache()

    def get_significant_changes(self, file_paths: List[str]) -> List[ChangeAnalysis]:
        """Get only the significant changes that require documentation updates."""
        all_changes = self.analyze_changes(file_paths)
        return [change for change in all_changes if change.is_significant]

    def save_current_state(self, file_paths: List[str]):
        """Save current state of files to cache."""
        for file_path in file_paths:
            if Path(file_path).exists():
                self.cached_signatures[file_path] = FileSignature(file_path)
        self._save_cache()
