import pytest

from iac_code.services.permissions.pipeline import check_tool_permission
from iac_code.tools.base import Tool, ToolResult
from iac_code.types.permissions import PermissionMode, ToolPermissionContext


class FakeReadTool(Tool):
    @property
    def name(self):
        return "read_file"

    @property
    def description(self):
        return "Read a file"

    @property
    def input_schema(self):
        return {"type": "object", "properties": {}}

    async def execute(self, *, tool_input, context):
        return ToolResult.success("ok")

    def is_read_only(self, input=None):
        return True


class FakeWriteTool(Tool):
    @property
    def name(self):
        return "write_file"

    @property
    def description(self):
        return "Write a file"

    @property
    def input_schema(self):
        return {"type": "object", "properties": {}}

    async def execute(self, *, tool_input, context):
        return ToolResult.success("ok")


def _ctx(mode=PermissionMode.DEFAULT, deny=None, allow=None):
    return ToolPermissionContext(
        mode=mode,
        cwd="/tmp",
        allow_rules=allow or {},
        deny_rules=deny or {},
        ask_rules={},
    )


class TestPipeline:
    @pytest.mark.asyncio
    async def test_readonly_tool_auto_allowed(self):
        r = await check_tool_permission(FakeReadTool(), {}, _ctx())
        assert r.behavior == "allow"

    @pytest.mark.asyncio
    async def test_tool_level_deny(self):
        ctx = _ctx(deny={"user_settings": ["write_file"]})
        r = await check_tool_permission(FakeWriteTool(), {}, ctx)
        assert r.behavior == "deny"

    @pytest.mark.asyncio
    async def test_tool_level_allow(self):
        ctx = _ctx(allow={"user_settings": ["write_file"]})
        r = await check_tool_permission(FakeWriteTool(), {}, ctx)
        assert r.behavior == "allow"

    @pytest.mark.asyncio
    async def test_bypass_mode_allows(self):
        ctx = _ctx(mode=PermissionMode.BYPASS_PERMISSIONS)
        r = await check_tool_permission(FakeWriteTool(), {}, ctx)
        assert r.behavior == "allow"

    @pytest.mark.asyncio
    async def test_dont_ask_converts_to_deny(self):
        ctx = _ctx(mode=PermissionMode.DONT_ASK)
        r = await check_tool_permission(FakeWriteTool(), {}, ctx)
        assert r.behavior == "deny"

    @pytest.mark.asyncio
    async def test_default_mode_asks(self):
        ctx = _ctx(mode=PermissionMode.DEFAULT)
        r = await check_tool_permission(FakeWriteTool(), {}, ctx)
        assert r.behavior == "ask"
