---
title: Slack for Macでチームの削除が出来なかった
date: 2017-01-25 20:46:00
slug: slack-for-mac-team-remove
draft: False
categories:
  - プログラミング
---

Mac用のSlackでチームを削除してアプリを再起動すると削除したチームが復活するという現象が起きてた． 地味に嫌だったので調べたらなんてこと無く解決したのでメモ. 

### 普通の削除

  1. アプリの左にあるサイドバーで削除したいチームを右クリック
  2. "Remove [Team Name]"と出るのでクリック
  3. チームがアプリから削除される
  4. アプリ再起動で何故か削除したチームが復活してる



### こうすりゃいい

  1. 削除したいチームで一番上のチーム名クリック
  2. 出てきたドロップダウンメニューの“Sign out of [Team Name]”をクリック ![f:id:Shinogasa:20170125202427p:plain:w200](https://cdn-ak.f.st-hatena.com/images/fotolife/S/Shinogasa/20170125/20170125202427.png)
  3. チームがアプリから削除される
  4. アプリ再起動しても復活してない!!

同じ現象起きている方いたらお試しあれ． 

##### 参考元

<http://www.9giantsteps.com/2016/02/04/how-to-remove-slack-teams-from-the-mac-slack-app-sidebar/>

[![](https://images-fe.ssl-images-amazon.com/images/I/51g9K9r7quL._SL160_.jpg)](http://www.amazon.co.jp/exec/obidos/ASIN/4774182389/deltafantom-22/ref=nosim/)

[Slack入門 [ChatOpsによるチーム開発の効率化]](http://www.amazon.co.jp/exec/obidos/ASIN/4774182389/deltafantom-22/ref=nosim/)

posted with [カエレバ](http://kaereba.com)

松下 雅和,小島 泰洋,長瀬 敦史,坂本 卓巳 技術評論社 2016-06-28
