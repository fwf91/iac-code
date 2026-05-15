# 设计文档：QwenPaw 模式 + Provider 体系全面对齐

## 概述

本设计覆盖两个紧密关联的目标：

1. **QwenPaw 模式（零配置 LLM 接入）**：iac-code 作为 QwenPaw 的 CloudPaw 插件运行时，直接读取 QwenPaw 的 LLM 配置，用户无需重复配置。
2. **Provider 体系全面对齐**：将 iac-code 的 provider 体系从 6 种扩展到 18+ 种，与 QwenPaw 完全对齐，同时更新所有模型列表至最新主流模型。

工作分两个阶段实施：
- **Phase 1**：Provider Registry 重构 + QwenPaw 模式 + 现有 provider 升级
- **Phase 2**：新 provider 扩展 + Gemini 支持 + Anthropic 主动缓存

---

## Phase 1：QwenPaw 模式 + Registry 重构 + 现有 Provider 升级

### 1. Provider Registry 架构

#### 1.1 核心数据结构

引入 `providers/registry.py`，定义声明式 provider 注册表：

```python
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ModelEntry:
    id: str
    is_default: bool = False


@dataclass(frozen=True)
class ProviderDescriptor:
    key: str                        # provider_key，如 "dashscope", "kimi_cn"
    name: str                       # 英文名，如 "Kimi CN"
    display_name: str               # 中文显示名，如 "Kimi 中国版"
    provider_class: str             # 延迟导入路径
    base_url: str | None            # 默认 API 基地址
    models: list[ModelEntry] = field(default_factory=list)
    require_api_key: bool = True
    is_local: bool = False
    qwenpaw_provider_ids: list[str] = field(default_factory=list)
    qwenpaw_chat_model: str = "OpenAIChatModel"

    @property
    def default_model(self) -> str:
        for m in self.models:
            if m.is_default:
                return m.id
        return self.models[0].id if self.models else ""

    @property
    def model_ids(self) -> list[str]:
        return [m.id for m in self.models]
```

**从 ProviderDescriptor 中移除的字段及原因：**

- **`cache_strategy`**：缓存决策是**模型级别**而非 provider 级别。同一个 DashScope provider 下，`qwen3.6-plus` 支持显式 cache_control 标记，但 `deepseek-v4-pro` 不支持。缓存逻辑保留在 provider class 内部（如 `DashScopeProvider._supports_explicit_cache()` 按模型前缀判断）。
- **`supports_stream_options`**：这是 provider class 的运行时行为属性（如 `DashScopeProvider.supports_stream_options = True`），不应在描述符中重复声明。保留为 class attribute。

全局注册表 `PROVIDER_REGISTRY: dict[str, ProviderDescriptor]` 在模块加载时由各 provider 的声明构建。

#### 1.2 Provider 构造函数统一

**现状问题**：各 provider 构造函数签名不一致：

| Provider | 参数 | 问题 |
|---|---|---|
| `OpenAIProvider` | `(model, api_key, base_url, client, effort)` | 无 `provider_key` |
| `DashScopeProvider` | `(model, api_key, effort, base_url, provider_key)` | 有 `provider_key` |
| `DeepSeekProvider` | `(model, api_key, effort)` | 无 `base_url`，硬编码 URL |
| `AnthropicProvider` | `(model, api_key, base_url, max_tokens, client, effort)` | 无 `provider_key` |

**解决方案**：统一所有 provider 构造函数接受 `(model, api_key, base_url, effort, provider_key, **kwargs)`。

具体修改：
- `OpenAIProvider.__init__`：新增 `provider_key` 参数（默认 `"openai"`），赋值给 `self._PROVIDER_KEY`
- `DeepSeekProvider.__init__`：新增 `base_url` 参数（默认 `DEEPSEEK_BASE_URL`），不再硬编码。`provider_key` 默认 `"deepseek"`
- `AnthropicProvider.__init__`：新增 `provider_key` 参数（默认 `"anthropic"`），赋值给 `self._PROVIDER_KEY`
- `DashScopeProvider.__init__`：已支持，无需修改
- 所有新 provider 子类：接受 `base_url` 和 `provider_key`，**不硬编码** base_url（由 registry 提供默认值）

这样 `create_provider` 可以统一传参：

```python
def create_provider(
    model: str,
    credentials: dict[str, str],
    base_url: str | None = None,
    provider_key_override: str | None = None,
) -> Provider:
    provider_key = provider_key_override or _detect_provider_name(model)
    descriptor = PROVIDER_REGISTRY.get(provider_key)
    if descriptor is None:
        raise ValueError(f"Unknown provider: {provider_key}")

    api_key = credentials.get(provider_key, "")
    if descriptor.require_api_key and not api_key:
        raise ProviderNotConfiguredError(...)

    cls = _import_provider_class(descriptor.provider_class)
    effective_url = base_url or descriptor.base_url
    effort = get_provider_config(provider_key).get("effort")

    return cls(
        model=model,
        api_key=api_key if api_key else None,
        base_url=effective_url,
        effort=effort if isinstance(effort, str) else None,
        provider_key=provider_key,
    )
```

新增 `provider_key_override` 参数供 QwenPaw 模式使用（已知 provider_key，无需推断）。
新增 `base_url` 参数供 QwenPaw 模式注入 base_url。

**新 thin subclass 模式**（以 KimiProvider 为例）：

```python
class KimiProvider(OpenAIProvider):
    """Kimi (Moonshot AI) — OpenAI-compatible endpoint."""

    _PROVIDER_KEY = "kimi_cn"  # 默认值，会被 provider_key 参数覆盖

    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        base_url: str | None = None,  # 不硬编码！由 registry 提供
        effort: str | None = None,
        provider_key: str = "kimi_cn",
        **kwargs,
    ) -> None:
        super().__init__(model=model, api_key=api_key, base_url=base_url, effort=effort)
        self._PROVIDER_KEY = provider_key
```

