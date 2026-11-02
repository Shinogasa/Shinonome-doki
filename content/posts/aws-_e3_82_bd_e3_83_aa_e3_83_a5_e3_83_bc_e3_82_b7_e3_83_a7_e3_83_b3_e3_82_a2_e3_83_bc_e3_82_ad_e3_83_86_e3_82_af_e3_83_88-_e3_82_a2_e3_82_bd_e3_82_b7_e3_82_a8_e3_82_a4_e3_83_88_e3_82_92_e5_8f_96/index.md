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

一番時間を割いたのは対策本を読んで**理解・暗記** すること． 自分は黒本と呼ばれている下記の対策本を2周通して読んで，それぞれの章末についている確認問題解いてみてわからないところを見直してました．

<!-- START MoshimoAffiliateEasyLink -->
<script type="text/javascript">
(function(b,c,f,g,a,d,e){b.MoshimoAffiliateObject=a;
b[a]=b[a]||function(){arguments.currentScript=c.currentScript
||c.scripts[c.scripts.length-2];(b[a].q=b[a].q||[]).push(arguments)};
c.getElementById(a)||(d=c.createElement(f),d.src=g,
d.id=a,e=c.getElementsByTagName("body")[0],e.appendChild(d))})
(window,document,"script","//dn.msmstatic.com/site/cardlink/bundle.js?20220329","msmaflink");
msmaflink({"n":"徹底攻略 AWS認定 ソリューションアーキテクト − アソシエイト教科書 第3版［SAA-C03］対応 徹底攻略シリーズ","b":"インプレス","t":"","d":"https:\/\/m.media-amazon.com","c_p":"","p":["\/images\/I\/51NzhXtma2L._SL500_.jpg"],"u":{"u":"https:\/\/www.amazon.co.jp\/dp\/B0BY7X5DTM","t":"amazon","r_v":""},"v":"2.1","b_l":[{"id":1,"u_tx":"Amazonで見る","u_bc":"#f79256","u_url":"https:\/\/www.amazon.co.jp\/dp\/B0BY7X5DTM","a_id":1052536,"p_id":170,"pl_id":27060,"pc_id":185,"s_n":"amazon","u_so":1},{"id":2,"u_tx":"楽天市場で見る","u_bc":"#f76956","u_url":"https:\/\/search.rakuten.co.jp\/search\/mall\/%E5%BE%B9%E5%BA%95%E6%94%BB%E7%95%A5%20AWS%E8%AA%8D%E5%AE%9A%20%E3%82%BD%E3%83%AA%E3%83%A5%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%82%A2%E3%83%BC%E3%82%AD%E3%83%86%E3%82%AF%E3%83%88%20%E2%88%92%20%E3%82%A2%E3%82%BD%E3%82%B7%E3%82%A8%E3%82%A4%E3%83%88%E6%95%99%E7%A7%91%E6%9B%B8%20%E7%AC%AC3%E7%89%88%EF%BC%BBSAA-C03%EF%BC%BD%E5%AF%BE%E5%BF%9C%20%E5%BE%B9%E5%BA%95%E6%94%BB%E7%95%A5%E3%82%B7%E3%83%AA%E3%83%BC%E3%82%BA\/","a_id":1052522,"p_id":54,"pl_id":27059,"pc_id":54,"s_n":"rakuten","u_so":2},{"id":3,"u_tx":"Yahoo!ショッピングで見る","u_bc":"#66a7ff","u_url":"https:\/\/shopping.yahoo.co.jp\/search?first=1&p=%E5%BE%B9%E5%BA%95%E6%94%BB%E7%95%A5%20AWS%E8%AA%8D%E5%AE%9A%20%E3%82%BD%E3%83%AA%E3%83%A5%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%82%A2%E3%83%BC%E3%82%AD%E3%83%86%E3%82%AF%E3%83%88%20%E2%88%92%20%E3%82%A2%E3%82%BD%E3%82%B7%E3%82%A8%E3%82%A4%E3%83%88%E6%95%99%E7%A7%91%E6%9B%B8%20%E7%AC%AC3%E7%89%88%EF%BC%BBSAA-C03%EF%BC%BD%E5%AF%BE%E5%BF%9C%20%E5%BE%B9%E5%BA%95%E6%94%BB%E7%95%A5%E3%82%B7%E3%83%AA%E3%83%BC%E3%82%BA","a_id":1052554,"p_id":1225,"pl_id":27061,"pc_id":1925,"s_n":"yahoo","u_so":3}],"eid":"8HHXz","s":"s"});
</script>
<div id="msmaflink-8HHXz">リンク</div>
<!-- MoshimoAffiliateEasyLink END -->

