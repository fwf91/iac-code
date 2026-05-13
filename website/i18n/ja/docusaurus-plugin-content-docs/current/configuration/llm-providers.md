---
title: LLM プロバイダー
description: サポートされるモデルプロバイダーと環境変数。
---

# LLM プロバイダー

IaC Code は複数のモデルプロバイダーバックエンドをサポートしています。

| プロバイダー値 | 用途 |
|---|---|
| `Anthropic` | Anthropic モデル |
| `OpenAI` | OpenAI モデル |
| `DashScope` | Alibaba Cloud DashScope 互換エンドポイント |
| `DeepSeek` | DeepSeek モデル |
| `OpenAPICompatible` | カスタム OpenAI 互換エンドポイント |

プロバイダーの選択は CLI オプション、環境変数、または設定ファイルから行えます。優先順位は以下の通りです：

```text
CLI 引数 > 環境変数 > 設定ファイル
```

LLM 環境変数：

| 変数 | 説明 |
|---|---|
| `IAC_CODE_PROVIDER` | モデルプロバイダー名（大文字小文字不問） |
| `IAC_CODE_MODEL` | モデル名 |
| `IAC_CODE_BASE_URL` | `OpenAPICompatible` 用の API エンドポイント |
| `IAC_CODE_API_KEY` | プロバイダー API キー |