与 DeepSeekProvider 的区别：**不硬编码 base_url**。同一个 KimiProvider class 可以服务 kimi_cn（moonshot.cn）和 kimi_intl（moonshot.ai），通过 registry 中不同的 descriptor 提供不同的 base_url。

#### 1.3 config.py 简化

以下映射表从 `PROVIDER_REGISTRY` 自动派生或直接引用 registry，消除重复声明：

- `_KEY_NAME_TO_CRED_SLOT`：从 registry keys 生成（`{key: key for key in PROVIDER_REGISTRY}`）
- `_PROVIDER_NAME_TO_KEY`：从 registry 的 name 生成
- `_PROVIDER_CANONICAL_NAMES`：从 registry 的 name 生成

**`_MODEL_PREFIX_TO_PROVIDER`** 保持为手写元组（无法从 model 列表自动推导，因为同一前缀可能对应多个 provider，且有 CN/Intl 的歧义需要人工指定默认值）。Phase 2 完成后的完整列表：

```python
_MODEL_PREFIX_TO_PROVIDER = (
    ("claude-", "anthropic"),
    ("gpt-", "openai"),
    ("o1-", "openai"),
    ("o3", "openai"),
    ("o4-", "openai"),
    ("qwen", "dashscope"),
    ("deepseek-", "deepseek"),
    ("gemini-", "gemini"),
    ("kimi-", "kimi_cn"),       # 默认中国版；国际版需通过 /auth 显式选择
    ("glm-", "zhipu_cn"),       # 默认中国版
    ("minimax", "minimax_cn"),   # 默认中国版
    ("doubao-", "volcengine_cn"),
)
```

注意：模型前缀匹配仅作为 fallback（当用户未通过 /auth 设置 activeProvider 时）。正常流程中 `_detect_provider_name` 优先使用 settings.yml 中的 `activeProvider`。

#### 1.4 auth.py PROVIDERS 列表

`PROVIDERS` 列表从 `PROVIDER_REGISTRY` 派生：

```python
def _build_auth_providers() -> list[LLMProvider]:
    result = []
    for desc in PROVIDER_REGISTRY.values():
        result.append({
            "name": desc.name,
            "display_name": desc.display_name,
            "key_name": desc.key,
            "api_base": desc.base_url,
            "models": desc.model_ids,
            "default_model": desc.default_model,
        })
    return result
```

**20+ provider 的 /auth UI 处理**：provider 列表按类别分组显示，便于用户选择：

| 分组 | Provider |
|------|----------|
| 阿里云 | DashScope, Token Plan, CodingPlan, CodingPlan Intl |
| 国际主流 | OpenAI, Anthropic, DeepSeek, Gemini |
| 中国厂商 | Kimi CN, ZhiPu CN, MiniMax CN, Volcengine, SiliconFlow CN |
| 国际厂商 | Kimi Intl, ZhiPu Intl, MiniMax Intl, SiliconFlow Intl |
| 聚合平台 | OpenRouter, Azure OpenAI, ModelScope |
| 本地部署 | Ollama, LM Studio |
| 自定义 | OpenAPI Compatible |

---

### 2. QwenPaw 模式（零配置 LLM 接入）

基于 `docs/design-qwenpaw-credential-source.md` 实现，以下是要点：

#### 2.1 llm_source 配置

```yaml
# ~/.iac-code/settings.yml
llm_source: qwenpaw  # 或缺省/local
```

| 字段 | 类型 | 默认值 | 可选值 | 说明 |
|------|------|--------|--------|------|
| `llm_source` | string | 缺省等同 `"local"` | `"local"`, `"qwenpaw"` | LLM 配置来源 |

#### 2.2 QwenPaw 文件结构

```
SECRET_DIR (默认 ~/.qwenpaw.secret)
├── providers/
│   ├── active_model.json        ← {"provider_id": "...", "model": "..."}
│   ├── builtin/
│   │   ├── dashscope.json       ← api_key 带 ENC: 前缀
│   │   ├── openai.json
│   │   ├── anthropic.json
│   │   └── ...
│   ├── custom/
│   └── plugin/
└── .master_key                  ← Fernet key (64 hex chars)
```

SECRET_DIR 定位优先级：
1. `QWENPAW_SECRET_DIR` 环境变量（`COPAW_SECRET_DIR` 回退）
2. `{WORKING_DIR}.secret`，WORKING_DIR 取自 `QWENPAW_WORKING_DIR`（`COPAW_WORKING_DIR` 回退）→ `~/.copaw`（旧版兼容）→ `~/.qwenpaw`

#### 2.3 Provider 映射

通过 `PROVIDER_REGISTRY` 中的 `qwenpaw_provider_ids` 字段自动构建映射表：

```python
def _build_qwenpaw_mapping() -> dict[str, str]:
    """从 registry 构建 QwenPaw provider_id → iac-code provider_key 映射。"""
    mapping = {}
    for key, desc in PROVIDER_REGISTRY.items():
        for qp_id in desc.qwenpaw_provider_ids:
            mapping[qp_id] = key
    return mapping
```

完整映射关系：

