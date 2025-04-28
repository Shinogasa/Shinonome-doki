---
title: HTMLからjQueryを使って配置してあるjsonの読み込み
date: 2016-09-14 20:36:00
slug: jquery-ajax-get-json
draft: False
categories:
  - プログラミング
---

## 時々jsonファイル読み込みたいよね

配置してあるjsonを読み込んでそのデータを使ってhtmlいじったりとかよくありますよね． え？無い？そんな人でもいつかは使うはずだから大丈夫． 

## 手段は2つ

Ajaxメソッドをそのまま使うのと省略メソッドを使う2パターンがありました． どっちも非同期処理なので注意． 

### $.ajax()
    
    
    $.ajax(
    {
    type:'GET',
    url:"sample.json",
    dataType:'json',
    success: function(){
    alert("Ajax");
    },
    error:function(){
    alert('Error');
    }
    });
    

ちょっと書き方が複雑です． `type:`の所を`post`にしたり`dataType`の種類を変更で色々なファイルに対応できるようです． `success:`には読み込み成功時の処理，`error:`には失敗時の処理書いてます． `url:`のところでjsonファイルの場所を指定しているのですが下記のような書き方でもいけます． 
    
    
    $.ajax(
    "sample.json",{
    type:'GET',
    dataType:'json',
    success: function(){
    alert("Ajax");
    },
    error:function(){
    alert('Error');
    }
    });
    

わかりにくいのでしっかりリファレンス読まないとダメですね． <http://api.jquery.com/jquery.ajax/>[api.jquery.com](http://api.jquery.com/jquery.ajax/)

### $.getJSON()
    
    
    $.getJSON("sample.json",function(data){
    alert("getJSON");
    });
    

Ajaxに比べたら非常にシンプルにかけますね． こちらはjsonの取得のみのメソッドのようです． ちなみに同じソース内にAjaxとgetJSON両方記載してみたら **Ajax** のほうが先に実行されていました． Ajaxのほうが実行速度が早いんですかね？ <http://api.jquery.com/jquery.getjson/>[api.jquery.com](http://api.jquery.com/jquery.getjson/)

## ここで詰まった

HTMLからjsでjsonを読み込もうとしたらなぜかうまく読み込んでくれないという事態が発生． 今回のディレクトリ構成は以下のとおり． 

  * index.html `←getjson.js読み込んでる`
  * js 
    * getjson.js `←sample.json読み込んでる`
    * sample.json

HTMLファイルと同じ階層にjsというディレクトリあってその中にjsとjsonファイルを配置していました． `index.html` 内にスクリプトタグで`getjson.js`を読み込んでjsonを読み込むというかたちです． コレで以下のようにjsのソース書いてたらうまく行かなかった 
    
    
    $.getJSON("sample.json",function(data){
    alert("ok");
    $(data.service).each(function(){
    alert("getJSON")
    })
    });
    

色々試行錯誤したら `$.getJSON("js/sample.json",function(data)` って指定してやらなきゃjsonを読み込んでくれませんでした． てっきりjsと同じ階層にjsonあるからそのままで良いと思っていたんですがダメだったようです． html内から読み込んでるから`js/sample.json`じゃないと辿りつけなかったってことかな？ ココらへん分かる方いましたらぜひご教授お願いします.  

[amazonjs asin="4873114683" locale="JP" title="jQueryクックブック"]
