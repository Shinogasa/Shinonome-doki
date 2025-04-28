---
title: AWS ソリューションアーキテクト アソシエイトに合格しました
date: 2020-01-28 22:25:51
slug: aws-%e3%82%bd%e3%83%aa%e3%83%a5%e3%83%bc%e3%82%b7%e3%83%a7%e3%83%b3%e3%82%a2%e3%83%bc%e3%82%ad%e3%83%86%e3%82%af%e3%83%88-%e3%82%a2%e3%82%bd%e3%82%b7%e3%82%a8%e3%82%a4%e3%83%88%e3%82%92%e5%8f%96
draft: False
categories:
  - AWS
  - プログラミング
---

こんにちは，しののめ([@Shinogasa](https://twitter.com/Shinogasa))です． 先日AWS ソリューションアーキテクト アソシエイトを受験してきて，無事合格することができました． 自分なりの勉強法をまとめましたので今後受験される方に少しでも参考になれば幸いです． 

## 勉強法

### 対策本

一番時間を割いたのは対策本を読んで**理解・暗記** すること． 自分は黒本と呼ばれている下記の対策本を2周通して読んで，それぞれの章末についている確認問題解いてみてわからないところを見直してました． [kattene] { "image": "https://images-na.ssl-images-amazon.com/images/I/91X-Q%2BaBb1L.jpg", "title": "徹底攻略 AWS認定 ソリューションアーキテクト – アソシエイト教科書 徹底攻略シリーズ", "description": "", "sites": [ { "color": "orange", "url": "https://amzn.to/30X254Q", "label": "Amazon", "main": "true" }, { "color": "red", "url": "//af.moshimo.com/af/c/click?a_id=1052522&p_id=54&pc_id=54&pl_id=616&url=https%3A%2F%2Fitem.rakuten.co.jp%2Fbook%2F15742600%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fbook%2Fi%2F19433294%2F", "label": "楽天" } ] } [/kattene] 重要なところがわかりやすくまとめられていて，章末の問題もあるので理解度チェックもしやすいです． 購入特典で独自の模擬試験がダウンロードできるのが結構ありがたいですね． 受験3日前に解いてみたら半分くらいしか取れなくて，そこから間違った問題を復習して本番に備えました． 

### 模試

これもかなり役に立ちました． 難易度としては 黒本の問題 < AWS模試 < AWS本試験 という感じです． 回答後に正答率は出ますが，各問題の正解不正解は出てきませんので，問題をこっそりスクショしておくのが大事ですね． 本番では似たような問題が出た記憶がありますので，スクショを元に対策本やネットで調べつつ理解していくといいと思います． 

### 実務経験

これはできればという感じですが，やはり実際に手を動かしていたりサービスに触っていたりするとかなり問題のイメージがしやすいです． 実務でなかなかさわれないよって方は下記の紫本で実際に手を動かしてみるとイメージしやすいかと思います． ただ，なかなかのボリュームですので時間に余裕があればという感じですね． [kattene] { "image": "https://images-na.ssl-images-amazon.com/images/I/51Fl-rIvlFL._SX385_BO1,204,203,200_.jpg", "title": "Amazon Web Services 基礎からのネットワーク＆サーバー構築 改訂版", "description": "", "sites": [ { "color": "orange", "url": "https://amzn.to/2GnUVxd", "label": "Amazon", "main": "true" }, { "color": "red", "url": "522&p_id=54&pc_id=54&pl_id=616&url=https%3A%2F%2Fitem.rakuten.co.jp%2Frakutenkobo-ebooks%2F337bdb4bbd8531d4b8205727bf66b2e6%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Frakutenkobo-ebooks%2Fi%2F16324433%2F", "label": "楽天" } ] } [/kattene] 

## 受験してみて

実際に試験を受けてみてですが，模試や対策本ではみたことの無い問題がたくさん出てきて難しかったです．．． 720点のボーダーで770点でしたので結構ギリギリな感じ． 対策本や模試でやったような問題もちょこちょこ出てきたのですが，見た事ないサービスが出てきたりもしたのでAWS公式のホワイトペーパーを読んだりするのも重要だと思います． 公式の受験ガイドはしっかり確認して対策するのがいいですね． 自分の受けた問題ではやはりVPC周り，ストレージ周りが多めに出てきて，深いところまで問われた印象です． VPCでは**NATゲートウェイやVPCエンドポイントの役割** ，プライベートゲートウェイに置いたDBにインターネットから接続するにはどうしたら実現できるか，のような**構築のベストプラクティス** しっかり理解して置いた方がいいと思います． ストレージでは**S3の種類，Glacierの種類と取り出しスピード** ，**EBSの種類とインスタンスストアとの違い** ，**EFSの詳細** はしっかりと押さえておく必要があると思います． AWS ソリューションアーキテクト アソシエイトはAWS触ってる方ならチャレンジしてみるべきですね． 自分のAWSに関する基礎的な知識の棚卸しにもなりますし，取得したらAWSサミットでは専用ブースに行けたりと特典も色々あり，値段以上の価値になるとは思います． アメリカで持ってると年収1000万とかいう噂もありますのでぜひ取得に向けて頑張ってください． それでは． 

## 追記

書いてる途中にAWSからのメルマガで気がついたのですが，この範囲でのソリューションアーキテクト試験は2月末で終了のようです． https://aws.amazon.com/jp/certification/coming-soon/?sc_channel=em&sc_campaign=Newsletter2020-1.NewsLetter_customer_2016_2017&sc_publisher=aws&sc_medium=em_217664&sc_content=&sc_country=JP&sc_region=JAPN&mkt_tok=eyJpIjoiTnpKbU5qTmxaRE0xT1RabSIsInQiOiI1dFcyQkN4TjZ3amVDMkNRM2hnUlZsM0JRQ0IzMEJkQW1FU2doUDBYTHhBblNNM1FiRUhidWF6djFEQTVxUmc4eGJUS0hPY09LSFJ3XC9udE5kZ0h1dU5laENKS2pkalE3cTB2UE9tWnkzQkFFZE5cL01nTW53U2dMM2k1RE1haG5Zb2d1Q3dUVDFDaStKbzRVQU1iVSsrR1RSRERsR2tScXlrc2h1MVhKXC85Tzg9In0%3D   出題範囲見た感じアーキテクチャのデザインが全てになるようなので，まずは模試で出題傾向を確認しつつ，ホワイトペーパーやブラックベルトでベストプラクティスを押さえておいたほうが良いかと思います． どんな風に変わるのかはわかりませんが，AWSAWS側がサーバーレスを推してきているのでVPCは段々と減ってくるような気もします． 一度受験した方も自分の知識の棚卸しや資格の更新も兼ねて受験をしてみるいい機会かもしれませんね． それでは．
