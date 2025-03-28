---
title: raspberry pi セットアップメモ
date: 2015-08-07 00:10:45
slug: 2015-08-07-001045
draft: False
categories:
  - Raspberry Pi
---

ちょっとraspberry pi のセットアップし直そうと思ってNOOBS入れなおしてみた． とりあえずSDFormatterでフォーマットしてダウンロードしたNOOBSをSDにコピー ラズパイにさしてインストール したら Error creating file system mkfs.fat: warning - lowercase labels might not work probely with DOS or Windows ってエラーが出てインストールできないぞよ．  とりあえずググったらこちらのサイトが出てきて同じエラーの状態でした． [ヤスダ式仕事日記: Raspberry Pi 2 のセットアップでエラー](http://blog.yuizi.com/2015/06/rapsberry-pi-2.html) どうやらフォーマットのオプションの指定が間違っているようでした． 上書きフォーマット，論理サイズ調整ONにして再フォーマット． 自分の前に買ってたラズパイの本にもよく見たらフォーマットのオプションしっかり書いとるやないかーい． ちゃんと読みましょう． ちなみに買った本は下のやつで結構詳しく載ってて後半はネタが多くて使えますよ． フォーマットが長いので続きはまたあとで． [amazonjs asin="480071172X" locale="JP" title="これ1冊でできる! ラズベリー・パイ 超入門 改訂第4版 Raspberry Pi 1+/2/3/Zero/Zero W対応"]
