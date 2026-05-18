"""Session-scoped permission rule storage."""

from __future__ import annotations

import copy

from iac_code.types.permissions import PermissionRuleValue, ToolPermissionContext

_SESSION_KEY = "session"


def _format_rule(rule_value: PermissionRuleValue) -> str:
    if rule_value.rule_content:
        return "{}({})".format(rule_value.tool_name, rule_value.rule_content)
    return rule_value.tool_name


def apply_session_rule(
    context: ToolPermissionContext,
    behavior: str,
    rule_value: PermissionRuleValue,
) -> ToolPermissionContext:
    """Add a session-scoped rule. Returns a NEW context (does not mutate original).

    Rule string format: "{tool_name}({rule_content})" if rule_content else tool_name
    Added to context.allow_rules["session"], deny_rules["session"], or ask_rules["session"]
    """
    new_ctx = copy.deepcopy(context)
    rule_str = _format_rule(rule_value)
    if behavior == "allow":
        bucket = new_ctx.allow_rules.setdefault(_SESSION_KEY, [])
    elif behavior == "deny":
        bucket = new_ctx.deny_rules.setdefault(_SESSION_KEY, [])
    elif behavior == "ask":
        bucket = new_ctx.ask_rules.setdefault(_SESSION_KEY, [])
    else:
        msg = "behavior must be 'allow', 'deny', or 'ask', got {!r}".format(behavior)
        raise ValueError(msg)
    bucket.append(rule_str)
    return new_ctx
