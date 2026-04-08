---
title: VSCode上のコミット時の署名にBitwarden SSH Agentを使う
date: 2025-10-10 12:00:00
slug: vscode-commit-signing-with-bitwarden
draft: False
categories:
  - プログラミング
---

こんにちは、しののめです。  
昨今のサプライチェーン攻撃の流行を受けて、会社のセキュリティ要件として全エンジニアがGitでのコミットに署名と署名時の認証を求められるようになりました。  

## Bitwarden側の設定

### Bitwardenアプリのインストール

macにはBitwardenアプリをインストールしておきます。  
自分はアプリストアから入れました。

https://apps.apple.com/jp/app/bitwarden/id1352778147?mt=12

### SSHキーの作成と設定

ここからは基本的に公式ドキュメントに沿って作業しましょう。  
https://bitwarden.com/help/ssh-agent/

[Create new SSH key](https://bitwarden.com/help/ssh-agent/#create-new-ssh-key)ではアプリ上からSSHキーを作成します。  
[Configure Bitwarden SSH agent](https://bitwarden.com/help/ssh-agent/#configure-bitwarden-ssh-agent)でSSHエージェントの設定を行います。  
私の場合はストアからアプリをインストールしたので`.zshrc`に以下を追加しました。

```bash
export SSH_AUTH_SOCK="$HOME/Library/Containers/com.bitwarden.desktop/Data/.bitwarden-ssh-agent.sock"
```

[Enable SSH agent](https://bitwarden.com/help/ssh-agent/#enable-ssh-agent)でBitWardenのSSHエージェントを有効化します。  
アプリを開いてメニューバー BitWarden > 設定 で「SSHエージェントを有効にする」にチェックを入れます。  
認証の要求頻度ですが、「常に表示する」がセキュリティ的に良いですが「保管庫がロックされるまで記憶する」でも良いかもしれません。

[Testing SSH keys](https://bitwarden.com/help/ssh-agent/#testing-ssh-keys)でSSHキーのテストを行います。  
ターミナルで下記コマンド実行して、BitWardenに登録したSSHキーが表示されれば成功です。
```bash
ssh-add -L
```

### GitとGitHubの設定

[Configure Git for SSH signing](https://bitwarden.com/help/ssh-agent/#configure-git-for-ssh-signing)に沿ってGitの設定を行います。

署名にSSHを利用するように設定。
```bash
git config --global gpg.format ssh
```

署名鍵として使用するSSH鍵を指定します。  
BitWardenアプリで作成したSSHキーの公開鍵を指定します。
```bash
git config --global user.signingkey "<YOUR_PUBLIC_KEY>"
```

自動コミット署名を有効にします。
```bash
git config --global commit.gpgSign true
```

これらがうまく設定されていれば`.gitconfig`にも反映されているはずです。

[Sign Git commits](https://bitwarden.com/help/ssh-agent/#sign-git-commits)でコミットに署名しましょう。  
まずはGitHubの[SSH and GPG keys](https://github.com/settings/keys)にBitWardenアプリで作成したSSHキーの公開鍵を登録します。  
**Key type**は`Signing Key`にするのを忘れずに。

そうしたら次のコマンドで`allowedSigners`を利用するように設定します。
```bash
git config --global gpg.ssh.allowedSignersFile "$HOME/.ssh/allowedSigners"
```

`allowedSigners`に公開鍵を追加します。  
私は`allowedSigners`がなかったため`~/.ssh`に新規作成しました。  
中身は署名に利用するメールアドレスと公開鍵をスペース区切りで1行にまとめたものを追加します。
```text
your@mail.address.com <BITWARDEN_SSH_PUBLIC_KEY>
```

## VSCodeの設定

settings.jsonに以下を追加します。

```json
  "terminal.integrated.env.osx": {
    "SSH_AUTH_SOCK": "${env:HOME}/Library/Containers/com.bitwarden.desktop/Data/.bitwarden-ssh-agent.sock"
  },
  "git.terminalGitEditor": true
```

念の為VSCodeを再起動します。  
これでVSCodeのサイドバーにあるソース管理からコミットした場合にもBitWardenが起動して署名ができるようになります。

以上、セキュリティ対策しながら開発していきましょう。
