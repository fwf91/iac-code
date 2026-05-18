"""Tests for bash safety checks."""

from __future__ import annotations

from iac_code.tools.bash.command_parser import SimpleCommand
from iac_code.tools.bash.safety_checks import check_command_safety, check_safety


class TestCheckSafety:
    def test_write_to_git_dir(self):
        cmd = SimpleCommand(text="rm -rf .git/hooks", argv=["rm", "-rf", ".git/hooks"])
        r = check_safety(cmd, "/project")
        assert r.behavior == "ask"
        assert r.reason is not None and r.reason.type == "safety_check"

    def test_normal_command(self):
        cmd = SimpleCommand(text="ls -la", argv=["ls", "-la"])
        r = check_safety(cmd, "/project")
        assert r.behavior == "passthrough"


class TestCheckCommandSafety:
    def test_null_bytes(self):
        assert check_command_safety("echo hello\x00world") is False

    def test_control_chars(self):
        assert check_command_safety("echo \x07bell") is False

    def test_normal_command(self):
        assert check_command_safety("git status") is True

    def test_unmatched_quotes(self):
        assert check_command_safety("echo 'hello") is False