| QwenPaw provider_id | chat_model | iac-code provider_key |
|---|---|---|
| `dashscope` | OpenAIChatModel | `dashscope` |
| `aliyun-tokenplan` | OpenAIChatModel | `dashscope_token_plan` |
| `aliyun-codingplan` | OpenAIChatModel | `aliyun_codingplan` |
| `aliyun-codingplan-intl` | OpenAIChatModel | `aliyun_codingplan_intl` |
| `openai` | OpenAIChatModel | `openai` |
| `azure-openai` | OpenAIChatModel | `azure_openai` |
| `anthropic` | AnthropicChatModel | `anthropic` |
| `deepseek` | OpenAIChatModel | `deepseek` |
| `gemini` | GeminiChatModel | `gemini` |
| `kimi-cn` | OpenAIChatModel | `kimi_cn` |
| `kimi-intl` | OpenAIChatModel | `kimi_intl` |
| `minimax-cn` | AnthropicChatModel | `minimax_cn` |
| `minimax` | AnthropicChatModel | `minimax_intl` |
| `zhipu-cn` | OpenAIChatModel | `zhipu_cn` |
| `zhipu-intl` | OpenAIChatModel | `zhipu_intl` |
| `volcengine-cn` | OpenAIChatModel | `volcengine_cn` |
| `volcengine-cn-codingplan` | OpenAIChatModel | `volcengine_cn_codingplan` |
| `siliconflow-cn` | OpenAIChatModel | `siliconflow_cn` |
| `siliconflow-intl` | OpenAIChatModel | `siliconflow_intl` |
| `ollama` | OpenAIChatModel | `ollama` |
| `lmstudio` | OpenAIChatModel | `lmstudio` |
| `openrouter` | OpenAIChatModel | `openrouter` |
| `modelscope` | OpenAIChatModel | `modelscope` |
| 其他 OpenAIChatModel | OpenAIChatModel | `openapi_compatible`（兜底） |
| 其他 AnthropicChatModel | AnthropicChatModel | `anthropic` + base_url |

关键设计：
- 始终传递 QwenPaw JSON 中的 base_url（用户可能选了不同区域）
- `require_api_key=False` 的 provider（ollama、lmstudio）不需要 api_key
- 无法映射的 provider 使用兜底策略

#### 2.4 读取流程

新增 `services/qwenpaw_source.py`：

```python
def load_from_qwenpaw() -> QwenPawConfig | None:
    """从 QwenPaw 读取 LLM 配置。

    返回 QwenPawConfig(model, provider_key, api_key, base_url) 或 None。
    """
    # 1. 定位 SECRET_DIR
    secret_dir = resolve_qwenpaw_secret_dir()
    if not secret_dir or not secret_dir.exists():
        return None

    # 2. 读取 active_model.json
    active = _read_active_model(secret_dir)
    if not active:
        return None

    # 3. 读取 provider 配置 JSON（搜索 builtin > custom > plugin）
    provider_data = _find_provider_json(secret_dir, active.provider_id)
    if provider_data is None:
        return None

    # 4. 解密 api_key
    api_key = _decrypt_api_key(provider_data, secret_dir)

    # 5. 映射到 iac-code provider_key
    provider_key = _map_to_iac_provider(active.provider_id, provider_data)

    # 6. 返回配置
    return QwenPawConfig(
        model=active.model,
        provider_key=provider_key,
        api_key=api_key,
        base_url=provider_data.get("base_url"),
    )
```

加密解密：
- 只有 `api_key` 字段被加密，格式 `ENC:` + Fernet token
- Master key 获取：OS Keychain (`keyring.get_password("qwenpaw", "master_key")`) → `.master_key` 文件
- Fernet key 构造：`base64.urlsafe_b64encode(bytes.fromhex(key_hex)[:32])`
- 解密失败返回空字符串（不抛异常）

#### 2.5 每次调用前重新读取

推荐在每次 LLM 调用前重新读取 `active_model.json`（< 100 bytes，< 0.1ms）：
- 如果 provider_id 或 model 变了 → 重新读取 provider JSON + reconfigure provider
- 如果没变 → 复用当前 provider 实例

实现方式：在 `ProviderManager` 中新增 `_check_qwenpaw_config_change()` 方法，在 `stream()` 和 `complete()` 开头调用。

#### 2.6 优先级

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1 | 环境变量 `IAC_CODE_API_KEY` + `IAC_CODE_MODEL` + `IAC_CODE_PROVIDER` | 最高，覆盖一切 |
| 2 | QwenPaw（当 `llm_source: qwenpaw`） | provider + model + api_key + base_url |
| 3 | 本地配置（当 `llm_source: local` 或缺省） | settings.yml + credentials.yml |

#### 2.7 /auth 和 /model 命令

当 `llm_source: qwenpaw` 时：

| 命令 | 行为 |
|------|------|
| `/auth` → LLM 配置 | 提示：「LLM 配置由 QwenPaw 管理，请在 QwenPaw 设置 → 模型中配置」 |
| `/auth` → Cloud 配置 | 正常工作 |
| `/model` | 提示：「模型由 QwenPaw 管理，请在 QwenPaw 中切换」 |

#### 2.8 错误处理

| 场景 | 行为 |
|------|------|
| SECRET_DIR 不存在 | 提示「QwenPaw 未安装或未初始化，请运行 qwenpaw init」 |
| `active_model.json` 不存在 | 提示「请在 QwenPaw 中选择模型 (qwenpaw app → 设置 → 模型)」 |
| Provider JSON 不存在 | 提示「QwenPaw 中 {provider} 未配置」 |
| api_key 为空或解密失败 | 提示「请在 QwenPaw 中配置 {provider} 的 API Key」 |
| provider 为 gemini（Phase 2 前） | 提示「iac-code 暂不支持 Gemini，请在 QwenPaw 中切换到其他模型」 |
| 本地服务未启动（ollama 等） | 正常的连接超时错误 |

