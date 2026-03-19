---
title: Bitwarden SSH Agent を Docker Desktop for Mac のコンテナ内で使う
date: 2026-03-19 12:00:00
slug: devcontainer-docker-bitwarden-ssh-agent
draft: False
categories:
  - プログラミング
---

こんにちは、しののめです。  
最近の開発では Claude Code を大活用しています。  
ただ、ローカルで動かしていると意図しないコマンドが実行されるリスクがあるため、Docker コンテナ上で動かすよう環境を整えています。  
また、会社のセキュリティ要件で Git コミットに署名が必要になり、Bitwarden の SSH Agent を利用しているのですが、Docker Desktop for Mac のコンテナ内でうまく Bitwarden の SSH エージェントを利用できなくて試行錯誤しました。  
今回はその解決策を共有します。

## TL;DR

Docker Desktop for Mac は Bitwarden SSH Agent を自動転送できません。  
`socat` で TCP ブリッジを構築し、ホスト側 LaunchAgent + コンテナ側 entrypoint で自動化します。

```text
Bitwarden SSH Agent (macOS)
  ↓ Unix socket
socat (macOS, LaunchAgent, TCP:22122)
  ↓ TCP via host.docker.internal
socat (コンテナ, entrypoint)
  ↓ Unix socket (/tmp/bitwarden-ssh-agent.sock)
SSH_AUTH_SOCK → git commit --gpg-sign, ssh -T git@github.com
```

## 背景・動機

- Git コミット署名に SSH 鍵を使いたい
- 秘密鍵は Bitwarden で一元管理（ファイルとしてディスクに置かない）
- 開発は Docker コンテナ内で行う（devcontainer）

## なぜ素朴な方法ではうまくいかないのか

### 試行1: Bitwarden ソケットを直接 bind mount

```yaml
# docker-compose.yml
volumes:
  - ~/Library/Containers/com.bitwarden.desktop/Data/.bitwarden-ssh-agent.sock:/tmp/ssh-agent.sock:ro
environment:
  - SSH_AUTH_SOCK=/tmp/ssh-agent.sock
```

**結果**: `The agent has no identities.`

**原因**: Docker Desktop for Mac はコンテナを Linux VM（LinuxKit）内で実行しています。  
macOS ↔ VM 間のファイル共有（VirtioFS / gRPC-FUSE）は **Unix ソケットの転送をサポートしていません**。  
bind mount しても、VM 内には無効なファイルが作られるだけです。

### 試行2: Docker Desktop 標準の SSH agent 転送

```yaml
# docker-compose.yml
volumes:
  - /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock
environment:
  - SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock
```

**結果**: `The agent has no identities.`

**原因**: Docker Desktop は `/run/host-services/ssh-auth.sock` を通じて **macOS のデフォルト SSH agent**（launchd が管理する `ssh-agent`）を転送します。  
ユーザーの `SSH_AUTH_SOCK` 環境変数は参照しません。

確認方法：

```bash
# ホスト側: Bitwarden agent → 鍵あり
SSH_AUTH_SOCK=~/Library/Containers/com.bitwarden.desktop/Data/.bitwarden-ssh-agent.sock ssh-add -l
# → 256 SHA256:xxxxx Github (ED25519)

# ホスト側: macOS デフォルト agent → 鍵なし
SSH_AUTH_SOCK=/private/tmp/com.apple.launchd.XXXX/Listeners ssh-add -l
# → The agent has no identities.
```

Docker Desktop が転送しているのは後者です。

### 試行3: launchctl setenv で Docker Desktop に環境変数を伝える

```bash
launchctl setenv SSH_AUTH_SOCK "$HOME/Library/Containers/com.bitwarden.desktop/Data/.bitwarden-ssh-agent.sock"
# → Docker Desktop を再起動
```

**結果**: `The agent has no identities.`

**原因**: Docker Desktop は `SSH_AUTH_SOCK` 環境変数を参照せず、macOS のデフォルト SSH agent に直接接続しています（内部実装としてハードコードされている可能性が高いです）。  
Docker Desktop v29.2.1 の `settings-store.json` にも SSH 関連の設定項目は存在しません。

## 解決策: socat TCP ブリッジ

macOS の VM 境界を越えるには、Unix ソケットを一度 TCP に変換し、コンテナ内で再び Unix ソケットに戻します。

### 前提条件

- macOS に socat がインストール済み（`brew install socat`）
- コンテナイメージに socat がインストール済み（`apt-get install socat`）
- Bitwarden デスクトップアプリで SSH Agent が有効化済み

### Step 1: ホスト側 — LaunchAgent で socat リレーを常駐起動

`~/Library/LaunchAgents/com.bitwarden.ssh-relay.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.bitwarden.ssh-relay</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/socat</string>
        <string>TCP-LISTEN:22122,bind=127.0.0.1,fork,reuseaddr</string>
        <string>UNIX-CONNECT:/Users/YOUR_USER/Library/Containers/com.bitwarden.desktop/Data/.bitwarden-ssh-agent.sock</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/bitwarden-ssh-relay.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/bitwarden-ssh-relay.log</string>
</dict>
</plist>
```

