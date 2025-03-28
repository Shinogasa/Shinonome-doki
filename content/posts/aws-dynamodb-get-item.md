---
title: DynamoDBのテーブルから特定のアイテムを取得する
date: 2017-02-22 19:32:00
slug: aws-dynamodb-get-item
draft: False
categories:
  - AWS
  - プログラミング
---

## DynamoDB

皆さんご存知AmazonWebServicesの提供しているNoSQLマネージドサービス． Lambdaでサーバーレスの外形監視ツールを作成していて，ステータスコード保存のためにDynamoDBを採用したら値の取得に癖があって結構詰まったので自分用にメモ． 

## コンソール

### テーブル

値を入れているテーブルはこんなかんじ． ![f:id:Shinogasa:20170222155639p:plain:w500](https://cdn-ak.f.st-hatena.com/images/fotolife/S/Shinogasa/20170222/20170222155639.png) ツリー形式だとこんな感じ 
    
    
    {
    "GitHub": "200",
    "Myblog": "200",
    "Time": "2017/2/22  14:52:00",
    "Twitter": "200"
    }
    

## 実装

ブラウザ上で取得したデータを表示したかったのでJavaScriptです． html側かJSのソース内でaws-sdkを読み込んでいないとDynamo使えません． また，今回は直接DyanmoにアクセスするためにAPI GatewayではなくCognitoを使っています． ソースがスパゲッティ気味なのはご愛嬌． 

### ソース

**getFromDynamo.js**
    
    
    //Cognito設定
    AWS.config.region = 'ap-northeast-1';
    AWS.config.credentials = new AWS.CognitoIdentityCredentials({IdentityPoolId: Cognitoから持ってきたIDを入れる});
    AWS.config.credentials.get(function(err) {
    if (!err) {
    console.log('Cognito Identify Id: ' + AWS.config.credentials.identityId);
    }
    });
    const db = new AWS.DynamoDB.DocumentClient();
    //DynamoDBの設定
    const table = "TestTable";
    const keys = "2017/2/22 14:00:00";
    const param = {
    TableName : table,　
    KeyConditionExpression: '#ct = :val',
    ExpressionAttributeNames:{
    "#ct": "Time"
    },
    ExpressionAttributeValues:{
    ":val": keys
    }
    };
    //Dynamoからデータ取得
    function getData(keys){
    console.log('2 inside dynamodata')
    return new Promise(function(resolve,reject){
    db.query(keys,function(err,data){
    if(err){
    console.error('エラーですね:' + err);
    reject(err);
    } else {
    const jsonData = JSON.stringify(data,null,4);
    console.log('成功したみたい:' + jsonData);
    /*
                    成功したみたい:{
                        "Items": [
                            {
                                "Twitter": 200,
                                "MyBlog": 200,
                                "Time": "2017/2/22 14:00:00",
                                "GitHub": 200
                             }
                         ],
                         "Count": 1,
                         "ScannedCount": 1
                     }
    */
    resolve(data);
    }
    });
    });
    }
    //実行
    getData(param)
    .then(function(result){
    console.log(result);
    //時々返ってきたjsonがそのまま使えない時があるのでJSON.paeseしてやる
    //const jsonItems = JSON.parse(result);
    console.log(result.Items[0].MyBlog);
    //200
    });
    

### Cognito

認証のやつ． ぶっちゃけそこまで理解していない．難しい． コレを入れてるとセキュアにAWSのサービスにアクセスできるらしいけどしっかり調べていないので今後の課題． 最上段に設定してあるCognitoのIdentityPoolIDは下記から持ってくる． Cognito -> Manage Federated Identities -> 作成してあるIdentity pool選択 (Identyty poolが無い場合はCreate new identity poolから作る) -> Sample code -> Get AWS Credentials ![f:id:Shinogasa:20170222160907p:plain:w500](https://cdn-ak.f.st-hatena.com/images/fotolife/S/Shinogasa/20170222/20170222160907.png)

### DynamoDBまわり

DynamoDBを使うには`AWS.DynamoDB`で大丈夫なのですがそのままだと非常に使いにくいので [AWS.DynamoDB.DocumentClient](http://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/DynamoDB/DocumentClient.html)を使っております. 普通に使うと色々指定が多くて面倒なところを色々簡単にしてくれる素敵なクラス． 詳しくは公式ドキュメントで. 

#### パラメータ

パラメータの指定も結構癖があって値をそのまま書けず，一度プレースホルダーに書いてやる必要があるみたい． 

  * TableName - テーブル名
  * KeyConditionExpression - プライマリキーでの検索定義
  * ExpressionAttributeNames - 属性名のプレースホルダー
  * ExpressionAttributeValues - 値のプレースホルダー

今回はqueryで検索していますがscanでも検索できます． queryだとプライマリキーの指定が必須になります． scanだとプライマリキーの指定は必要ないみたいですが，テーブルをすべてスキャンなのでqueryより時間がかかるのかな？ 状況に応じて使い分けしていく必要がありそう． 

#### 子要素へアクセス

JSONで返ってきているのでドットつなぎで指定してやればOK． ただし返ってきたItemが１つでも `result.Items[0].MyBlog` と指定してやらねばundefindって怒られるので注意. 

### その他

今回はコメントアウトして使用していないのですが， 私の組んでいたプログラムでは返ってきた値をJSON.parseしてやらないと うまく子要素までアクセス出来ないということがありました． 返ってきた値を別の関数に渡したりしていたので渡す際にJSON形式から変わってしまったのかなと． 意外とDynamoDBに関する情報の殆どが公式ドキュメントという中， 素晴らしき先人たちの資料によってなんとかDynamoで要素を取得できました． NoSQLってなかなか難しいですね． あとJSの非同期がすごい難しいです. Promise.thenしまくりですよ．．．． 

### 参考

[Amazon DynamoDB 入門ガイド](http://docs.aws.amazon.com/ja_jp/amazondynamodb/latest/gettingstartedguide/GettingStarted.Js.04.html) [AWS SDK for JavaScript](http://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/DynamoDB.html#query-property) [Node.js+Dynamo DBでレコードを検索する](http://tech.sanwasystem.com/entry/2016/01/20/143533) [AWS LambdaからDynamoDBをQueryする](http://takamints.hatenablog.jp/entry/2016/02/25/query-aws-dynamodb-by-aws-lambda-function) [amazonjs asin="B07143JTD9" locale="JP" title="RDB技術者のためのNoSQLガイド"] [amazonjs asin="4897978874" locale="JP" title="NOSQLの基礎知識 (ビッグデータを活かすデータベース技術)"]
