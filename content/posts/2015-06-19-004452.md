---
title: 【追記あり】Raspberry Pi2でUSBスピーカーがやっと使えた
date: 2015-06-19 00:44:52
slug: 2015-06-19-004452
draft: False
categories:
  - Raspberry Pi
---

Raspberry Pi2から音を出すにはヘッドホン端子だけかと思ってましたがどうやらUSBスピーカーが使えるらしいです． ノイズが入らないんじゃないかと期待してUSBスピーカーから音を出すため試行錯誤しました．  Raspberry Pi2から音をだして見ようと思いとりあえずヘッドホン端子にイヤホンさしてそこから出すように設定してみた． 
    
    
     amixer cset numid=3 1

一番最後の数字が出力の場所を表してるみたいで，1がヘッドホン端子，2がHDMI，0が自動判別らしい． 今回はヘッドホン端子から出したいので1を選択． いきなり大きな音が出たら耳がやられるので念のため音量調節． 
    
    
    alsamixer

矢印上下で音量変更，Escキーで終了． とりあえず音が出るかテスト． 
    
    
    aplay /usr/share/sounds/alsa/Front_Center.wav

再生してみたらちゃんと流れたもののノイズがひどい． 音楽再生にはちとキツイ． 色々調べてみたらUSBスピーカーがいいと書いてあるのを発見． とりあえず安くて動作確認されてる下のもので試してみた． [amazonjs asin="B004BQ0OGO" locale="JP" title="SANWA SUPPLY USBサウンドバースピーカー MM-SPU5BK"] 

#### \--追記 2016/03/19

上であげているUSBスピーカーがどうやら生産終了してしまっているようですね． 調べてみたら以下のものが後継機のようでした． [amazonjs asin="B004JTJKX6" locale="JP" title="サンワダイレクト USBスピーカー 小型 クリップ搭載 1.1W パソコンスピーカー 400-SP012"] こちら実際に使っていないので動作未確認ですがどなたか確認できた人いらっしゃいましたらコメントいただけるとありがたいです． 近いうちに私の方でも動作確認してみます． USBに挿す前と挿したあとに 
    
    
    lsusb

で表示される内容を比較して増えてたら認識されてます． USBスピーカーをデフォルトにしないと再生されないらしいのでデフォルトに設定しちゃいましょう． 
    
    
    sudo vim /etc/modprorbe.d/alsa-base.conf

この中の真ん中辺りにある 
    
    
    options snd-usb-audio index=-2

を 
    
    
    options snd-usb-audio index=0

に変更． -2を0に変えただけ(コメントアウトでもいいらしい？)． 設定を反映させるために再起動 
    
    
    sudo reboot

が，起動時にスピーカーからポップノイズが出てしまうという謎現象が発生． なんかアンペア足らんよみたいな表示が出てたのでUSBアダプタ変えてみましたが直らず． 起動してから挿してもうまく反映されてなくて音が出ない・・・． 小1時間悩んで探しまわったところ [Raspberry Pi で音を出してみる : sstea備忘録](http://sstea.blog.jp/raspi/sound.html) [sstea.blog.jp](http://sstea.blog.jp/raspi/sound.html) このサイトにアンロードして再ロードすればよろしいと書いてあるではないか． アンロードして再ロード 
    
    
    sudo alsa unload
    
    sudo modprobe snd_usb_audio

反映されてるか確認 
    
    
    cat /proc/asound/cards

ちゃんと一番上にUSBスピーカーがきてた． さっきのサンプルを再生したら音が出たー！ 再起動してノイズが出るなんて思わなかったので非常に困りましたがなんとか音を再生することが出来ました． ヘッドホン端子と違ってノイズなくていいですね． ハイレゾプレイヤー化計画も考えているのでパーツそろえて色々やってみましょ． 

### ーー追記ーー

/boot 内の config.txt の末尾に下記を記載したら起動時にUSBスピーカー挿しっぱなしでも問題なくなりました． 
    
    
    max_usb_current=1

これでいちいち抜いてから起動しなくても良さそう！   [amazonjs asin="B01CSFZ4JG" locale="JP" title="Raspberry Pi3 Model B ボード＆ケースセット 3ple Decker対応 (Element14版, Clear)-Physical Computing Lab"]