> ⚠️ `YOUR_USER` は自分の macOS ユーザー名に置き換えてください。

```bash
# 登録 & 起動
launchctl load ~/Library/LaunchAgents/com.bitwarden.ssh-relay.plist

# 確認
launchctl list com.bitwarden.ssh-relay
lsof -i :22122
# → socat LISTEN on 127.0.0.1:22122
```

ポイント：
- `bind=127.0.0.1` で localhost のみ。外部からアクセスされるリスクなし
- `fork` で複数の同時接続を処理
- `KeepAlive=true` で socat が落ちても自動再起動
- LaunchAgent なのでログイン時に自動起動

### Step 2: Dockerfile — socat をインストール

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    ... \
    openssh-client socat \
    ...
```

### Step 3: entrypoint.sh — ファイアウォール初期化後に socat ブリッジを起動

コンテナ内にファイアウォール（iptables）がある場合、`host.docker.internal` への通信がブロックされます。  
socat セットアップは**ファイアウォール初期化の後**に配置し、必要なルールを動的に追加します。

```bash
# ファイアウォール初期化の後に配置する

if command -v socat >/dev/null 2>&1; then
    SOCAT_SSH_SOCK="/tmp/bitwarden-ssh-agent.sock"

    # host.docker.internal:22122 への通信をファイアウォールで許可
    HOST_DI_IP=$(getent ahosts host.docker.internal 2>/dev/null | awk 'NR==1{print $1}')
    if [ -n "$HOST_DI_IP" ]; then
        sudo iptables -I OUTPUT 1 -d "$HOST_DI_IP" -p tcp --dport 22122 -j ACCEPT 2>/dev/null || true
        sudo iptables -I INPUT 1 -s "$HOST_DI_IP" -p tcp --sport 22122 -m state --state ESTABLISHED -j ACCEPT 2>/dev/null || true
    fi

    rm -f "$SOCAT_SSH_SOCK"
    socat UNIX-LISTEN:"$SOCAT_SSH_SOCK",fork,mode=600 TCP:host.docker.internal:22122 &
    sleep 0.5

    if [ -S "$SOCAT_SSH_SOCK" ]; then
        export SSH_AUTH_SOCK="$SOCAT_SSH_SOCK"
        echo "SSH agent: Bitwarden relay (via socat)"
    else
        echo "SSH agent: socat relay failed, falling back to Docker Desktop"
    fi
fi
```

### Step 4: .zshenv — シェル起動時に SSH_AUTH_SOCK を設定

`docker exec` で入ったとき、entrypoint の `export` は引き継がれません。  
`.zshenv` は interactive / non-interactive 問わず全ての zsh 起動時に読み込まれるため、`docker exec` でも確実に反映されます。

```bash
# .zshenv (entrypoint で生成)
if [ -S "/tmp/bitwarden-ssh-agent.sock" ]; then
    export SSH_AUTH_SOCK="/tmp/bitwarden-ssh-agent.sock"
fi
```

## ハマりポイントまとめ

| ハマりポイント | 原因 | 対処 |
|---|---|---|
| bind mount したソケットが動かない | macOS ↔ Docker VM 間で Unix ソケットは共有不可 | socat で TCP に変換 |
| `/run/host-services/ssh-auth.sock` に鍵がない | Docker Desktop は macOS デフォルト agent を転送する | Bitwarden は別の agent なので socat が必要 |
| `launchctl setenv` しても変わらない | Docker Desktop は `SSH_AUTH_SOCK` を参照していない | socat アプローチに切り替え |
| socat ソケットはあるが `communication with agent failed` | コンテナのファイアウォールが `host.docker.internal` をブロック | iptables ルールを動的追加 |
| ファイアウォール前に socat を起動すると動くが後で壊れる | ファイアウォール初期化で全ルールがフラッシュされる | socat セットアップをファイアウォール初期化の後に配置 |
| `docker exec zsh` で `SSH_AUTH_SOCK` が変わらない | non-interactive shell は `.zshrc` を読まない | `.zshenv` を使う（全ての zsh 起動時に読み込まれる） |

## 動作確認

```bash
# コンテナにシェル接続
docker exec -it cw-devcontainer zsh

# SSH agent の鍵を確認
ssh-add -l
# → 256 SHA256:xxxxx Github (ED25519)

# GitHub 接続テスト
ssh -T git@github.com
# → Hi username! You've successfully authenticated...

# Git コミット署名テスト
git commit --allow-empty -m "test: signing check"
git log --show-signature -1
git reset HEAD~1
```

## セキュリティ考慮

- **ホスト側 socat**: `127.0.0.1` にバインド。外部ネットワークからのアクセス不可
- **秘密鍵**: Bitwarden vault 内に保持。ホストにもコンテナにもファイルとして存在しない
- **コンテナ側ファイアウォール**: `host.docker.internal:22122` のみピンポイントで許可
- **ソケットパーミッション**: `mode=600` で owner のみアクセス可

## 環境情報

- macOS (Apple Silicon)
- Docker Desktop v29.2.1
- Bitwarden Desktop (SSH Agent 有効)
- socat 1.8.x (Homebrew)
