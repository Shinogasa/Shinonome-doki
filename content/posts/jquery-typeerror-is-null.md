---
title: "メモ:jQueryでTypeError: $(...) is nullって出た"
date: 2016-09-08 18:37:00
slug: jquery-typeerror-is-null
draft: False
categories:
  - プログラミング
---

## TypeError: $(...) is null

Firebugでウォッチ式にjQueryを書いて要素をいじってたら 

> TypeError: $(...) is null

って怒られた． 

### おしえてGoogle先生

要素の指定はあっていたんだけど何故かエラー出たのでGoogle先生に聞いてみた．  [stackoverflow.com](http://stackoverflow.com/questions/16171681/typeerror-is-null-whats-going-on) どうやら複数のバージョンのjQueryを読み込んでいたりするとコンフリクトが起きる場合があるらしい． あとはうまく読み込めていないとか． 

# 解決方法

[jQueryと他のライブラリのコンフリクトを避ける方法 | HALAWATA.NET](https://www.halawata.net/2011/10/jquery-noconflict/) `$(function)` を `jQuery(function)` にしたらエラー消えた． 根本的な原因はわからなかったけどおそらく他のライブラリとコンフリクトしてたようです． 

## 追記

ついったで下記コードで複数バージョンが共存ができるとの情報を頂きました． `jQuery.noConflict(true)` 誰がどこで使うんだろ． 

[amazonjs asin="B00HE4R9H2" locale="JP" title="jQuery入門道場"]
