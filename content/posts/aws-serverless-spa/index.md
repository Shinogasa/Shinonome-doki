---
title: サーバーレスシングルページアプリケーションやってみる(メモ)
date: 2017-07-18 21:33:00
slug: aws-serverless-spa
draft: False
categories:
  - AWS
  - プログラミング
---

みんな大好きオライリー [amazonjs asin="4873118069" locale="JP" title="サーバーレスシングルページアプリケーション ―S3、AWS Lambda、API Gateway、DynamoDB、Cognitoで構築するスケーラブルなWebサービス"] 初っ端から躓いたのでメモ 

### 1.3.2 S3のバケットを作成する
    
    
    $ ./sspa create_bucket learnjs.hogehoge.com
    Please specify a bucket name

なんでバケット作れないんだろ？ S3のバケット名は全ユーザーでユニークなもの付けなきゃいけないから名前変えたのに． 軽く調べたけどそれっぽい回答が見つからなかったのでcliのコマンド普通に打って作成． 
    
    
    $ aws s3api create-bucket --bucket learnjs.hogehoge.com --profile admin
    {
    "Location": "/learnjs.shinonome.com"
    }

無事作成できました． `--profile admin`は複数IAMユーザーある時に指定するために使用． コレだけだとホスティングされないのでコンソールからStatic website hosting を有効にしてあげてください． 発行されたエンドポイントにアクセスするとアプリが表示されるはず． やっぱり[リファレンス](http://docs.aws.amazon.com/cli/latest/reference/s3api/create-bucket.html)見るのが速い． 最近プログラマからWebディレクターにジョブチェンジしかけてるからお勉強しなきゃ．