重要なところがわかりやすくまとめられていて，章末の問題もあるので理解度チェックもしやすいです． 購入特典で独自の模擬試験がダウンロードできるのが結構ありがたいですね． 受験3日前に解いてみたら半分くらいしか取れなくて，そこから間違った問題を復習して本番に備えました． 

### 模試

これもかなり役に立ちました． 難易度としては 黒本の問題 < AWS模試 < AWS本試験 という感じです． 回答後に正答率は出ますが，各問題の正解不正解は出てきませんので，問題をこっそりスクショしておくのが大事ですね． 本番では似たような問題が出た記憶がありますので，スクショを元に対策本やネットで調べつつ理解していくといいと思います． 

### 実務経験

これはできればという感じですが，やはり実際に手を動かしていたりサービスに触っていたりするとかなり問題のイメージがしやすいです． 実務でなかなかさわれないよって方は下記の紫本で実際に手を動かしてみるとイメージしやすいかと思います． ただ，なかなかのボリュームですので時間に余裕があればという感じですね．

<!-- START MoshimoAffiliateEasyLink -->
<script type="text/javascript">
(function(b,c,f,g,a,d,e){b.MoshimoAffiliateObject=a;
b[a]=b[a]||function(){arguments.currentScript=c.currentScript
||c.scripts[c.scripts.length-2];(b[a].q=b[a].q||[]).push(arguments)};
c.getElementById(a)||(d=c.createElement(f),d.src=g,
d.id=a,e=c.getElementsByTagName("body")[0],e.appendChild(d))})
(window,document,"script","//dn.msmstatic.com/site/cardlink/bundle.js?20220329","msmaflink");
msmaflink({"n":"Amazon Web Services基礎からのネットワーク＆サーバー構築改訂４版","b":"","t":"","d":"https:\/\/m.media-amazon.com","c_p":"","p":["\/images\/I\/51FciS4b1FL._SL500_.jpg"],"u":{"u":"https:\/\/www.amazon.co.jp\/dp\/B0C3L6NC76","t":"amazon","r_v":""},"v":"2.1","b_l":[{"id":1,"u_tx":"Amazonで見る","u_bc":"#f79256","u_url":"https:\/\/www.amazon.co.jp\/dp\/B0C3L6NC76","a_id":1052536,"p_id":170,"pl_id":27060,"pc_id":185,"s_n":"amazon","u_so":1},{"id":2,"u_tx":"楽天市場で見る","u_bc":"#f76956","u_url":"https:\/\/search.rakuten.co.jp\/search\/mall\/Amazon%20Web%20Services%E5%9F%BA%E7%A4%8E%E3%81%8B%E3%82%89%E3%81%AE%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF%EF%BC%86%E3%82%B5%E3%83%BC%E3%83%90%E3%83%BC%E6%A7%8B%E7%AF%89%E6%94%B9%E8%A8%82%EF%BC%94%E7%89%88\/","a_id":1052522,"p_id":54,"pl_id":27059,"pc_id":54,"s_n":"rakuten","u_so":2},{"id":3,"u_tx":"Yahoo!ショッピングで見る","u_bc":"#66a7ff","u_url":"https:\/\/shopping.yahoo.co.jp\/search?first=1&p=Amazon%20Web%20Services%E5%9F%BA%E7%A4%8E%E3%81%8B%E3%82%89%E3%81%AE%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF%EF%BC%86%E3%82%B5%E3%83%BC%E3%83%90%E3%83%BC%E6%A7%8B%E7%AF%89%E6%94%B9%E8%A8%82%EF%BC%94%E7%89%88","a_id":1052554,"p_id":1225,"pl_id":27061,"pc_id":1925,"s_n":"yahoo","u_so":3}],"eid":"gwDlA","s":"s"});
</script>
<div id="msmaflink-gwDlA">リンク</div>
<!-- MoshimoAffiliateEasyLink END -->

