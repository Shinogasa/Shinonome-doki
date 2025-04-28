---
title: CloudFormationのMappingsでListを使いたかった
date: 2020-10-14 23:24:17
slug: cloudformation-mapping-list
draft: False
categories:
  - AWS
  - プログラミング
---

CloudFormationのテンプレートをゴリゴリ書いていて，Mappingsの箇所でListを使ったらエラーでスタックがコケてしまった．  
公式ドキュメントにはList使えるよって書いていたので色々試行錯誤したがうまく行かなかった．  
無理やり解決させた方法の備忘録．

## 概要

  * Dev,QA環境があるアカウントとProd環境のあるアカウントを分けている
  * テンプレートは共通
  * スタックのデプロイ時にパラメータで環境を渡してリソースを切り替え
  * 諸事情によりKMSのARNを複数渡す必要があった
  * 環境により渡すArnが異なるのでMappingsにList形式でArnを記載した



## うまくいかなかったソース

https://github.com/Shinogasa/cloudformation-mapping-list-test/blob/main/template_ng.yml 

MappingsのところへList形式にてKMSのArnを複数記載．  
公式ドキュメントにも「値は `String` または `List` タイプです」と記載があったので使えるもんだと思っていた．

https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/mappings-section-structure.html 

cloudformation deproyにてスタック作成，execution-stackにて実行したところ  
**Syntax errors in policy. (Service: AmazonIdentityManagement; Status Code: 400; Error Code: MalformedPolicyDocument; Request ID: hoge-fuga-poyo-piyo; Proxy: null)**  
でCREATE_FAILED．

## うまくいったパターン

どうにかしてできないもんかと試行錯誤した結果，非常に泥臭くソースのメンテナンス性が悪い方法で成功した．

https://github.com/Shinogasa/cloudformation-mapping-list-test/blob/main/template_ok.yml 

結局List形式は使わずそれぞれのArnを変数に入れる羽目に．  
これじゃあKeyが追加になった場合や環境が追加になった際に非常にメンテがめんどくさい．

カンマで区切ればいけるよって海外の質問サイトに書いていたのでやってみたが，結果は変わらず失敗．

https://serverfault.com/questions/844559/can-findinmap-return-a-list 

なにかいい方法はないものか．  
今後解決策を見つけたら追記予定．

リンク
