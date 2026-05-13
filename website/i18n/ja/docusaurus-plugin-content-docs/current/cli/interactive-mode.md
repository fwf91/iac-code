---
title: 対話モード
description: REPL を使用してインフラ作業を反復的に行う。
---

# 対話モード

引数なしで実行して対話 REPL に入ります：

```bash
iac-code
```

対話モードは、複数ターンにわたってインフラ要件を詰めたい場合に便利です。

まず認証から始めます：

```text
/auth
```

次に構築したいものを記述します：

```text
Create a VPC, two ECS instances, and a security group that allows SSH from my office IP.
```
