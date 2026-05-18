import pytest

from iac_code.tools.bash.command_parser import SimpleCommand
from iac_code.tools.bash.readonly_commands import is_command_readonly


class TestReadonlyBasicCommands:
    @pytest.mark.parametrize("cmd", ["ls", "ls -la", "cat foo.txt", "head -n5 file", "tail file", "wc -l file"])
    def test_filesystem_view_commands(self, cmd):
        assert is_command_readonly(SimpleCommand(text=cmd, argv=cmd.split(), redirects=[])) is True

    @pytest.mark.parametrize("cmd", ["grep pattern file", "rg foo", "find . -name '*.py'", "which python"])
    def test_search_commands(self, cmd):
        assert is_command_readonly(SimpleCommand(text=cmd, argv=cmd.split(), redirects=[])) is True

    @pytest.mark.parametrize("cmd", ["pwd", "env", "whoami", "hostname", "uname -a", "date"])
    def test_system_info_commands(self, cmd):
        assert is_command_readonly(SimpleCommand(text=cmd, argv=cmd.split(), redirects=[])) is True

    @pytest.mark.parametrize("cmd", ["echo hello", "printf '%s' foo"])
    def test_output_commands(self, cmd):
        assert is_command_readonly(SimpleCommand(text=cmd, argv=cmd.split(), redirects=[])) is True


class TestReadonlyGitCommands:
    @pytest.mark.parametrize(
        "cmd",
        [
            "git status",
            "git log",
            "git diff",
            "git show HEAD",
            "git branch",
            "git tag",
            "git blame file.py",
        ],
    )
    def test_git_readonly(self, cmd):
        assert is_command_readonly(SimpleCommand(text=cmd, argv=cmd.split(), redirects=[])) is True

    @pytest.mark.parametrize(
        "cmd",
        [
            "git push",
            "git commit -m 'msg'",
            "git checkout main",
            "git merge dev",
            "git rebase main",
        ],
    )
    def test_git_write_not_readonly(self, cmd):
        assert is_command_readonly(SimpleCommand(text=cmd, argv=cmd.split(), redirects=[])) is False


class TestReadonlyVersionCommands:
    @pytest.mark.parametrize("cmd", ["python --version", "node --version", "cargo --version"])
    def test_version_flags(self, cmd):
        assert is_command_readonly(SimpleCommand(text=cmd, argv=cmd.split(), redirects=[])) is True


class TestNotReadonly:
    @pytest.mark.parametrize(
        "cmd",
        [
            "rm -rf /",
            "mv a b",
            "cp a b",
            "mkdir dir",
            "python script.py",
            "node app.js",
            "curl https://example.com",
            "wget file",
            "npm install",
            "pip install pkg",
            "docker run img",
            "ssh host",
            "chmod 755 file",
            "sed -i 's/a/b/' file",
        ],
    )
    def test_write_and_dangerous_commands(self, cmd):
        assert is_command_readonly(SimpleCommand(text=cmd, argv=cmd.split(), redirects=[])) is False


class TestRedirectDisqualifies:
    def test_echo_with_redirect(self):
        cmd = SimpleCommand(text="echo hello > out.txt", argv=["echo", "hello"], redirects=["> out.txt"])
        assert is_command_readonly(cmd) is False

    def test_cat_without_redirect(self):
        cmd = SimpleCommand(text="cat file.txt", argv=["cat", "file.txt"], redirects=[])
        assert is_command_readonly(cmd) is True
