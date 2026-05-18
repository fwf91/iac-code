"""Tests for session permission storage."""

from __future__ import annotations

from iac_code.services.permissions.storage import apply_session_rule
from iac_code.types.permissions import PermissionMode, PermissionRuleValue, ToolPermissionContext


class TestApplySessionRule:
    def test_add_allow_rule(self):
        ctx = ToolPermissionContext(mode=PermissionMode.DEFAULT, cwd="/tmp")
        new_ctx = apply_session_rule(ctx, "allow", PermissionRuleValue(tool_name="bash", rule_content="git:*"))
        assert "bash(git:*)" in new_ctx.allow_rules.get("session", [])
        assert ctx.allow_rules.get("session") is None

    def test_add_deny_rule(self):
        ctx = ToolPermissionContext(mode=PermissionMode.DEFAULT, cwd="/tmp")
        new_ctx = apply_session_rule(ctx, "deny", PermissionRuleValue(tool_name="bash", rule_content="rm:*"))
        assert "bash(rm:*)" in new_ctx.deny_rules.get("session", [])
