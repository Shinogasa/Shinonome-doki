---
title: Vagrantにてマウントエラーが出たっぽい話
date: 2015-12-19 10:08:57
slug: 2015-12-19-100857
draft: False
categories:
  - プログラミング
---

前にVagrant導入してました． 久しぶりにいじったらなんかエラーが出ていたので自分用にメモ．  いつもvagrant up しっぱなしだったのでわからなかったのですが， 久しぶりにvagrantを再起動したら下のようなエラーが． 

> Failed to mount folders in Linux guest. This is usually because the "vboxsf" file system is not available. Please verify that the guest additions are properly installed in the guest and can work properly. The command attempted was: mount -t vboxsf -o uid=`id -u vagrant`,gid=`getent group vagrant | cut -d: -f3` vagrant /vagrant mount -t vboxsf -o uid=`id -u vagrant`,gid=`id -g vagrant` vagrant /vagrant The error output from the last command was: /sbin/mount.vboxsf: mounting failed with the error: No such device

ググったら共有フォルダがマウントエラーになってるっぽい． 解決策がQiitaにあったのでありがたく実行． [blogcard url="https://qiita.com/osamu1203/items/10e19c74c912d303ca0b"] vagrant up してもまだエラーが出るぞよ？ 別の方法もチャレンジ． [blogcard url="https://qiita.com/DQNEO/items/2375dd8002a831268cb5"] GuestAdditions入れたはいいけどバージョンあってないから使えねーよみたいなエラーが． 

> GuestAdditions versions on your host (5.0.2) and guest (5.0.6) do not match.

GuestAdditions入れてvagrant up すれば自動でバージョン合わせてくれるみたいなこと書いてたのに変わらん． 再インストールしたりして小１時間悩む． 悩んだ末なんとなくゲストOSでyum updateしてみる 

> sudo yum update

ゲストOSでvagrant reload. なんか色々出た． 

> GuestAdditions versions on your host (5.0.2) and guest (5.0.6) do not match. Loaded plugins: fastestmirror Loading mirror speeds from cached hostfile * base: ftp.riken.jp * extras: ftp.riken.jp * updates: ftp.riken.jp Package kernel-devel-3.10.0-327.3.1.el7.x86_64 already installed and latest version Package gcc-4.8.5-4.el7.x86_64 already installed and latest version Package 1:make-3.82-21.el7.x86_64 already installed and latest version Package 4:perl-5.16.3-286.el7.x86_64 already installed and latest version Package bzip2-1.0.6-13.el7.x86_64 already installed and latest version Nothing to do Copy iso file /Applications/VirtualBox.app/Contents/MacOS/VBoxGuestAdditions.iso into the box /tmp/VBoxGuestAdditions.iso mount: /dev/loop0 is write-protected, mounting read-only Installing Virtualbox Guest Additions 5.0.2 - guest version is 5.0.6 Verifying archive integrity... All good. Uncompressing VirtualBox 5.0.2 Guest Additions for Linux............ VirtualBox Guest Additions installer Removing installed version 5.0.2 of VirtualBox Guest Additions... Removing existing VirtualBox non-DKMS kernel modules[ OK ] Copying additional installer modules ... Installing additional modules ... Removing existing VirtualBox non-DKMS kernel modules[ OK ] Building the VirtualBox Guest Additions kernel modules Building the main Guest Additions module[ OK ] Building the shared folder support module[ OK ] Building the OpenGL support module[FAILED] (Look at /var/log/vboxadd-install.log to find out what went wrong) Doing non-kernel setup of the Guest Additions[ OK ] Installing the Window System drivers Could not find the X.Org or XFree86 Window System, skipping. An error occurred during installation of VirtualBox Guest Additions 5.0.2. Some functionality may not work as intended. In most cases it is OK that the "Window System drivers" installation failed.

なんかいけた？ vagrant vbguest --status したら 

> GuestAdditions 5.0.2 running --- OK.

うまくいってた． 無事エラーもなく起動できるようになりました． 唐突なエラーやめちくりー． 

### 追記

また色々やってたらマウントエラーが出た． 上記試したけどだめだった． 調べたら kernel-devel とかインストールしなくてはならないらしい． とりあえずインストール 

> 
>     [root@vagrant-centos65 ~]# yum install kernel-devel
>     Loaded plugins: fastestmirror
>     Loading mirror speeds from cached hostfile
>     * base: www.ftp.ne.jp
>     * epel: ftp.tsukuba.wide.ad.jp
>     * extras: www.ftp.ne.jp
>     * rpmforge: ftp.riken.jp
>     * updates: www.ftp.ne.jp
>     Setting up Install Process
>     No package kernel-devel available.
>     Error: Nothing to do

そんなパッケージねーよって言われちゃった． 色々調べてたら下記に方法が． [blogcard url="https://utano.jp/entry/2014/11/vagrant_guest_additions_update_error/"] どうやら指定されたカーネルのバージョンじゃないとだめらしい． vagrant upした時に表示されているカーネルを調べてrpmを直接インストールしたらうまく行った． ものぐさだめですね．[amazonjs asin="4873116651" locale="JP" title="実践 Vagrant"]
