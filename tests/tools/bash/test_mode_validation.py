"""Tests for permission mode validation against filesystem commands."""

from __future__ import annotations

import pytest

from iac_code.tools.bash.command_parser import SimpleCommand
from iac_code.tools.bash.mode_validation import check_permission_mode, is_filesystem_command
from iac_code.types.permissions import PermissionMode


class TestIsFilesystemCommand:
    @pytest.mark.parametrize("cmd", ["mkdir", "touch", "rm", "rmdir", "mv", "cp", "sed"])
    def test_filesystem_commands(self, cmd):
        assert is_filesystem_command(cmd) is True

    @pytest.mark.parametrize("cmd", ["git", "echo", "curl", "python"])
    def test_non_filesystem_commands(self, cmd):
        assert is_filesystem_command(cmd) is False


class TestCheckPermissionMode:
    def test_accept_edits_filesystem_cmd(self):
        cmd = SimpleCommand(text="mkdir foo", argv=["mkdir", "foo"])
        r = check_permission_mode(cmd, PermissionMode.ACCEPT_EDITS)
        assert r.behavior == "allow"

    def test_accept_edits_non_filesystem_cmd(self):
        cmd = SimpleCommand(text="curl url", argv=["curl", "url"])
        r = check_permission_mode(cmd, PermissionMode.ACCEPT_EDITS)
        assert r.behavior == "passthrough"

    def test_default_mode_passthrough(self):
        cmd = SimpleCommand(text="mkdir foo", argv=["mkdir", "foo"])
        r = check_permission_mode(cmd, PermissionMode.DEFAULT)
        assert r.behavior == "passthrough"
