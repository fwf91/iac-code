from iac_code.tools.bash.rule_matching import (
    extract_prefix,
    find_matching_rules,
    match_rule,
    match_wildcard,
    normalize_command,
)


class TestExtractPrefix:
    def test_prefix_rule(self):
        assert extract_prefix("git:*") == "git"

    def test_non_prefix_rule(self):
        assert extract_prefix("git push") is None

    def test_wildcard_not_prefix(self):
        assert extract_prefix("npm * --registry=*") is None


class TestMatchWildcard:
    def test_simple_wildcard(self):
        assert match_wildcard("git *", "git push") is True

    def test_no_match(self):
        assert match_wildcard("git *", "npm install") is False

    def test_multiple_wildcards(self):
        assert match_wildcard("npm * --registry=*", "npm install --registry=https://r.com") is True

    def test_exact_via_wildcard(self):
        assert match_wildcard("ls", "ls") is True
        assert match_wildcard("ls", "ls -la") is False


class TestMatchRule:
    def test_exact_match(self):
        assert match_rule("ls -la", "ls -la") is True
        assert match_rule("ls -la", "ls -la /tmp") is False

    def test_prefix_match(self):
        assert match_rule("git:*", "git") is True
        assert match_rule("git:*", "git push") is True
        assert match_rule("git:*", "git push origin main") is True
        assert match_rule("git:*", "gitk") is False

    def test_multiword_prefix_match(self):
        assert match_rule("git push:*", "git push") is True
        assert match_rule("git push:*", "git push origin main") is True
        assert match_rule("git push:*", "git") is False
        assert match_rule("git push:*", "git fetch") is False

    def test_wildcard_match(self):
        assert match_rule("git *", "git push") is True
        assert match_rule("git *", "git") is False

    def test_empty_rule(self):
        assert match_rule("", "anything") is False


class TestNormalizeCommand:
    def test_strip_env_vars(self):
        assert normalize_command("FOO=bar git push") == "git push"

    def test_multiple_env_vars(self):
        assert normalize_command("A=1 B=2 npm test") == "npm test"

    def test_no_env_vars(self):
        assert normalize_command("git push") == "git push"

    def test_strip_whitespace(self):
        assert normalize_command("  git push  ") == "git push"

    def test_env_var_only(self):
        assert normalize_command("FOO=bar") == "FOO=bar"


class TestFindMatchingRules:
    def test_finds_deny(self):
        result = find_matching_rules(
            "rm -rf /",
            allow_rules=["bash(git *)"],
            deny_rules=["bash(rm -rf /)"],
            ask_rules=[],
        )
        assert "bash(rm -rf /)" in result["deny"]

    def test_finds_allow(self):
        result = find_matching_rules("git push", allow_rules=["bash(git:*)"], deny_rules=[], ask_rules=[])
        assert "bash(git:*)" in result["allow"]

    def test_no_matches(self):
        result = find_matching_rules(
            "docker run",
            allow_rules=["bash(git *)"],
            deny_rules=["bash(rm -rf /)"],
            ask_rules=[],
        )
        assert result == {"allow": [], "deny": [], "ask": []}
