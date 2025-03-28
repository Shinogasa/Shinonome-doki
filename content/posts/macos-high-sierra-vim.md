---
title: macOS High Sierraにしたらvimが使えなくなった件
date: 2017-10-15 19:03:00
slug: macos-high-sierra-vim
draft: False
categories:
  - Mac
---

どうも**しののめ**([@Shinogasa](https://twitter.com/Shinogasa))です. 先日macOS High Sierraにアップデートした際にvimが使えなくなってしまいました． 
    
    
    $ vim
    dyld: Library not loaded: /System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/lib/libruby.2.0.0.dylib
    Referenced from: /usr/local/bin/vim
    Reason: image not found
    Abort trap: 6

こりゃいかんと思い色々調べてたところ下記ブログに解決策が．    ありがとうございます． コマンド実行． 
    
    
    $ brew upgrade vim
    Updating Homebrew...
    ==> Auto-updated Homebrew!
    Updated 1 tap (homebrew/core).
    ==> Updated Formulae
    gomplate
    ---中略---
    1 error generated.
    make[1]: *** [objects/if_python.o] Error 1
    make[1]: *** Waiting for unfinished jobs....
    make: *** [first] Error 2
    READ THIS: https://docs.brew.sh/Troubleshooting.html
    Error: GitHub
    The GitHub credentials in the macOS keychain may be invalid.
    Clear them with:
    printf "protocol=https\nhost=github.com\n" | git credential-osxkeychain erase
    Or create a personal access token:
    https://github.com/settings/tokens/new?scopes=gist,public_repo&description=Homebrew
    and then set the token as: export HOMEBREW_GITHUB_API_TOKEN="your_new_token"

なにやらGitHubのキーチェーンがおかしいっぽい？ とりあえずエラーでググったら下記ページがヒット． [Updating credentials from the OSX Keychain - User Documentation](https://help.github.com/articles/updating-credentials-from-the-osx-keychain/) 説明通り Space+Ctrlで「Keychain Access.app」を検索 ↓ github.comを検索 したらキーチェンがヒットしない． 別のエラーでググったら下記記事がヒット．    git configしてやればエエのじゃな． 
    
    
    $ git config --global credential.helper osxkeychain
    $

何も出ない． とりあえずもう一度upgrade． 
    
    
    $ brew upgrade vim
    ==> Upgrading 1 outdated package, with result:
    vim 8.0.1175
    ==> Upgrading vim --with-lua
    ==> Downloading https://github.com/vim/vim/archive/v8.0.1175.zip
    ---中略---
    if_python.c:67:10: fatal error: 'Python.h' file not found
    #include <Python.h>
    ^~~~~~~~~~
    1 error generated.
    make[1]: *** [objects/if_python.o] Error 1
    make[1]: *** Waiting for unfinished jobs....
    make: *** [first] Error 2
    READ THIS: https://docs.brew.sh/Troubleshooting.html

今度はPython.hが無いとな？ pyenvで変えてるからかしら？ 
    
    
    $ pyenv global system

systemのpythonに変更． もう1度upgradeしてみたけどダメ． 今度は下記のstack overflowの回答を実行． 
    
    
    $brew install python
    Error: python 2.7.11 is already installed
    To upgrade to 2.7.14, run `brew upgrade python`

そりゃpython入ってるもんな，と思ったらバージョン上げれるよって． 上げてみましょう． 
    
    
    $ brew upgrade python
    => Upgrading 1 outdated package, with result:
    python 2.7.14
    ==> Upgrading python
    ==> Installing dependencies for python: gdbm
    ==> Installing python dependency: gdbm
    ==> Downloading https://homebrew.bintray.com/bottles/gdbm-1.13.high_sierra.bottle.tar.gz
    ---中略---
    See: https://docs.brew.sh/Homebrew-and-Python.html
    ==> Summary
    🍺  /usr/local/Cellar/python/2.7.14: 6,344 files, 87.5MB, built in 3 minutes 51 seconds

無事アップグレード出来たっぽい． もう1度vimアップグレードじゃ． 
    
    
    $ brew upgrade vim
    ==> Upgrading 1 outdated package, with result:
    vim 8.0.1175
    ==> Upgrading vim --with-lua
    ==> Downloading https://github.com/vim/vim/archive/v8.0.1175.zip
    Already downloaded: /Users/Nozomi/Library/Caches/Homebrew/vim-8.0.1175.zip
    ==> ./configure --prefix=/usr/local --mandir=/usr/local/Cellar/vim/8.0.1175/share/man --enable-multibyte --with-tlib=ncurses --enable-cscope --enable-terminal --with-compiledby=Ho
    ==> make
    ==> make install prefix=/usr/local/Cellar/vim/8.0.1175 STRIP=/usr/bin/true
    🍺  /usr/local/Cellar/vim/8.0.1175: 1,419 files, 22.7MB, built in 1 minute 50 seconds

無事アップグレードされましたねー． vimコマンドでしっかり起動するようになりました． High Sierraにアップデートしたらその他いろいろアップグレードする必要があるんですね． [amazonjs asin="B00HWLJI3U" locale="JP" title="実践Vim 思考のスピードで編集しよう！ (アスキー書籍)"]