---

### 3. 现有 Provider 模型列表更新

#### 3.1 DashScope (dashscope)

```python
ProviderDescriptor(
    key="dashscope",
    name="DashScope",
    display_name="阿里云百炼",
    provider_class="iac_code.providers.dashscope_provider.DashScopeProvider",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    models=[
        ModelEntry("qwen3.6-plus", is_default=True),
        ModelEntry("qwen3.6-max-preview"),
        ModelEntry("qwen3.5-plus"),
        ModelEntry("qwen3.5-flash"),
        ModelEntry("qwq-plus"),
        ModelEntry("qwen3-coder-plus"),
        ModelEntry("kimi-k2.6"),
        ModelEntry("deepseek-v4-pro"),
        ModelEntry("deepseek-v4-flash"),
        ModelEntry("glm-5.1"),
    ],
    qwenpaw_provider_ids=["dashscope"],
)
```

#### 3.2 DashScope Token Plan (dashscope_token_plan)

```python
ProviderDescriptor(
    key="dashscope_token_plan",
    name="DashScope Token Plan",
    display_name="阿里云百炼 Token Plan",
    provider_class="iac_code.providers.dashscope_provider.DashScopeProvider",
    base_url="https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    models=[
        ModelEntry("qwen3.6-plus", is_default=True),
        ModelEntry("deepseek-v3.2"),
        ModelEntry("glm-5"),
        ModelEntry("MiniMax-M2.5"),
        ModelEntry("kimi-k2.5"),
    ],
    qwenpaw_provider_ids=["aliyun-tokenplan"],
)
```

#### 3.3 OpenAI (openai)

```python
ProviderDescriptor(
    key="openai",
    name="OpenAI",
    display_name="OpenAI",
    provider_class="iac_code.providers.openai_provider.OpenAIProvider",
    base_url=None,
    models=[
        ModelEntry("gpt-5.5", is_default=True),
        ModelEntry("gpt-5.4"),
        ModelEntry("gpt-5.4-mini"),
        ModelEntry("gpt-5.3-codex"),
        ModelEntry("gpt-5.2"),
        ModelEntry("o3"),
        ModelEntry("o4-mini"),
    ],
    qwenpaw_provider_ids=["openai"],
)
```

#### 3.4 Anthropic (anthropic)

```python
ProviderDescriptor(
    key="anthropic",
    name="Anthropic",
    display_name="Anthropic",
    provider_class="iac_code.providers.anthropic_provider.AnthropicProvider",
    base_url=None,
    models=[
        ModelEntry("claude-opus-4-7", is_default=True),
        ModelEntry("claude-opus-4-6"),
        ModelEntry("claude-sonnet-4-6"),
        ModelEntry("claude-sonnet-4-6-1m"),
        ModelEntry("claude-haiku-4-5-20251001"),
    ],
    qwenpaw_provider_ids=["anthropic"],
    qwenpaw_chat_model="AnthropicChatModel",
)
```

#### 3.5 DeepSeek (deepseek)

```python
ProviderDescriptor(
    key="deepseek",
    name="DeepSeek",
    display_name="DeepSeek",
    provider_class="iac_code.providers.deepseek_provider.DeepSeekProvider",
    base_url="https://api.deepseek.com/v1",
    models=[
        ModelEntry("deepseek-v4-pro", is_default=True),
        ModelEntry("deepseek-v4-flash"),
    ],
    qwenpaw_provider_ids=["deepseek"],
)
```

#### 3.6 OpenAPI Compatible (openapi_compatible)

```python
ProviderDescriptor(
    key="openapi_compatible",
    name="OpenAPI Compatible",
    display_name="OpenAPI 兼容",
    provider_class="iac_code.providers.openai_provider.OpenAIProvider",
    base_url=None,
    models=[],
)
```

#### 3.7 Thinking 配置更新

`thinking.py` 中的 `MODEL_THINKING` 新增条目：

```python
"openai": {
    # 现有
    "gpt-5.5": ThinkingSpec(ThinkingFamily.OPENAI, _OPENAI_EFFORTS, EffortLevel.HIGH),
    "gpt-5.4": ThinkingSpec(ThinkingFamily.OPENAI, _OPENAI_EFFORTS, EffortLevel.HIGH),
    "gpt-5.4-mini": ThinkingSpec(ThinkingFamily.OPENAI, _OPENAI_EFFORTS, EffortLevel.HIGH),
    "gpt-5.3-codex": ThinkingSpec(ThinkingFamily.OPENAI, _OPENAI_EFFORTS, EffortLevel.HIGH),
    "gpt-5.2": ThinkingSpec(ThinkingFamily.OPENAI, _OPENAI_EFFORTS, EffortLevel.HIGH),
    # 新增
    "o3": ThinkingSpec(ThinkingFamily.OPENAI, _OPENAI_EFFORTS, EffortLevel.HIGH),
    "o4-mini": ThinkingSpec(ThinkingFamily.OPENAI, _OPENAI_EFFORTS, EffortLevel.HIGH),
},
```

---

### 4. Phase 1 文件变更清单

