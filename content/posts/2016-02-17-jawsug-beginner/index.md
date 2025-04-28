---
title: JAWS-UG初心者支部に初参加してきた
date: 2016-02-17 19:49:13
slug: 2016-02-17-jawsug-beginner
draft: False
categories:
  - AWS
  - プログラミング
---

### JAWS-UG

以前から興味のあったAWS．

AWSのユーザーグループとしてかなり活発に活動されているJAWS-UG.

その初心者支部があると知って以前から参加してみたかったので参加してきました．

今回は最近発売された「AmazonWebServices実践入門」(通称緑本)の著者の方が登壇されるということでAWS初心者として学んできました．

以下セッションのメモ．

[amazonjs asin="4774176737" locale="JP" title="Amazon Web Services実践入門 (WEB+DB PRESS plus)"] 

### \--東急ハンズのEC2の使い方

**1．EC2の特徴，東急ハンズでの利用例**

  EC2 仮想サーバを必要に応じて調達可能 自由にカスタマイズ

  ハンズネット（ECサイト）

      ハンズメッセ時に大量のアクセス 通常の10倍以上

      その時だけインスタンス立ち上げ

      終わったら落とす

  その他の活用

      POSサーバ

      メールマガジン配信システム

**2．学習方法**

  AWSブログ

      公式

      ソリューションアーキテクトの人書いてるの

      サービスカテゴリごと

      RSS登録して時間があるときに読む

  AWS Black Belt Tech Webiner

      中の人のウェブセミナー

      中の人が作ってるからわかりやすい

      押さえておけば脱初心者

  AWS公式トレーニング

      試験は手を動かして覚えるのが一番

      有料だから補助があったら最高

      Architecting on AWS

          浅く広くサービスを知る

          ソリューションアーキテクトアソシエイト対策

      Advanced Aechtecting on AWS

          更に多くのサービス

  re:Invent

      AWSのお祭り

      セッション，スライド，動画が公開

          新サービス発表とか

**3．まとめ**

  EC2は柔軟で便利

      うまく使えば高い費用対効果

      オンプレ前提のアプリも動く

  学習するにはとにかく使ってみる

      無料枠で十分勉強できる

      EC2から始めるといいかも

### \--SimpleFront 53

**S3**

  オブジェクトストレージ

  めっちゃ耐久性高い

  可用性，SLAも高い

  シンプルで安い

  利用例

      ログの保存

          ログローテート時にSDKやCLI利用

          ライフサイクル使用して財布に優しく

              より安いストレージに移動/アーカイブ

      静的ファイル配信

      静的ウェブサイトホスティング

          安く手間なくウェブサイトの運用

          デフォでSSL/TLS使える

          独自ドメイン使える

  応用例

      静的ウェブサイトホスティング+JS+Cognito

      オブジェクト登録時のイベント発火

          Lamdaで画像のリサイズとか

**Cloud Front**

  便利なCDN

  動的なコンテンツでも使える

  レポート機能が便利

  アクセスログはKinesisで集められてるらしい

  利用例

      CDN:コンテンツデリバリーネットワーク

          キャッシュによるオリジン負荷軽減

          世界中のエッジでレイテンシ低下

          コネクションの最適化

      ウェブサイトのSSL/TLS対応

          cloudfront+S3で最強の静的ウェブサイト

              cmsでHTML生成しているようなサイトで有用

                  （うちの奴ってコレだからいいのかな？

              certificate managerで無料＋更新不要の証明書

      地域に応じたレスポンス geo trageting/registration

          httpヘッダにアクセスされた国を保持

          同一URLで別コンテンツ

      AWS WAFとの統合

          セキュリティ対策

              IPアドレスマッチ

**Route 53**

  安くてたまいらずのDNSサービス

  サーバがオンプレでも使うべき

  注意点

      DNSキャッシュサーバではない

      AWS CLIでの管理は苦行

          簡単な操作ならマネジメントコンソール

          自動化ならAWS SDK

          JSON好きならどうぞ

      使用例

          DNSフェイルオーバー

          荷重ラウンドロビン

              重みに応じてラウンドロビン

          レイテンシベースドロビン

              レイテンシの少ないリージョンに振り分け

**まとめ**

  3サービスとも手間がかからない

  使い方いろいろ

  安い

**[JAWS-UG初心者支部第4回 Simple Front 53](https://www.slideshare.net/matetsu/jawsugbeginner420160216simplefront53 "JAWS-UG初心者支部第4回 Simple Front 53") ** from **[Tetsuya Mase](http://www.slideshare.net/matetsu)**

[www.slideshare.net](http://www.slideshare.net/matetsu/jawsugbeginner420160216simplefront53)

### \--ぎょりと学ぶAWSのBilling+Legal

習うより慣れろ&ggrksがモットー

料金と契約について

**Billing**

  従量課金モデル

  課金対象

      稼働時間，データ量，データ転送量，ディスクI/O

      稼働時間が大体占める

  計算はSIMPLE MONTHLY CALICULATORを使おう

      主要サービスに対応

      ドル計算されるので注意

      チェックボックスで無料枠使うか使わないかを設定

      計算結果は保存できる

  料金は電気代のイメージ

      使った分だけ支払い

      それぞれにあったプランを選択

後半は時間なくてカットされたので下記スライドで

**[Amazon Web Service（AWS）Billingの話_JAWSUG初心者支部(20160216)](https://www.slideshare.net/NagafuchiKyoko/amazon-web-serviceawsbillingjawsug20160216 "Amazon Web Service（AWS）Billingの話_JAWSUG初心者支部\(20160216\)") ** from **[Gyori Nagafuchi](http://www.slideshare.net/NagafuchiKyoko)**

[www.slideshare.net](http://www.slideshare.net/NagafuchiKyoko/amazon-web-serviceawsbillingjawsug20160216)

### 参加してみて

初心者支部だけあって内容が初歩的な部分中心で有りがたかったです． ですが途中ついていけなかった点もあったのでやっぱり触ってみることが大事なんだなと改めて実感しました． LTもありましたがそちらでは失敗談等の経験談を中心に参考になりました． 懇親会にも参加しましたが話してみると皆さん結構ガッツリAWS触ってる方ばかりですね・・・． 「AWS初心者」ではなく「JAWS-UG初心者」という雰囲気もあり，この前「アカウント作ったら$30あげるよ」とAmazonから来て作ったばかりの私には少し肩身が狭いところもありました． ですが色々勉強して話について行けるようになりAWSの話ができるようにならなければといい刺激にもなりました． とりあえず緑本やってみます！ JAWS DAYS参加予定なのでそれまでに一通りやらないと！ [amazonjs asin="4822237443" locale="JP" title="Amazon Web Services 基礎からのネットワーク&サーバー構築 改訂版"] [amazonjs asin="4774179922" locale="JP" title="AWSエキスパート養成読本Amazon Web Servicesに最適化されたアーキテクチャを手に入れる! (Software Design plus)"]
