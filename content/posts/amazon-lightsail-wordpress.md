---
title: LightsailのWordPressに独自ドメインを設定する
date: 2018-01-11 23:00:27
slug: amazon-lightsail-wordpress
draft: False
categories:
  - AWS
  - プログラミング
---

諸用でLightsailのWordPressに独自ドメイン設定する必要があったので

自分用の備忘録．

### 前提

・AWSアカウント持っている

・独自ドメイン取得済み (今回はお名前.com)

・DNSはRoute53 (せっかくなので使ってみる)

ざっくりやっていきましょう．

### LightsailでWordpressをたてる

とりあえずインスタンス立てましょう．

コンソールからLightsailのページへ行って「インスタンスの作成」をクリック．

![f:id:Shinogasa:20180109222533p:plain](https://cdn-ak.f.st-hatena.com/images/fotolife/S/Shinogasa/20180109/20180109222533.png)

上の画像は既にインスタンス1個作成済みですが作成していなかったら真ん中に作成のボタンがあった気が．

インスタンスのイメージの選択でWordPressを選択します．

![f:id:Shinogasa:20180109222942p:plain](https://cdn-ak.f.st-hatena.com/images/fotolife/S/Shinogasa/20180109/20180109222942.png)

多分デフォで選択されてます．

インスタンスロケーションは日本がいいですね．

早いので．

インスタンスプランは一番安いやつ．

1ヶ月無料！素敵！

インスタンス名はわかりやすい名前にしておくと後で楽．多分．

全世界で他の人がインスタンス名に使ってないものにしないと怒られます．

最下部の作成をクリックしてインスタンス起動！

ちょっと待てばWordPressの入ったインスタンスがガシャーンってできます．

#### とりあえずアクセス

ホームに戻って作成したインスタンスをクリックすると管理画面が表示されます．

![f:id:Shinogasa:20180109224555p:plain](https://cdn-ak.f.st-hatena.com/images/fotolife/S/Shinogasa/20180109/20180109224555.png)

表示されてるパブリックIPをアドレスバーにコピペしてアクセスすると

WordPressの初期画面が表示されますね．

とりあえずこれで自分のWordPressができました．いえーい．

#### IPを静的IPにする

現状だとインスタンスを再起動したときにIPが変わってしまいます．

そうなってWordPressつながらねえってならないようにするためにIPを固定しましょう．

![f:id:Shinogasa:20180109225611p:plain](https://cdn-ak.f.st-hatena.com/images/fotolife/S/Shinogasa/20180109/20180109225611.png)

管理画面の**ネットワーキング** をクリックして

**静的IPをアタッチ** をクリック

さっき作成したインスタンスを選択して

IPにも全世界で1つの名前をつけてあげて**作成** クリック

静的IPがアタッチされました．素敵．

正しくアタッチされていたらインスタンスのIPの横にピンが表示されます．

#### WordPressの管理画面にアクセス

先程アタッチした静的IPの後ろに/loginって付けると

WordPressの管理画面にアクセスできます

> http://{静的IP}/login

ですね．

ログイン画面が表示されたものの情報がわかりません．

ユーザー名は**user** なんですがパスワードはインスタンスの中にあります．

SSHしてパスワードを入手しましょう．

#### インスタンスにSSHする

Lightsailの管理画面にもSSH用のコンソールがあるのですが

せっかくですのでターミナルからSSHします．

SSH用のプライベートキーをダウンロードしましょう．

インスタンストップ下部の**アカウントページ** っていうリンクから

ダウンロードページに飛びます．

飛んだら**デフォルト** というのがあると思うので**ダウンロード** します．

普段自分がSSHのキー置いているところに配置したら

下記コマンドでSSHしちゃいましょう．

> ssh -i /{SSHキー置いてるディレクトリのフルパス}/落としたキー.pem bitnami@{インスタンスの静的IP}

SSHキーをコピペしちゃったりすると

> It is required that your private key files are NOT accessible by others.  
> This private key will be ignored.  
> Load key "/{フルパス}/{落としたキー.pem}": bad permissions  
> bitnami@{静的IP}: Permission denied (publickey).

って怒られたりします．

権限変わっちゃってるので正しく設定しましょう．

> chmod 600 /{フルパス}/落としたキー.pem

これでSSHしたら接続されるはず．

パスワードを確認しましょう．

> cat bitnami_application_password

これでパスワードがわかりましたね．やったぜ．

ついでにWordPressトップ下部のバナーも消し去りましょう．

> sudo /opt/bitnami/apps/wordpress/bnconfig --disable_banner 1

apache再起動で完了．

> sudo /opt/bitnami/ctlscript.sh restart apache 

これでWordPressの管理画面にログインすることができますね．

好きなだけいじりましょう．

### 独自ドメインを設定

やっぱり自分のドメイン使いたいよねってことで設定しましょうね．

LightsailにはDNS機能があるのですがせっかくなのでRoute53使いましょう．

無料なので．

#### Route53にてネームサーバーの設定

Route53にアクセスしたら**DNS management** の**Get started now** をクリック．

**Created Hosted Zone** をクリックしたらドメインとか入力するところ出るので

**Domain Name** にドメイン

**Comment** に何のドメインかわかるような説明

**Type** はPublic Hosted Zoneのまま

で**Create**.

![f:id:Shinogasa:20180111212225p:plain](https://cdn-ak.f.st-hatena.com/images/fotolife/S/Shinogasa/20180111/20180111212225.png)

そうしたらNS4つとSOA1つが生成されます．

後でNSを使うので4つともメモっておきましょう．

![f:id:Shinogasa:20180111212951p:plain](https://cdn-ak.f.st-hatena.com/images/fotolife/S/Shinogasa/20180111/20180111212951.png)

#### Record Setする

IPとドメインを紐付けますよ．

上部の**Create Record Set** をクリックしたら右に色々出るので

**Name** ：何も入力しない

**Type** ：A - IPv4 address

**Alias** ：No

**TTL (Seconds)** ：300

**Value** ：Lightsailの静的IP

で**Create** ．

wwwありのドメインからwwwなしのドメインに飛ばしたい人は

もう一度**Create Record Set** して

**Name** ：www

**Type** ：CNAME \- Canonical name

**Alias** ：No

**TTL (Seconds)** ：300

**Value** ：独自ドメイン

**Routeing Policy** ：Simple

で**Create** ．

#### お名前.comで設定

お名前.comのドメインNaviにログインして

**ドメイン** →**ドメイン設定** →**DNS関連機能の設定→ネームサーバーの変更**

設定したいドメインにチェックを入れて**他のネームサーバーを利用．**

**1プライマリネームサーバー** ，**2セカンダリネームサーバー** ，．．．

って５つ入力欄出るので上から順にさっき控えたNSを入力．

**最後の「．」は消すこと！**

確認画面へ進むをクリックしたらお名前.comの設定も完了！

ターミナルで

> dig 独自ドメイン

ってやって設定したDNSが表示されたらOK．

最大72時間くらいで独自ドメインにサイトが表示されるようになるはず．

#### 最後の仕上げ

このままだとWordPressのURLはIPのままなのでドメインに変更しましょう．

とりあえずLightsailにSSHで接続．

vimで**wp-config.php** を編集しましょう．

> vim /opt/bitnami/apps/wordpress/htdocs/wp-config.php

してから

> define('WP_SITEURL', 'http://' . $_SERVER['HTTP_HOST'] . '/');  
> define('WP_HOME', 'http://' . $_SERVER['HTTP_HOST'] . '/');

  
ってところを

> define('WP_SITEURL', 'http://自分のドメイン/');  
> define('WP_HOME', 'http://自分のドメイン/');

に変更しましょう．

これで管理画面も自分のドメインになりました！

これにて全て終了！！！！！

おつぽよーーーーーーー！！！！

### 参考にさせていただいた素敵なサイト

非常に参考になりました．ありがとうございます．

[Amazon LightsailでWordpressブログを作ってみる(1)~インスタンス作成、固定IP設定~ | Opvel](https://opvel.com/2017/09/03/lightsail-1-wordpress-blog/)

[お名前.comで取得したドメインをAmazon EC2に紐付ける - Qiita](https://qiita.com/nadonado/items/a7c32c94fef87b7db0d5)

[Bitnami WordPress for AWS Cloud | How To Change The WordPress Domain Name?](https://docs.bitnami.com/aws/apps/wordpress/#how-to-change-the-wordpress-domain-name)