| 文件 | 变更类型 | 说明 |
|------|----------|------|
| `src/iac_code/providers/registry.py` | **新增** | ProviderDescriptor + PROVIDER_REGISTRY + 现有 6 provider 注册 |
| `src/iac_code/services/qwenpaw_source.py` | **新增** | QwenPaw 配置读取、解密、映射 |
| `src/iac_code/providers/manager.py` | 重构 | create_provider 改为注册表驱动；新增 base_url/provider_key_override 参数；更新 MODEL_FALLBACK_MAP |
| `src/iac_code/providers/openai_provider.py` | 修改 | `__init__` 新增 `provider_key` 参数 |
| `src/iac_code/providers/deepseek_provider.py` | 修改 | `__init__` 新增 `base_url` 和 `provider_key` 参数，不再硬编码 URL |
| `src/iac_code/providers/anthropic_provider.py` | 修改 | `__init__` 新增 `provider_key` 参数 |
| `src/iac_code/providers/dashscope_provider.py` | 无需修改 | 已支持 `provider_key` 和 `base_url` |
| `src/iac_code/config.py` | 修改 | 映射表从 registry 派生；新增 get_llm_source()；load_credentials 增加 qwenpaw 分支 |
| `src/iac_code/commands/auth.py` | 修改 | PROVIDERS 列表从 registry 派生；qwenpaw 模式下屏蔽 LLM 配置 |
| `src/iac_code/commands/model.py` | 修改 | qwenpaw 模式下提示去 QwenPaw |
| `src/iac_code/providers/thinking.py` | 修改 | 新增 o3/o4-mini thinking spec |
| `src/iac_code/ui/repl.py` | 修改 | 初始化时根据 llm_source 选择配置来源；调用前检测配置变更 |
| `src/iac_code/cli/headless.py` | 修改 | 同 repl.py |
| `src/iac_code/ui/banner.py` | 修改 | 显示 LLM 来源标识 |
| `pyproject.toml` | 修改 | 添加 cryptography + keyring 为可选依赖 |
| `tests/test_qwenpaw_source.py` | **新增** | 目录定位、映射、解密、回退测试 |
| `tests/test_provider_registry.py` | **新增** | 注册表一致性测试 |

---

## Phase 2：新 Provider 扩展

### 5. 新增 Provider 完整列表

#### 5.1 Gemini (gemini) — 新增 GeminiProvider

需新建 `GeminiProvider`，使用 `google-genai` SDK（非 OpenAI 兼容协议）。

```python
ProviderDescriptor(
    key="gemini",
    name="Gemini",
    display_name="Google Gemini",
    provider_class="iac_code.providers.gemini_provider.GeminiProvider",
    base_url=None,
    models=[
        ModelEntry("gemini-2.5-pro", is_default=True),
        ModelEntry("gemini-2.5-flash"),
        ModelEntry("gemini-2.5-flash-lite"),
        ModelEntry("gemini-2.0-flash"),
    ],
    qwenpaw_provider_ids=["gemini"],
    qwenpaw_chat_model="GeminiChatModel",
)
```

GeminiProvider 实现要点：
- 继承 `Provider` 抽象基类（不继承 OpenAIProvider）
- 使用 `google.genai.Client` 异步 API
- 实现 `stream()` 和 `complete()` 方法
- Token 统计字段映射：`prompt_token_count` → `input_tokens`，`candidates_token_count` → `output_tokens`，`cached_content_token_count` → `cache_read_input_tokens`
- Thinking 模式：通过 `generation_config.thinking_config` 控制
- Tool calling：`google.genai.types.Tool` + `FunctionDeclaration` 格式
- 依赖 `google-genai`，lazy import，缺失时明确报错

#### 5.2 Kimi CN (kimi_cn) — KimiProvider(OpenAIProvider)

```python
ProviderDescriptor(
    key="kimi_cn",
    name="Kimi CN",
    display_name="Kimi 中国版",
    provider_class="iac_code.providers.kimi_provider.KimiProvider",
    base_url="https://api.moonshot.cn/v1",
    models=[
        ModelEntry("kimi-k2.6", is_default=True),
        ModelEntry("kimi-k2.5"),
    ],
    qwenpaw_provider_ids=["kimi-cn"],
)
```

KimiProvider 极薄，类似 DeepSeekProvider：固定 base_url + provider_key。

#### 5.3 Kimi Intl (kimi_intl)

```python
ProviderDescriptor(
    key="kimi_intl",
    name="Kimi Intl",
    display_name="Kimi 国际版",
    provider_class="iac_code.providers.kimi_provider.KimiProvider",
    base_url="https://api.moonshot.ai/v1",
    models=[
        ModelEntry("kimi-k2.6", is_default=True),
        ModelEntry("kimi-k2.5"),
    ],
    qwenpaw_provider_ids=["kimi-intl"],
)
```

#### 5.4 MiniMax CN (minimax_cn) — MiniMaxProvider(AnthropicProvider)

MiniMax 使用 Anthropic 兼容协议。

```python
ProviderDescriptor(
    key="minimax_cn",
    name="MiniMax CN",
    display_name="MiniMax 中国版",
    provider_class="iac_code.providers.minimax_provider.MiniMaxProvider",
    base_url="https://api.minimaxi.com/anthropic",
    models=[
        ModelEntry("MiniMax-M2.5", is_default=True),
        ModelEntry("MiniMax-M2.7"),
    ],
    qwenpaw_provider_ids=["minimax-cn"],
    qwenpaw_chat_model="AnthropicChatModel",
)
```

#### 5.5 MiniMax Intl (minimax_intl)

```python
ProviderDescriptor(
    key="minimax_intl",
    name="MiniMax",
    display_name="MiniMax 国际版",
    provider_class="iac_code.providers.minimax_provider.MiniMaxProvider",
    base_url="https://api.minimax.io/anthropic",
    models=[
        ModelEntry("MiniMax-M2.5", is_default=True),
        ModelEntry("MiniMax-M2.7"),
    ],
    qwenpaw_provider_ids=["minimax"],
    qwenpaw_chat_model="AnthropicChatModel",
)
```

#### 5.6 ZhiPu CN (zhipu_cn) — ZhiPuProvider(OpenAIProvider)

