---
title: Vagrantの勉強を始めた話
date: 2015-10-28 18:37:53
slug: 2015-10-28-183753
draft: False
categories:
  - プログラミング
---

仕事でVagrantを使う必要があったので備忘録． 教材はいつもお世話になってるドットインストール． [blogcard url="https://dotinstall.com/lessons/basic_vagrant"] わかりやすいし1本3分くらいなのでテンポよく学習できる素晴らしいサイト． プレミアム入ろうか考え中です． それと先人の素晴らしい技術者の方々のブログなどを参考にやっていきます． 

### 環境構築

何はともあれVagrant使える環境をば． 必要なもの 

  * [Vagrant](https://www.vagrantup.com/)
  * [Oracle VM VirtualBox](https://www.virtualbox.org/)

公式サイトから自分のOSにあったものをインストール． 会社はWindowsでしたが個人の環境はMacなので両方体験しました． 多分流れはほぼ同じですよね． 

### OSのダウンロード

仮想環境で使いたいOSをダウンロードします． VagrantではOSがBoxという形式で配布されています． 有志の方がいろんなOSを以下のサイトで配布してくれてます． 

  *  [A list of base boxes for Vagrant - Vagrantbox.es](http://www.vagrantbox.es/)

今回はCentOS 7を使おうと思います． 先輩から配布元がchefなら信頼できるの配布してるよというのを聞きchefのCentOS  7を探したのですが先ほどのところには載ってないですね．．． 調べたら配元が別の所になっているようですね． [blogcard url="http://chopschips.net/blog/2015/08/28/chef-vagrant-box-migrate-to-bento/"] 上のブログから情報をいただきBoxをダウンロード． 

> vagrant box add bento/centos-7.1

VertualBoxを選択してしばらく待機． DLできたら以下のコマンドでちゃんとあるか確認． 

> vagrant box list

あったのでOK. 

### 仮想マシンを起動

仮想マシンを設置したいフォルダに移動してコマンド叩いて起動． 

> vagrant up

起動するはずなのですがなんかエラー出ました． 

> Bringing machine 'default' up with 'virtualbox' provider... ==> default: Box 'base' could not be found. Attempting to find and install... default: Box Provider: virtualbox default: Box Version: >= 0 ==> default: Box file was not detected as metadata. Adding it directly... ==> default: Adding box 'base' (v0) for provider: virtualbox default: Downloading: base An error occurred while downloading the remote file. The error message, if any, is reproduced below. Please fix this error and try again.

boxが無いとか言われていますね． よく見たらBoxファイル名がbaseになってるみたいですね． Vagrantファイルの中を見て変更します． 

>  config.vm.box = "base"

を 

>  config.vm.box = "bento/centos-7.1"

に変更しました． ついでにSSHで接続するときのIPの部分もコメントから外してしまいます． 

>   # config.vm.network "private_network", ip: "192.168.33.10"

を 

>   config.vm.network "private_network", ip: "192.168.33.10"

こうする． これで起動すると思うのでもう一度vagrant up. なにやら色々流れて無事起動しました． これでVagrantの第1歩を踏み出すことができました． ドットインストールの＃4くらいまでの内容ですね． これからもっと勉強していきます． [amazonjs asin="B00F418SQ8" locale="JP" title="Vagrant入門ガイド"]
