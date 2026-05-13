---
title: 認証
description: 認証フローで LLM とクラウドの認証情報を設定。
---

# 認証

対話モードで `/auth` を使用して、モデルプロバイダーのアクセスと Alibaba Cloud のアクセスの両方を設定します。

```bash
iac-code
```

```text
/auth
```

認証フローでは、プロバイダーの選択、API キーの入力、モデルの選択、Alibaba Cloud の認証情報のセットアップをガイドします。

ランタイム設定はユーザー設定ディレクトリに保存されます：

```text
~/.iac-code/
```

重要なファイル：

| ファイル | 用途 |
|---|---|
| `.credentials.yml` | LLM プロバイダーの認証情報 |
| `.cloud-credentials.yml` | Alibaba Cloud の認証情報 |
| `settings.yml` | ランタイム設定 |
