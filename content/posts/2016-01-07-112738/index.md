---
title: 「RaspberryPiで手作り目覚まし時計！ストップボタン編」をやってみた
date: 2016-01-07 11:27:38
slug: 2016-01-07-112738
draft: False
categories:
  - Raspberry Pi
---

今年もよろしくお願いします． こんな記事見つけて唐突にやってみようと思ったのでチャレンジ． http://deviceplus.jp/hobby/raspberrypi_entry_019/ 

[amazonjs asin="B01CSFZ4JG" locale="JP" title="Raspberry Pi3 Model B ボード＆ケースセット 3ple Decker対応 (Element14版, Clear)-Physical Computing Lab"]

#### ハードウェア

配線 今回はGPIOは25番使用してます． 配線がちゃんとしてるかチェック． GPIOポートの使用開始を宣言． 

> $ echo 25 > /sys/class/gpio/export $ echo in > /sys/class/gpio/gpio25/direction

GPIOポートの値を取得しましょ． 

> $ cat  /sys/class/gpio/gpio25/value

スイッチ押してない時コマンド実行で0，押しながら実行で1が出たらOK． 今回音を鳴らすのでスピーカー準備します． 前の自分の記事参考にして設定しました． http://13.230.11.248/entry/2015/06/19/004452 調べたら使ってるUSBスピーカーが廃盤になってるっぽいですね． こちら後継機っぽいですが動作どうなんでしょう．．． 

[amazonjs asin="B004JTJKX6" locale="JP" title="サンワダイレクト USBスピーカー 小型 クリップ搭載 1.1W パソコンスピーカー 400-SP012"]

確実な方法はイヤホンジャックにスピーカーですね． 

#### プログラム

ただ音鳴らすのもひねりがないので音声流します． 使うソフトはAquesTalkPiというRaspberryPi用ゆっくり． 公式からDLします． [AquesTalk Pi - Raspberry Pi用の音声合成](http://www.a-quest.com/products/aquestalkpi.html) 詳しい使い方はこちらが非常に参考になりました． http://blog-yama.a-quest.com/?eid=970157 とりあえず音を出してみますか． 解答したファイル内にAquesTalkPiというファイルがあるので 実行プログラムのあるフォルダ内に設置しておきます． main.py 

> #coding:utf-8 import os import sys #メイン処理 if __name__ == "__main__": try: message = "hello" os.system('./AquesTalkPi' + message + ' | aplay") except Exception , e: print e , "error"

これで実行したらゆっくりボイスでへろーと喋ってくれるはず． 

> $ python main.py 再生中 WAVE 'stdin' : Signed 16 bit Little Endian, レート 8000Hz, モノラル

mesageを変えれば喋る言葉変えられます． 

#### ストップスイッチ

スイッチ押したら音声が止まるようにしたいっすね． 元記事だと再生用と停止用の2つのプログラム作っていましたが1つでも行けるんじゃないかと思ってチャレンジ． とりあえずこんな感じでどーよと． 20回再生するうちにスイッチ押されたら終了するイメージ． main.py 

> #coding:utf-8 import os import sys #メイン処理 if __name__ == "__main__": try: message = "hello" sum = 0 os.system('echo 25 > /sys/class/gpio/export') os.system('echo in > /sys/class/gpio/gpio25/direction') for num in range(1,20): os.system('./AquesTalkPi' + message + ' | aplay") sum += num if os.system('cat /sys/class/gpio/gpio25/value') == 1 : break except Exception , e: print e , "error"

実行したけどうまく止まってくれないっす． gpioポートのvalueの値を取得できてないっぽいですね． ここで小1時間悩んで「これPythonじゃなくてshellやんけ」という結論に． PythonにGPIOポートの値取得するものあるのになぜかPyhon内にshell記述してました． PythonでGPIOポートの値取得できるので書き直します． 

### 配線

正しい配線はこちら ![](https://lh3.googleusercontent.com/-EmB2mPGjrO8/VnejAB26KHI/AAAAAAAARZs/ZVBvofQ2Wp4/s1024/CameraZOOM-20151221155537035.jpg) 見にくいかもしれませんが24番ポートを使ってます． 

### ソース

Python使いました． 

> #coding:utf-8 import os import sys import RPi.GPIO as GPIO from time import sleep GPIO.setmode(GPIO.BCM) GPIO.setup(25,GPIO.OUT) GPIO.setup(24,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #メイン処理 if __name__ == "__main__": try: message = "hello" #USBスピーカーの設定 必要に応じて #os.system('lsusb') #os.system('sudo alsa unload') #os.system('sudo modprobe snd_usb_audio') while GPIO.input(24) == 0 : os.system('./Voice/aquestalkpi/AquesTalkPi '+ message + ' | aplay') else : print "end" sleep(0.01) except KeybordInterrupt: pass GPIO.cleanup()

GPIOポート使うので sudo つけて実行． うまくいったっぽいですぞ． Pythonで書いたらスッキリした感． 他のやつもPythonで実装してみよ． こちらの本がGPIO周りで非常に参考にさせていただきました． [amazonjs asin="4062578913" locale="JP" title="Raspberry Piで学ぶ電子工作 超小型コンピュータで電子回路を制御する (ブルーバックス)"]