```python
ProviderDescriptor(
    key="zhipu_cn",
    name="ZhiPu CN",
    display_name="智谱 AI",
    provider_class="iac_code.providers.zhipu_provider.ZhiPuProvider",
    base_url="https://open.bigmodel.cn/api/paas/v4",
    models=[
        ModelEntry("glm-5.1", is_default=True),
        ModelEntry("glm-5"),
        ModelEntry("glm-5-turbo"),
    ],
    qwenpaw_provider_ids=["zhipu-cn"],
)
```

#### 5.7 ZhiPu Intl (zhipu_intl)

```python
ProviderDescriptor(
    key="zhipu_intl",
    name="ZhiPu Intl",
    display_name="ZhiPu AI (Intl)",
    provider_class="iac_code.providers.zhipu_provider.ZhiPuProvider",
    base_url="https://api.z.ai/api/paas/v4",
    models=[
        ModelEntry("glm-5.1", is_default=True),
        ModelEntry("glm-5"),
        ModelEntry("glm-5-turbo"),
    ],
    qwenpaw_provider_ids=["zhipu-intl"],
)
```

#### 5.8 Volcengine CN (volcengine_cn) — VolcengineProvider(OpenAIProvider)

```python
ProviderDescriptor(
    key="volcengine_cn",
    name="Volcengine CN",
    display_name="火山引擎",
    provider_class="iac_code.providers.volcengine_provider.VolcengineProvider",
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    models=[
        ModelEntry("doubao-seed-2-0-code-preview-260215", is_default=True),
        ModelEntry("doubao-seed-2-0-pro-260215"),
        ModelEntry("doubao-seed-2-0-lite-260428"),
    ],
    qwenpaw_provider_ids=["volcengine-cn"],
)
```

#### 5.9 SiliconFlow CN (siliconflow_cn) — SiliconFlowProvider(OpenAIProvider)

```python
ProviderDescriptor(
    key="siliconflow_cn",
    name="SiliconFlow CN",
    display_name="硅基流动",
    provider_class="iac_code.providers.siliconflow_provider.SiliconFlowProvider",
    base_url="https://api.siliconflow.cn/v1",
    models=[],
    qwenpaw_provider_ids=["siliconflow-cn"],
)
```

#### 5.10 SiliconFlow Intl (siliconflow_intl)

```python
ProviderDescriptor(
    key="siliconflow_intl",
    name="SiliconFlow Intl",
    display_name="SiliconFlow (Intl)",
    provider_class="iac_code.providers.siliconflow_provider.SiliconFlowProvider",
    base_url="https://api.siliconflow.com/v1",
    models=[],
    qwenpaw_provider_ids=["siliconflow-intl"],
)
```

#### 5.11 Ollama (ollama) — OllamaProvider(OpenAIProvider)

```python
ProviderDescriptor(
    key="ollama",
    name="Ollama",
    display_name="Ollama (本地)",
    provider_class="iac_code.providers.ollama_provider.OllamaProvider",
    base_url="http://localhost:11434/v1",
    models=[],
    require_api_key=False,
    is_local=True,
    qwenpaw_provider_ids=["ollama"],
)
```

OllamaProvider 要点：不需要 API key，base_url 可被用户覆盖。

#### 5.12 LM Studio (lmstudio) — LMStudioProvider(OpenAIProvider)

```python
ProviderDescriptor(
    key="lmstudio",
    name="LM Studio",
    display_name="LM Studio (本地)",
    provider_class="iac_code.providers.lmstudio_provider.LMStudioProvider",
    base_url="http://localhost:1234/v1",
    models=[],
    require_api_key=False,
    is_local=True,
    qwenpaw_provider_ids=["lmstudio"],
)
```

#### 5.13 OpenRouter (openrouter) — OpenRouterProvider(OpenAIProvider)

```python
ProviderDescriptor(
    key="openrouter",
    name="OpenRouter",
    display_name="OpenRouter",
    provider_class="iac_code.providers.openrouter_provider.OpenRouterProvider",
    base_url="https://openrouter.ai/api/v1",
    models=[],
    qwenpaw_provider_ids=["openrouter"],
)
```

OpenRouterProvider 要点：需设置 `HTTP-Referer` 和 `X-Title` 请求头。

#### 5.14 Azure OpenAI (azure_openai) — AzureOpenAIProvider(OpenAIProvider)

```python
ProviderDescriptor(
    key="azure_openai",
    name="Azure OpenAI",
    display_name="Azure OpenAI",
    provider_class="iac_code.providers.azure_openai_provider.AzureOpenAIProvider",
    base_url=None,  # 用户填写部署 URL
    models=[
        ModelEntry("gpt-5", is_default=True),
        ModelEntry("gpt-5-mini"),
        ModelEntry("gpt-4.1"),
        ModelEntry("gpt-4o"),
    ],
    qwenpaw_provider_ids=["azure-openai"],
)
```

#### 5.15 ModelScope (modelscope) — ModelScopeProvider(OpenAIProvider)

```python
ProviderDescriptor(
    key="modelscope",
    name="ModelScope",
    display_name="魔搭",
    provider_class="iac_code.providers.modelscope_provider.ModelScopeProvider",
    base_url="https://api-inference.modelscope.cn/v1",
    models=[
        ModelEntry("Qwen/Qwen3.5-122B-A10B", is_default=True),
    ],
    qwenpaw_provider_ids=["modelscope"],
)
```

#### 5.16 Aliyun CodingPlan (aliyun_codingplan)

