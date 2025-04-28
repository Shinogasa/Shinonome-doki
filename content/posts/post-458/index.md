---
title: liquibase updateしたらjava.lang.NoClassDefFoundErrorが出た
date: 2018-05-19 17:31:35
slug: post-458
draft: False
categories:
  - プログラミング
---

こんにちは，しののめ(@Shinogasa)です．   お仕事で環境構築しててliquibaseなるものを使う機会がありました． どうやらデータベースリファクタリングツールらしいですね． https://qiita.com/opengl-8080/items/37beac5e210f5363af4b   書いてあった手順書通りに実行したら怒られました． 
    
    
    $ liquibase update 
    java.lang.NoClassDefFoundError: org/slf4j/LoggerFactory 
            at liquibase.logging.core.Slf4JLoggerFactory.getLog(Slf4JLoggerFactory.java:9) 
            at liquibase.logging.LogService.getLog(LogService.java:39) 
            at liquibase.integration.commandline.Main.<clinit>(Main.java:67) 
    Caused by: java.lang.ClassNotFoundException: org.slf4j.LoggerFactory 
            at java.net.URLClassLoader.findClass(Unknown Source) 
            at java.lang.ClassLoader.loadClass(Unknown Source) 
            at sun.misc.Launcher$AppClassLoader.loadClass(Unknown Source) 
            at java.lang.ClassLoader.loadClass(Unknown Source) 
            ... 3 more 
    Exception in thread "main"

  エラー解消するためにいろいろ調べたらslf4jが必要っぽいです． 

  1. [ここ](https://www.slf4j.org/download.html)からダウンロードして解凍．
  2. フォルダ内にある**slf4j-api-1.7.25.jar** を**liquibase-3.5.5/lib** に格納
  3. これでエラー解消！

単純にファイルが足りなかったみたいですね． 下記参考にしました． https://liquibase.jira.com/browse/CORE-3201    

[![](https://images-fe.ssl-images-amazon.com/images/I/51blgdC5j7L._SL160_.jpg)](https://www.amazon.co.jp/exec/obidos/ASIN/1785882872/deltafantom-22/)

[Practical Devops](https://www.amazon.co.jp/exec/obidos/ASIN/1785882872/deltafantom-22/)

posted with [カエレバ](http://kaereba.com)

Joakim Verona Packt Publishing 2016-02-16

[Amazon](https://www.amazon.co.jp/gp/search?keywords=liquibase&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&tag=deltafantom-22)

[楽天市場](https://hb.afl.rakuten.co.jp/hgc/140c65f5.f2d5fda6.140c65f6.51a0545a/?pc=https%3A%2F%2Fsearch.rakuten.co.jp%2Fsearch%2Fmall%2Fliquibase%2F-%2Ff.1-p.1-s.1-sf.0-st.A-v.2%3Fx%3D0%26scid%3Daf_ich_link_urltxt%26m%3Dhttp%3A%2F%2Fm.rakuten.co.jp%2F)
