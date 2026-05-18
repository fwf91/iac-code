"""Tests for tree-sitter bash command parsing."""

from iac_code.tools.bash.command_parser import parse_command


class TestParseSimpleCommands:
    def test_single_command(self):
        r = parse_command("ls -la")
        assert r.kind == "simple"
        assert len(r.commands) == 1
        assert r.commands[0].argv[0] == "ls"

    def test_git_push(self):
        r = parse_command("git push origin main")
        assert r.kind == "simple"
        assert r.commands[0].argv == ["git", "push", "origin", "main"]

    def test_command_with_redirect(self):
        r = parse_command("echo hello > out.txt")
        assert r.kind == "simple"
        assert len(r.commands[0].redirects) >= 1


class TestParseCompoundCommands:
    def test_and_chain(self):
        r = parse_command("cd /tmp && ls")
        assert r.kind == "simple"
        assert len(r.commands) == 2

    def test_pipe(self):
        r = parse_command("ls | grep foo")
        assert r.kind == "simple"
        assert len(r.commands) == 2

    def test_semicolon(self):
        r = parse_command("echo a; echo b")
        assert r.kind == "simple"
        assert len(r.commands) == 2


class TestParseTooComplex:
    def test_command_substitution(self):
        r = parse_command("echo $(whoami)")
        assert r.kind == "too_complex"

    def test_backtick_substitution(self):
        r = parse_command("echo `whoami`")
        assert r.kind == "too_complex"

    def test_eval(self):
        r = parse_command("eval 'rm -rf /'")
        assert r.kind == "too_complex"

    def test_source(self):
        r = parse_command("source ~/.bashrc")
        assert r.kind == "too_complex"

    def test_exec(self):
        r = parse_command("exec /bin/bash")
        assert r.kind == "too_complex"


class TestParseEdgeCases:
    def test_empty_command(self):
        r = parse_command("")
        assert r.kind in ("parse_error", "simple")

    def test_env_var_prefix(self):
        r = parse_command("FOO=bar git push")
        assert r.kind == "simple"
        assert len(r.commands) >= 1
