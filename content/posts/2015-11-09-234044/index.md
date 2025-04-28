---
title: MacにMacVimを導入してやったぜ
date: 2015-11-09 23:40:44
slug: 2015-11-09-234044
draft: False
categories:
  - プログラミング
---

コマンドラインでカタカタやるのってエンジニアっぽくていいですよね！ MacにHomebrewでVimインストールしたんですがなんか使いにくい．．． てかこれVimじゃなくてViっぽくね？ ってなったので調べてMacで使いやすいらしいMacVim入れました．   

### MacVim-Kaoriyaを入れる

何はともあれVim入れましょう． 下記リンクから最新版の.dmgファイルをダウンロードしてアプリケーションフォルダに追加． [blogcard url="https://github.com/splhack/macvim-kaoriya"] これでGUIで使えるようにはなりました． でもターミナル上で使いたいので設定していきます． 

### MacVimをコマンドライン上で使えるようにする

ホームディレクトリの.bashrcに下記を追記． 

> alias vi='env LANG=ja_JP.UTF-8 /Applications/MacVim.app/Contents/MacOS/Vim "$@"' alias vim='env_LANG=ja_JP.UTF-8 /Applications/MacVim.app/Contents/MacOS/Vim "$@"'

ターミナル再起動で反映されるはず． 

### 使いやすく設定をする

Vimの設定ファイルに色々追記して使いやすくしましょう． とりあえず設定ファイルを作成するためホームディレクトリで下記を実行． 

> vim .vimrc

この中にターミナル上のVimの設定を書き込みます． 私は最初のブログの方の設定にタブ関係で下記ブログのものを使わせていただいています． [blogcard url="http://d.hatena.ne.jp/tetsuya32/20080709/1215630361"] 

>  "新しい行のインデントを現在行と同じにする set autoindent "バックアップファイルのディレクトリを指定する set backupdir=$HOME/vimbackup "クリップボードをWindowsと連携する set clipboard=unnamed "vi互換をオフする set nocompatible "スワップファイル用のディレクトリを指定する set directory=$HOME/vimbackup "タブの代わりに空白文字を指定する set expandtab "変更中のファイルでも、保存しないで他のファイルを表示する set hidden "インクリメンタルサーチを行う set incsearch "行番号を表示する set number "閉括弧が入力された時、対応する括弧を強調する set showmatch "新しい行を作った時に高度な自動インデントを行う set smarttab " grep検索を設定する set grepformat=%f:%l:%m,%f:%l%m,%f\ \ %l%m,%f set grepprg=grep\ -nh " 検索結果のハイライトをEsc連打でクリアする nnoremap <ESC><ESC> :nohlsearch<CR> " タブを表示するときの幅 set tabstop=4 " タブを挿入するときの幅 set shiftwidth=4 " タブをタブとして扱う(スペースに展開しない) set noexpandtab " set softtabstop=0 "---------- " カラースキーム "---------- colorscheme molokai syntax on

ここまでやったら上書き保存． 最後にバックアップフォルダの設定とカラースキームの設定を． バックアップファイルとスワップファイルの格納フォルダ作ります． ホームディレクトリで 

> mkdir vimbackup

カラースキームの仕上げ． カラースキーム用のフォルダを作成します． 

> mkdir .vim cd .vim mkdir colors

カラースキームはmolokaiがキレイだったのでmolokai使います． 下記よりダウンロード． [molokai - A port of the monokai scheme for TextMate : vim online](http://www.vim.org/scripts/script.php?script_id=2340) ダウンロードしたらファイルを.vimフォルダにファイルを移動． 

> sudo mv ~/Downloads/molokai.vim ~/.vim/colors/molokai.vim

これでOK． ターミナルでVim起動してみて文字に色が付いてれば大成功． これでMacでもVim使えますね． succi0303さん，tetsuya32さん素晴らしいエビデンスをありがとうございました． 非常に助かりました． これで今日からVimマスターだ！ [amazonjs asin="B00HWLJI3U" locale="JP" title="実践Vim 思考のスピードで編集しよう！ (アスキー書籍)"] [amazonjs asin="B00OIDI7SW" locale="JP" title="Vimテクニックバイブル～作業効率をカイゼンする150の技"]
