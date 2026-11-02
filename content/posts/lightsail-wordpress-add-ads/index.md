---
title: Lightsailで構築したWordpressにads.txtを追加する
date: 2020-03-29 20:36:50
slug: lightsail-wordpress-add-ads
draft: False
categories:
  - AWS
  - プログラミング
---

こんにちは，しののめ(@Shinogasa)です．

このサイトはアドセンスを入れて広告表示をしているのですが，最近アドセンスの管理画面を見ると

> 要注意 - 収益に重大な影響が出ないよう、ads.txt ファイルの問題を修正してください。

と表示が出ていました．

調べてみるとads.txtの設置は推奨であり必須ではないようですが，この先突然方針が変わるということがあるかもしれませんので安全のために設置しておくことにします．

## 設置場所

肝心の設置場所は公式によるとドメインの直下に置くことになってるようです．

https://support.google.com/adsense/answer/7532444?hl=ja 

LightsailでWordpressを建てた場合は下記に設置したらOKなようです．
    
    
    ~/apps/wordpress/htdocs/ads.txt 

  
LightsailではコンソールからアップロードすることができないのでSCPコマンドを使ってターミナルでアップロードしてあげましょう．
    
    
    ❯ scp -i <Your SSH Key> ads.txt bitnami@<Your Domain>:~/apps/wordpress/htdocs/ads.txt 

  
アップロードが完了しましたら https://自分のドメイン/ads.txt へアクセスしてads.txtが表示されたら完了です．

アドセンスのクローラがクロールするまで要注意の警告表示は消えないみたいなので気長に待ちましょう．  
数日程度でクロールされるようです．

### 参考

https://www.iscle.com/web-it/g-drive/adsense/ads-txt-keikoku.html 

https://gloria.cool/blog/20190611-adsense-adstxt/

<!-- START MoshimoAffiliateEasyLink -->
<script type="text/javascript">
(function(b,c,f,g,a,d,e){b.MoshimoAffiliateObject=a;
b[a]=b[a]||function(){arguments.currentScript=c.currentScript
||c.scripts[c.scripts.length-2];(b[a].q=b[a].q||[]).push(arguments)};
c.getElementById(a)||(d=c.createElement(f),d.src=g,
d.id=a,e=c.getElementsByTagName("body")[0],e.appendChild(d))})
(window,document,"script","//dn.msmstatic.com/site/cardlink/bundle.js?20220329","msmaflink");
msmaflink({"n":"Google AdSense マネタイズの教科書［完全版］","b":"","t":"","d":"https:\/\/m.media-amazon.com","c_p":"","p":["\/images\/I\/51ZNK1VPaRL._SL500_.jpg"],"u":{"u":"https:\/\/www.amazon.co.jp\/dp\/B07RM59DFY","t":"amazon","r_v":""},"v":"2.1","b_l":[{"id":1,"u_tx":"Amazonで見る","u_bc":"#f79256","u_url":"https:\/\/www.amazon.co.jp\/dp\/B07RM59DFY","a_id":1052536,"p_id":170,"pl_id":27060,"pc_id":185,"s_n":"amazon","u_so":1},{"id":2,"u_tx":"楽天市場で見る","u_bc":"#f76956","u_url":"https:\/\/search.rakuten.co.jp\/search\/mall\/Google%20AdSense%20%E3%83%9E%E3%83%8D%E3%82%BF%E3%82%A4%E3%82%BA%E3%81%AE%E6%95%99%E7%A7%91%E6%9B%B8%EF%BC%BB%E5%AE%8C%E5%85%A8%E7%89%88%EF%BC%BD\/","a_id":1052522,"p_id":54,"pl_id":27059,"pc_id":54,"s_n":"rakuten","u_so":2},{"id":3,"u_tx":"Yahoo!ショッピングで見る","u_bc":"#66a7ff","u_url":"https:\/\/shopping.yahoo.co.jp\/search?first=1&p=Google%20AdSense%20%E3%83%9E%E3%83%8D%E3%82%BF%E3%82%A4%E3%82%BA%E3%81%AE%E6%95%99%E7%A7%91%E6%9B%B8%EF%BC%BB%E5%AE%8C%E5%85%A8%E7%89%88%EF%BC%BD","a_id":1052554,"p_id":1225,"pl_id":27061,"pc_id":1925,"s_n":"yahoo","u_so":3}],"eid":"Tiuxz","s":"s"});
</script>
<div id="msmaflink-Tiuxz">リンク</div>
<!-- MoshimoAffiliateEasyLink END -->

