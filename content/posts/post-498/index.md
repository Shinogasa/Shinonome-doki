---
title: MEMO：Javaでネストされているハッシュデータの取得
date: 2018-06-07 22:26:42
slug: post-498
draft: False
categories:
  - プログラミング
---

最近Javaが嫌いから少し嫌いにステップアップしたしののめ([@Shinogasa](https://twitter.com/Shinogasa))です．   ネストされたハッシュデータを取得するのに手間取ったのでメモ．   こんな感じのJSONが投げられてきた 
    
    
    { 
      "hoge": "fuga", 
      "call":{ 
        "yeah": "tiger", 
        "fivo": "wiper" 
      } 
    }

  これからネスト内のデータを取得したかった．  
    
    
    Public void catch_data(HashMap<String, Object> info) { 
      //fugaを取りたいとき 
      String get_fuga = (String) info.get("hoge"); 
      log.debug("get_fuga : {}",get_fuga); //get_fuga : fuga 
    
    
      //tigerを取りたいとき 
      HashMap<String, Object> get_call = (HashMap<String, Object> info.get("call"); 
      String get_tiger = (String) get_call.get("yeah"); 
      log.debug("get_tiger : {}",get_tiger); //get_tiger : tiger 
    
      //1行でtigerを取りたいとき 
      String get_tiger1 = (String) ((HashMap<String, Object>) info.get("call")).get("yeah"); 
      log.debug("get_tiger1 : {}",get_tiger1); //get_tiger1 : tiger 
    
    }

  単純に要素に対して2回getしてやったら良いだけなのに結構悩みました． 難しいですね．  

### 参考

https://qiita.com/DQMerA/items/965cd6462e1795e0d1a3  

[![](https://images-fe.ssl-images-amazon.com/images/I/51B0H%2BURtOL._SL160_.jpg)](https://www.amazon.co.jp/exec/obidos/ASIN/4844339931/deltafantom-22/)

[徹底攻略 Java SE 8 Silver 問題集[1Z0-808]対応](https://www.amazon.co.jp/exec/obidos/ASIN/4844339931/deltafantom-22/)

posted with [カエレバ](https://kaereba.com)

志賀 澄人 インプレス 2016-01-18

[Amazon](https://www.amazon.co.jp/gp/search?keywords=Java&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&tag=deltafantom-22)

[楽天市場](https://hb.afl.rakuten.co.jp/hgc/140c65f5.f2d5fda6.140c65f6.51a0545a/?pc=https%3A%2F%2Fsearch.rakuten.co.jp%2Fsearch%2Fmall%2FJava%2F-%2Ff.1-p.1-s.1-sf.0-st.A-v.2%3Fx%3D0%26scid%3Daf_ich_link_urltxt%26m%3Dhttp%3A%2F%2Fm.rakuten.co.jp%2F)
