"""Shell command rule matching for bash permission checks."""

from __future__ import annotations

import re

_ENV_ASSIGNMENT_PREFIX = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=\S+\s+")


def extract_prefix(rule_content: str) -> str | None:
    """Return the prefix from a `prefix:*` rule, or None if not in prefix form."""
    if rule_content.endswith(":*"):
        return rule_content[:-2]
    return None


def match_wildcard(pattern: str, command: str) -> bool:
    """Match command against pattern where each `*` spans `.*` in regex."""
    parts = pattern.split("*")
    regex_body = ".*".join(re.escape(part) for part in parts)
    return re.fullmatch(regex_body, command) is not None


def match_rule(rule_content: str, command: str) -> bool:
    """Try prefix (`:*`), then wildcard (`*`), then exact match."""
    if rule_content == "":
        return False

    cmd = command.strip()

    prefix = extract_prefix(rule_content)
    if prefix is not None:
        if cmd == prefix:
            return True
        return cmd.startswith(prefix + " ")

    if "*" in rule_content:
        return match_wildcard(rule_content, cmd)

    return cmd == rule_content


def normalize_command(command: str) -> str:
    """Strip leading env assignments; trim whitespace.

    If stripping consumes everything (only env assignments), return the original trimmed string.
    """
    s = command.strip()
    rest = s
    while True:
        m = _ENV_ASSIGNMENT_PREFIX.match(rest)
        if not m:
            break
        rest = rest[m.end() :]

    rest_stripped = rest.strip()
    if rest_stripped:
        return rest_stripped
    return s


def _parse_rule_string(rule_string: str) -> tuple[str, str]:
    m = re.fullmatch(r"(\w+)\((.*)\)", rule_string.strip())
    if not m:
        msg = "invalid rule string: {}".format(rule_string)
        raise ValueError(msg)
    return m.group(1), m.group(2)


def find_matching_rules(
    command: str,
    allow_rules: list[str],
    deny_rules: list[str],
    ask_rules: list[str],
) -> dict[str, list[str]]:
    """Collect rules that match ``command`` per allow/deny/ask policy.

    Allow rules use the raw ``command``; deny and ask rules use ``normalize_command``.
    """
    normalized = normalize_command(command)
    out: dict[str, list[str]] = {"allow": [], "deny": [], "ask": []}

    for rule in allow_rules:
        try:
            shell, content = _parse_rule_string(rule)
        except ValueError:
            continue
        if shell != "bash":
            continue
        if match_rule(content, command):
            out["allow"].append(rule)

    for rule in deny_rules:
        try:
            shell, content = _parse_rule_string(rule)
        except ValueError:
            continue
        if shell != "bash":
            continue
        if match_rule(content, normalized):
            out["deny"].append(rule)

    for rule in ask_rules:
        try:
            shell, content = _parse_rule_string(rule)
        except ValueError:
            continue
        if shell != "bash":
            continue
        if match_rule(content, normalized):
            out["ask"].append(rule)

    return out
