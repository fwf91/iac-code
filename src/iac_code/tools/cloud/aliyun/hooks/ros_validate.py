"""Pre-call hook: validate ROS template resource types before ValidateTemplate API call."""

from __future__ import annotations

import json
from typing import Any

import yaml

from iac_code.tools.base import ToolResult
from iac_code.tools.cloud.aliyun.api_hooks import before_call

_RESOURCE_TYPE_CORRECTIONS: dict[str, str] = {
    "ALIYUN::VPC::VPC": "ALIYUN::ECS::VPC",
    "ALIYUN::VPC::VSwitch": "ALIYUN::ECS::VSwitch",
}


def _parse_template(template_body: str) -> dict | None:
    try:
        data = yaml.safe_load(template_body)
    except Exception:
        try:
            data = json.loads(template_body)
        except Exception:
            return None
    return data if isinstance(data, dict) else None


def _find_wrong_resource_types(template_data: dict) -> dict[str, str]:
    """Return {wrong_type: correct_type} for all incorrect resource types found."""
    resources = template_data.get("Resources", {})
    if not isinstance(resources, dict):
        return {}
    found: dict[str, str] = {}
    for resource in resources.values():
        if not isinstance(resource, dict):
            continue
        rtype = resource.get("Type", "")
        if rtype in _RESOURCE_TYPE_CORRECTIONS:
            found[rtype] = _RESOURCE_TYPE_CORRECTIONS[rtype]
    return found


@before_call("ros", "ValidateTemplate")
def check_resource_types(product: str, action: str, params: dict[str, Any]) -> ToolResult | None:
    template_body = params.get("TemplateBody", "")
    if not template_body:
        return None
    template_data = _parse_template(template_body)
    if template_data is None:
        return None
    wrong_types = _find_wrong_resource_types(template_data)
    if not wrong_types:
        return None
    corrections = "\n".join(f"  {wrong} -> {correct}" for wrong, correct in wrong_types.items())
    return ToolResult.error(f"Template contains incorrect resource types. Please fix before validation:\n{corrections}")
