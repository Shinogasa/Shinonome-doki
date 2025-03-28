---
title: Dockerで作成したイメージのリポジトリ名とタグ名を変更する
date: 2017-04-18 19:04:00
slug: docker-rename-repo-tag
draft: False
categories:
  - Docker
---

Dockerで作成したコンテナイメージをDockerHubにプッシュしようとしたら下記エラーが出てできなかった． 
    
    
    $ docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    hoge/httpd     ver1.0              54e9a8d65f50        2 days ago          258 MB
    $ docker push hoge/httpd:ver1.0
    The push refers to a repository [docker.io/hoge/httpd]
    09ce67b5172f: Preparing
    5f70bf18a086: Preparing
    8d12f3483b2e: Preparing
    denied: requested access to the resource is denied

どうやらローカルのリポジトリ名とDockerHubのリポジトリ名が一致していないよって言われてるみたい．  [stackoverflow.com](http://stackoverflow.com/questions/41984399/denied-requested-access-to-the-resource-is-denied-docker) 自分のDockerHubのユーザー名がfugaだったのでそちらに変更． 
    
    
    $ docker tag 54e9a8d65f50 fuga/httpd:ver1
    $ docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    fuga/httpd     ver1.0              54e9a8d65f50        2 days ago          258 MB
    hoge/httpd     ver1.0              54e9a8d65f50        2 days ago          258 MB

そしていらなくなったイメージを削除． 
    
    
    $ docker rmi hoge/httpd:ver1.0
    Untagged: hoge/httpd:ver1.0

そしてプッシュ． 
    
    
    $ docker push fuga/httpd
    The push refers to a repository [docker.io/fuga/httpd]
    09ce67b5172f: Pushed
    5f70bf18a086: Pushed
    8d12f3483b2e: Pushed
    ver1.0: digest: sha256:a8484be3b56351f2e2208fb2e60728565a9bb0254da9c41db34a0520274afabe size: 1153

コレでOK． 基本構文は以下の通り． 
    
    
    $docker tag イメージID リポジトリ名:タグ名

### 参考

大変参考になりました．ありがとうございます． http://taker.hatenablog.com/entry/2016/05/04/175021   [amazonjs asin="B015IZT854" locale="JP" title="Docker実践入門――Linuxコンテナ技術の基礎から応用まで"]