```python
ProviderDescriptor(
    key="aliyun_codingplan",
    name="Aliyun CodingPlan",
    display_name="阿里云编程计划",
    provider_class="iac_code.providers.dashscope_provider.DashScopeProvider",
    base_url="https://coding.dashscope.aliyuncs.com/v1",
    models=[
        ModelEntry("qwen3.6-plus", is_default=True),
        ModelEntry("qwen3.5-plus"),
        ModelEntry("glm-5"),
        ModelEntry("MiniMax-M2.5"),
        ModelEntry("kimi-k2.5"),
    ],
    qwenpaw_provider_ids=["aliyun-codingplan"],
)
```

#### 5.17 Aliyun CodingPlan Intl (aliyun_codingplan_intl)

```python
ProviderDescriptor(
    key="aliyun_codingplan_intl",
    name="Aliyun CodingPlan Intl",
    display_name="阿里云编程计划（国际）",
    provider_class="iac_code.providers.dashscope_provider.DashScopeProvider",
    base_url="https://coding-intl.dashscope.aliyuncs.com/v1",
    models=[
        ModelEntry("qwen3.6-plus", is_default=True),
        ModelEntry("qwen3.5-plus"),
        ModelEntry("glm-5"),
        ModelEntry("MiniMax-M2.5"),
        ModelEntry("kimi-k2.5"),
    ],
    qwenpaw_provider_ids=["aliyun-codingplan-intl"],
)
```

#### 5.18 ZhiPu CN CodingPlan (zhipu_cn_codingplan)

```python
ProviderDescriptor(
    key="zhipu_cn_codingplan",
    name="ZhiPu CN CodingPlan",
    display_name="智谱编程计划",
    provider_class="iac_code.providers.zhipu_provider.ZhiPuProvider",
    base_url="https://open.bigmodel.cn/api/coding/paas/v4",
    models=[
        ModelEntry("glm-5.1", is_default=True),
        ModelEntry("glm-5"),
    ],
    qwenpaw_provider_ids=["zhipu-cn-codingplan"],
)
```

#### 5.19 ZhiPu Intl CodingPlan (zhipu_intl_codingplan)

```python
ProviderDescriptor(
    key="zhipu_intl_codingplan",
    name="ZhiPu Intl CodingPlan",
    display_name="ZhiPu AI CodingPlan (Intl)",
    provider_class="iac_code.providers.zhipu_provider.ZhiPuProvider",
    base_url="https://api.z.ai/api/coding/paas/v4",
    models=[
        ModelEntry("glm-5.1", is_default=True),
        ModelEntry("glm-5"),
    ],
    qwenpaw_provider_ids=["zhipu-intl-codingplan"],
)
```

#### 5.20 Volcengine CodingPlan (volcengine_cn_codingplan)

```python
ProviderDescriptor(
    key="volcengine_cn_codingplan",
    name="Volcengine CodingPlan",
    display_name="火山引擎编程计划",
    provider_class="iac_code.providers.volcengine_provider.VolcengineProvider",
    base_url="https://ark.cn-beijing.volces.com/api/coding/v3",
    models=[
        ModelEntry("doubao-seed-2-0-code-preview-260215", is_default=True),
        ModelEntry("doubao-seed-2-0-pro-260215"),
        ModelEntry("doubao-seed-2-0-lite-260428"),
    ],
    qwenpaw_provider_ids=["volcengine-cn-codingplan"],
)
```

---

### 6. Prompt Cache 策略

缓存策略是 **provider class 内部逻辑**，不在 ProviderDescriptor 中声明。各 provider class 自行决定是否以及如何使用缓存。

#### 6.1 主动缓存（provider class 内部按模型决定）

**DashScope 系列**（已有实现，无需修改）：

`DashScopeProvider._supports_explicit_cache()` 按模型前缀判断是否插入 `cache_control` 标记：

```python
_EXPLICIT_CACHE_MODEL_PREFIXES = (
    "qwen3-coder-plus", "qwen3-coder-flash",
    "qwen3.5-plus", "qwen3.6-plus",
    "qwen-plus", "qwen3.5-flash",
    "qwen3.6-flash", "qwen-flash",
)
```

同一个 DashScope provider 下：
- `qwen3.6-plus` → 命中前缀 → 插入 system + last-user cache_control 标记
- `deepseek-v4-pro` → 不命中 → 不插入标记，走 passthrough

此逻辑对 `dashscope`、`dashscope_token_plan`、`aliyun_codingplan`、`aliyun_codingplan_intl` 均生效（它们共享 `DashScopeProvider` class）。

**Anthropic**（Phase 2 新增）：

Anthropic API 的 cache_control 是 API 级别特性，所有模型都支持。在 `AnthropicProvider._build_kwargs` 中新增主动标记：

```python
def _build_system_with_cache(self, system: str) -> list[dict]:
    static_part, dynamic_part = split_by_dynamic_boundary(system)
    blocks = [
        {"type": "text", "text": static_part, "cache_control": {"type": "ephemeral"}}
    ]
    if dynamic_part:
        blocks.append({"type": "text", "text": dynamic_part})
    return blocks
```

同时对最后一条 user message 也标记 cache_control。将 DashScope 的 `_mark_last_user_message_cacheable` 提取为共享工具函数供两者复用。

#### 6.2 被动统计（所有 provider 通用）

所有 provider 都从 API 响应中读取缓存统计信息：

| Provider 类型 | 缓存字段来源 |
|---|---|
| OpenAI 兼容（OpenAI/DeepSeek/Kimi/ZhiPu/...） | `usage.prompt_tokens_details.cached_tokens` + `cache_creation_input_tokens` |
| Anthropic 兼容（Anthropic/MiniMax） | `usage.cache_creation_input_tokens` + `cache_read_input_tokens` |
| Gemini | `usage_metadata.cached_content_token_count` |
| 本地（Ollama/LM Studio） | 仅 `input_tokens` + `output_tokens`（无缓存字段） |

