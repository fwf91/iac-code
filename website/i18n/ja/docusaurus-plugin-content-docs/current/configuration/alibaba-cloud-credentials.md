---
title: Alibaba Cloud 認証情報
description: Alibaba Cloud の AccessKey または STS 認証情報の設定。
---

# Alibaba Cloud 認証情報

Alibaba Cloud の認証情報は、クラウドリソースの検査や管理を行う操作に必要です。

サポートされる環境変数：

| 変数 | 説明 |
|---|---|
| `ALIBABA_CLOUD_ACCESS_KEY_ID` | AccessKey ID |
| `ALIBABA_CLOUD_ACCESS_KEY_SECRET` | AccessKey Secret |
| `ALIBABA_CLOUD_SECURITY_TOKEN` | STS トークン。設定すると認証モードが STS に切り替わります |
| `ALIBABA_CLOUD_REGION_ID` | デフォルトリージョン |

実験時はテスト用または一時的な認証情報を使用してください。本番環境のシークレットをシェル履歴、スクリーンショット、ログ、Issue レポートに貼り付けないでください。
