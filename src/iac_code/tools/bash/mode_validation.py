"""Permission mode helpers for filesystem-oriented bash commands."""

from __future__ import annotations

from typing import TYPE_CHECKING

from iac_code.types.permissions import PermissionMode, PermissionResult

if TYPE_CHECKING:
    from iac_code.tools.bash.command_parser import SimpleCommand

_FILESYSTEM_COMMANDS = frozenset({"mkdir", "touch", "rm", "rmdir", "mv", "cp", "sed"})


def is_filesystem_command(base_cmd: str) -> bool:
    """Check if command is a filesystem command."""
    return base_cmd in _FILESYSTEM_COMMANDS


def check_permission_mode(cmd: SimpleCommand, mode: PermissionMode) -> PermissionResult:
    """accept_edits + filesystem → allow, otherwise → passthrough"""
    if mode is not PermissionMode.ACCEPT_EDITS:
        return PermissionResult(behavior="passthrough")
    base = cmd.argv[0] if cmd.argv else ""
    if is_filesystem_command(base):
        return PermissionResult(behavior="allow")
    return PermissionResult(behavior="passthrough")
