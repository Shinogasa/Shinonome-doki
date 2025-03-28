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

[kattene] { "image": "https://images-na.ssl-images-amazon.com/images/I/41Do-5YqjQL._SX351_BO1,204,203,200_.jpg", "title": "Google AdSense マネタイズの教科書[完全版]", "sites": [ { "color": "orange", "url": "https://amzn.to/2JpuZTb", "label": "Amazon", "main": "true" }, { "color": "blue", "url": "https://amzn.to/2Uphjhi", "label": "Kindle" }, { "color": "red", "url": "https://hb.afl.rakuten.co.jp/ichiba/18bf1b7c.65602340.18bf1b7d.9c7f8714/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fbook%2F15659075%2F&link_type=text&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJ0ZXh0Iiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjB9", "label": "楽天" } ] } [/kattene] 
