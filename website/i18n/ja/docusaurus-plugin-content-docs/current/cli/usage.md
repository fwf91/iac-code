---
title: CLI 概要
description: ターミナルから IaC Code を起動し、適切なワークフローを選択。
---

# CLI 概要

ターミナルから `iac-code` を実行します：

```bash
iac-code
```

CLI は 2 つのワークフローをサポートしています：

| ワークフロー | 用途 |
|---|---|
| [対話モード](./interactive-mode.md) | REPL で複数ターンにわたってインフラ要件を詰めたい場合。 |
| [非対話モード](../automation/non-interactive-mode.md) | 単一のプロンプトを実行して出力を呼び出し元に返したい場合。 |

よく使う起動コマンド：

```bash
iac-code
iac-code --prompt "Create an OSS Bucket"
echo "Create a VPC" | iac-code --prompt -
iac-code --debug
```

起動フラグは[コマンドラインオプション](./command-line-options.md)を、対話セッション内のコマンドは[スラッシュコマンド](./commands.md)をご覧ください。
