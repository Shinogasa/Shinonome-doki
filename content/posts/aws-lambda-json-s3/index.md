---
title: LambdaからS3にあるjsonファイルを取得 node.js編
date: 2016-08-25 18:31:00
slug: aws-lambda-json-s3
draft: False
categories:
  - プログラミング
---

仕事でAWS Lambdaを使うことになって苦戦してます．  
LambdaからS3にアップロードされているjsonファイルを取得するやつ．  
結構単純なんですがAWS触っていなかったせいで悩んじゃいました．  
以下ソース．
    
    
    var aws = require('aws-sdk');
    aws.config.region = 'ap-northeast-1';
    var bucket = 'bucketName';
    var s3 = new aws.S3();
    
    exports.handler = function(event, context) {
       
        var params = {
            Bucket: bucket,
            Key: 'sample.json'
        };
        s3.getObject(params, function(err, data) {
            if (err) {
                console.log(err, err.stack);
            } else {
                var object = JSON.parse(data.Body.toString());
                console.log(object);
            }
        });
    }

bucketNameはファイルの配置されているバケット名，Keyはそのファイルのパス(ディレクトリ直下ならそのまま)という感じです．  
テスト実行して

> Task timed out after 3.00 seconds

って出たらタイムアウトまでの時間を伸ばすとうまくいくはず．  
こう見ると単純ですね.

参考にさせていただいたサイト  
ほぼほぼこちらのソースです．ありがとうございました  
[S3上のjsonをnode.jsで読み込む | ハックノート](http://hacknote.jp/archives/15016/)

[Task timed out after 3.00 secondsの対処法 | ハックノート](http://hacknote.jp/archives/11625/)

[はてなブログにソースコードを貼り付ける方法 - くりにっき](http://sue445.hatenablog.com/entry/2012/11/18/223809)

この本分厚いですが基礎的なところ抑えられててよかったです．

<!-- START MoshimoAffiliateEasyLink -->
<script type="text/javascript">
(function(b,c,f,g,a,d,e){b.MoshimoAffiliateObject=a;
b[a]=b[a]||function(){arguments.currentScript=c.currentScript
||c.scripts[c.scripts.length-2];(b[a].q=b[a].q||[]).push(arguments)};
c.getElementById(a)||(d=c.createElement(f),d.src=g,
d.id=a,e=c.getElementsByTagName("body")[0],e.appendChild(d))})
(window,document,"script","//dn.msmstatic.com/site/cardlink/bundle.js?20220329","msmaflink");
msmaflink({"n":"AWS Lambda実践ガイド 第2版 impress top gearシリーズ","b":"インプレス","t":"","d":"https:\/\/m.media-amazon.com","c_p":"","p":["\/images\/I\/51vlB3JskRL._SL500_.jpg"],"u":{"u":"https:\/\/www.amazon.co.jp\/dp\/B09TVG5H17","t":"amazon","r_v":""},"v":"2.1","b_l":[{"id":1,"u_tx":"Amazonで見る","u_bc":"#f79256","u_url":"https:\/\/www.amazon.co.jp\/dp\/B09TVG5H17","a_id":1052536,"p_id":170,"pl_id":27060,"pc_id":185,"s_n":"amazon","u_so":1},{"id":2,"u_tx":"楽天市場で見る","u_bc":"#f76956","u_url":"https:\/\/search.rakuten.co.jp\/search\/mall\/AWS%20Lambda%E5%AE%9F%E8%B7%B5%E3%82%AC%E3%82%A4%E3%83%89%20%E7%AC%AC2%E7%89%88%20impress%20top%20gear%E3%82%B7%E3%83%AA%E3%83%BC%E3%82%BA\/","a_id":1052522,"p_id":54,"pl_id":27059,"pc_id":54,"s_n":"rakuten","u_so":2},{"id":3,"u_tx":"Yahoo!ショッピングで見る","u_bc":"#66a7ff","u_url":"https:\/\/shopping.yahoo.co.jp\/search?first=1&p=AWS%20Lambda%E5%AE%9F%E8%B7%B5%E3%82%AC%E3%82%A4%E3%83%89%20%E7%AC%AC2%E7%89%88%20impress%20top%20gear%E3%82%B7%E3%83%AA%E3%83%BC%E3%82%BA","a_id":1052554,"p_id":1225,"pl_id":27061,"pc_id":1925,"s_n":"yahoo","u_so":3}],"eid":"ixb8s","s":"s"});
</script>
<div id="msmaflink-ixb8s">リンク</div>
<!-- MoshimoAffiliateEasyLink END -->

