"""Tests for bash path constraint validation."""

from __future__ import annotations

from iac_code.tools.bash.command_parser import SimpleCommand
from iac_code.tools.bash.path_validation import check_path_constraints, validate_path


class TestValidatePath:
    def test_path_within_cwd(self, tmp_path):
        target = str(tmp_path / "sub" / "file.txt")
        assert validate_path(target, str(tmp_path), []) == "allow"

    def test_path_outside_cwd(self, tmp_path):
        assert validate_path("/etc/passwd", str(tmp_path), []) == "deny"

    def test_path_in_additional_dir(self, tmp_path):
        assert validate_path("/shared/libs/foo.py", str(tmp_path), ["/shared/libs"]) == "allow"


class TestCheckPathConstraints:
    def test_no_paths_passthrough(self, tmp_path):
        cmd = SimpleCommand(text="echo hello", argv=["echo", "hello"], redirects=[])
        r = check_path_constraints(cmd, str(tmp_path), [])
        assert r.behavior == "passthrough"

    def test_rm_outside_cwd(self, tmp_path):
        cmd = SimpleCommand(text="rm /etc/passwd", argv=["rm", "/etc/passwd"], redirects=[])
        r = check_path_constraints(cmd, str(tmp_path), [])
        assert r.behavior in ("ask", "deny")
