---
title: コマンドラインオプション
description: IaC Code の起動オプションとワンショット実行フラグのリファレンス。
---

# コマンドラインオプション

コマンドラインオプションは IaC Code の起動方法を変更します。対話 REPL に入る前に使用するか、`--prompt` と組み合わせてワンショット自動化に使用します。

| オプション | 用途 |
|---|---|
| `-h`, `--help` | CLI ヘルプを表示して終了します。インストールされたバージョンでサポートされているオプションを確認できます。 |
| `-v`, `-V`, `--version` | インストールされた IaC Code のバージョンを表示して終了します。 |
| `-m <model>`, `--model <model>` | 特定の LLM モデルで開始します。今回の実行で保存済みモデルを上書きします。 |
| `-p <prompt>`, `--prompt <prompt>` | 単一のプロンプトを実行して終了します。非対話モードが有効になります。`--prompt -` で標準入力からプロンプトを読み取ります。 |
| `--output-format <format>` | 非対話モードの出力形式を設定します。サポートされる値は `text`、`json`、`stream-json` です。デフォルトは `text` です。 |
| `--max-turns <number>` | 非対話モードでのエージェントターンの最大数を制限します。デフォルトは `100` です。 |
| `-d`, `--debug` | 今回の実行でデバッグログを有効にします。対話モードでは起動後に `/debug` でデバッグログの検査や変更ができます。 |
| `-r <session-id>`, `--resume <session-id>` | セッション ID で前のセッションを再開します。既知の会話に戻るためのものです。 |
| `-c`, `--continue` | 最新のセッションを再開します。`--resume` と同時に使用できません。 |

## よく使う起動コマンド

保存済みモデルで対話 REPL を開始：

```bash
iac-code
```

今回の実行で特定のモデルを指定して開始：

```bash
iac-code --model qwen3.6-plus
```

ワンショットプロンプトを実行：

```bash
iac-code --prompt "Create an OSS Bucket"
```

標準入力からプロンプトを読み取り：

```bash
echo "Create a VPC and two ECS instances" | iac-code --prompt -
```

最新のセッションを再開：

```bash
iac-code --continue
```
