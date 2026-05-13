---
title: 非対話モード
description: 引数または標準入力からワンショットプロンプトを実行。
---

# 非対話モード

非対話モードは単一のプロンプトを実行して終了します。REPL に留まらずに繰り返しタスクの出力を生成したい場合に使用します。

`--prompt` でプロンプトを直接渡します：

```bash
iac-code --prompt "Create an OSS Bucket"
```

`--prompt -` で標準入力からプロンプトを読み取ります：

```bash
echo "Create a VPC and two ECS instances" | iac-code --prompt -
```

呼び出し元が構造化出力を必要とする場合は `--output-format` を使用します：

```bash
iac-code --prompt "Create an OSS Bucket" --output-format json
```

エージェントの作業時間を制限するには `--max-turns` を使用します：

```bash
iac-code --prompt "Create a VPC" --max-turns 20
```

サポートされる出力形式：

| 形式 | 用途 |
|---|---|
| `text` | 人間が読みやすい出力。デフォルトです。 |
| `json` | 最終応答を解析する呼び出し元向けの単一 JSON 結果。 |
| `stream-json` | 増分進捗を処理する呼び出し元向けのストリーミング JSON イベント。 |

すべての起動フラグは[コマンドラインオプション](../cli/command-line-options.md)をご覧ください。