## 受験してみて

実際に試験を受けてみてですが，模試や対策本ではみたことの無い問題がたくさん出てきて難しかったです．．． 720点のボーダーで770点でしたので結構ギリギリな感じ． 対策本や模試でやったような問題もちょこちょこ出てきたのですが，見た事ないサービスが出てきたりもしたのでAWS公式のホワイトペーパーを読んだりするのも重要だと思います． 公式の受験ガイドはしっかり確認して対策するのがいいですね． 自分の受けた問題ではやはりVPC周り，ストレージ周りが多めに出てきて，深いところまで問われた印象です． VPCでは**NATゲートウェイやVPCエンドポイントの役割** ，プライベートゲートウェイに置いたDBにインターネットから接続するにはどうしたら実現できるか，のような**構築のベストプラクティス** しっかり理解して置いた方がいいと思います． ストレージでは**S3の種類，Glacierの種類と取り出しスピード** ，**EBSの種類とインスタンスストアとの違い** ，**EFSの詳細** はしっかりと押さえておく必要があると思います． AWS ソリューションアーキテクト アソシエイトはAWS触ってる方ならチャレンジしてみるべきですね． 自分のAWSに関する基礎的な知識の棚卸しにもなりますし，取得したらAWSサミットでは専用ブースに行けたりと特典も色々あり，値段以上の価値になるとは思います． アメリカで持ってると年収1000万とかいう噂もありますのでぜひ取得に向けて頑張ってください． それでは． 

## 追記

書いてる途中にAWSからのメルマガで気がついたのですが，この範囲でのソリューションアーキテクト試験は2月末で終了のようです． https://aws.amazon.com/jp/certification/coming-soon/?sc_channel=em&sc_campaign=Newsletter2020-1.NewsLetter_customer_2016_2017&sc_publisher=aws&sc_medium=em_217664&sc_content=&sc_country=JP&sc_region=JAPN&mkt_tok=eyJpIjoiTnpKbU5qTmxaRE0xT1RabSIsInQiOiI1dFcyQkN4TjZ3amVDMkNRM2hnUlZsM0JRQ0IzMEJkQW1FU2doUDBYTHhBblNNM1FiRUhidWF6djFEQTVxUmc4eGJUS0hPY09LSFJ3XC9udE5kZ0h1dU5laENKS2pkalE3cTB2UE9tWnkzQkFFZE5cL01nTW53U2dMM2k1RE1haG5Zb2d1Q3dUVDFDaStKbzRVQU1iVSsrR1RSRERsR2tScXlrc2h1MVhKXC85Tzg9In0%3D   出題範囲見た感じアーキテクチャのデザインが全てになるようなので，まずは模試で出題傾向を確認しつつ，ホワイトペーパーやブラックベルトでベストプラクティスを押さえておいたほうが良いかと思います． どんな風に変わるのかはわかりませんが，AWSAWS側がサーバーレスを推してきているのでVPCは段々と減ってくるような気もします． 一度受験した方も自分の知識の棚卸しや資格の更新も兼ねて受験をしてみるいい機会かもしれませんね． それでは．