**关于 `supports_stream_options`**：这是 provider class 的 class attribute，控制是否在 streaming 请求中附加 `stream_options={"include_usage": True}`。各 provider class 自行声明：
- `DashScopeProvider.supports_stream_options = True`
- `DeepSeekProvider.supports_stream_options = True`
- `OpenAIProvider.supports_stream_options = False`（基类默认，OpenAI 自动返回 usage）
- 新 provider 子类继承自 `OpenAIProvider`，按需覆盖

---

### 7. Token 统计

#### 7.1 API 报告的 Usage

所有 provider 统一使用 `Usage` 数据类（已有）。各 provider 子类负责从 API 响应中提取 usage 并填充。

Gemini 特殊映射：
- `prompt_token_count` → `input_tokens`
- `candidates_token_count` → `output_tokens`
- `cached_content_token_count` → `cache_read_input_tokens`

#### 7.2 客户端估算

`services/token_counter.py` 扩展 `_MODEL_ENCODING_MAP`：

```python
_MODEL_ENCODING_MAP = {
    "gpt-5": "o200k_base",
    "gpt-4o": "o200k_base",
    "gpt-4": "cl100k_base",
    "o3": "o200k_base",
    "o4": "o200k_base",
    "claude": "cl100k_base",
    "qwen": "cl100k_base",
    "deepseek": "cl100k_base",
    "gemini": "cl100k_base",
    "glm": "cl100k_base",
    "kimi": "cl100k_base",
    "minimax": "cl100k_base",
    "doubao": "cl100k_base",
}
```

---

### 8. Phase 2 文件变更清单

| 文件 | 变更类型 | 说明 |
|------|----------|------|
| `src/iac_code/providers/gemini_provider.py` | **新增** | GeminiProvider（Google GenAI SDK） |
| `src/iac_code/providers/kimi_provider.py` | **新增** | KimiProvider(OpenAIProvider) |
| `src/iac_code/providers/minimax_provider.py` | **新增** | MiniMaxProvider(AnthropicProvider) |
| `src/iac_code/providers/zhipu_provider.py` | **新增** | ZhiPuProvider(OpenAIProvider) |
| `src/iac_code/providers/volcengine_provider.py` | **新增** | VolcengineProvider(OpenAIProvider) |
| `src/iac_code/providers/siliconflow_provider.py` | **新增** | SiliconFlowProvider(OpenAIProvider) |
| `src/iac_code/providers/ollama_provider.py` | **新增** | OllamaProvider(OpenAIProvider) |
| `src/iac_code/providers/lmstudio_provider.py` | **新增** | LMStudioProvider(OpenAIProvider) |
| `src/iac_code/providers/openrouter_provider.py` | **新增** | OpenRouterProvider(OpenAIProvider) |
| `src/iac_code/providers/azure_openai_provider.py` | **新增** | AzureOpenAIProvider(OpenAIProvider) |
| `src/iac_code/providers/modelscope_provider.py` | **新增** | ModelScopeProvider(OpenAIProvider) |
| `src/iac_code/providers/registry.py` | 修改 | 注册新 provider |
| `src/iac_code/providers/thinking.py` | 修改 | 新增 Gemini/Kimi/MiniMax thinking spec |
| `src/iac_code/providers/anthropic_provider.py` | 修改 | 新增主动 cache_control 标记 |
| `src/iac_code/services/token_counter.py` | 修改 | 扩展 _MODEL_ENCODING_MAP |
| `src/iac_code/config.py` | 修改 | 新增 credential slots |
| `pyproject.toml` | 修改 | 新增 google-genai 可选依赖 |
| `tests/test_gemini_provider.py` | **新增** | Gemini provider 测试 |
| `tests/test_new_providers.py` | **新增** | 新 provider 统一测试 |

---

### 9. 依赖变更

| 包 | 用途 | 阶段 | 处理方式 |
|----|------|------|---------|
| `cryptography` | Fernet 解密 QwenPaw api_key | Phase 1 | 可选依赖 (extras: qwenpaw)，lazy import |
| `keyring` | OS Keychain 读取 master key | Phase 1 | 可选依赖 (extras: qwenpaw)，lazy import |
| `google-genai` | Gemini Provider | Phase 2 | 可选依赖 (extras: gemini)，lazy import |

所有三个依赖使用 lazy import，缺失时给出明确提示。

---

### 10. Credentials 体系扩展

`load_credentials()` 当前返回 6 个固定 slots。扩展后改为从 `PROVIDER_REGISTRY` 动态生成：

```python
def load_credentials(model: str | None = None) -> dict[str, str]:
    raw = _load_yaml(get_credentials_path())
    creds = {}
    for key in PROVIDER_REGISTRY:
        creds[key] = str(raw.get(key, "") or "")
    # 保留 legacy 兼容
    if not creds.get("dashscope"):
        creds["dashscope"] = str(raw.get("bailian", "") or "")
    # 环境变量覆盖（逻辑不变）
    ...
    return creds
```

本地 provider（ollama、lmstudio）的 credential slot 存在但允许为空（`require_api_key=False`）。

---

### 11. 安全考虑

- **只读**：iac-code 不修改 QwenPaw 任何文件
- **不缓存明文**：每次读取，api_key 只在内存中短暂持有
- **日志安全**：解密后的 api_key 不输出到日志
- **解密失败优雅降级**：返回原密文时检测 `ENC:` 前缀并报错
- **新 credential slots**：遵循现有 `.credentials.yml` 模式，不引入新的存储位置
