---
title: Djangoチュートリアルの頭でいきなりハマった
date: 2017-01-20 20:33:00
slug: django-tutorial-miss
draft: False
categories:
  - プログラミング
---

[Django](http://d.hatena.ne.jp/keyword/Django)[チュートリアル](http://d.hatena.ne.jp/keyword/%A5%C1%A5%E5%A1%BC%A5%C8%A5%EA%A5%A2%A5%EB)の頭でいきなりハマった  
すっごい単純なところでハマって1時間くらい悩んだので書く

やったのは公式[チュートリアル](http://d.hatena.ne.jp/keyword/%A5%C1%A5%E5%A1%BC%A5%C8%A5%EA%A5%A2%A5%EB)

[はじめての Django アプリ作成、その 1 | Django documentation | Django](https://docs.djangoproject.com/ja/1.9/intro/tutorial01/)

## はじめてのビュー作成

書いてるとおりに進めてビューの作成へ．  
polls/view.pyに下記書いた．

**polls/view.py**
    
    
    from django.http import HttpResponse
    def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

polls/urls.pyに下記書いた.

**polls/urls.py**
    
    
    from django.conf.urls import url
    from . import views
    urlpatterns = [
    url(r'^, views.index, name='index'), ]

そしてmysite/urls.pyに下記作成．

**mysite/urls.py**
    
    
    from django.conf.urls import include, url
    from django.contrib import admin
    urlpatterns = [
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
    ]

そしてサーバー起動！
    
    
    python manage.py runserver

エラー！！！
    
    
    NameError: name 'url' is not defined

なんでや！！！urls.pyあるじゃん！！！って思って1時間ぐらいにらめっこ．  
そうしたらmysite/urls.pyの置く場所を間違っていたという．
    
    
    mysite/
     - manage.py
     - mysite/
      - __init__.py
      - settings.py
      - urls.py ← ◯ 正しくはここに記載
      - wsgi.py
     - polls/
      - __init__.py
      - admin.py
      - apps.py
     - migrations/
      - __init__.py
      - models.py
      - tests.py
      - views.py
      - urls.py ← ☓ 間違って新しく作ってた

ちょっとわかりにくいかもしれませんが公式[チュートリアル](http://d.hatena.ne.jp/keyword/%A5%C1%A5%E5%A1%BC%A5%C8%A5%EA%A5%A2%A5%EB)で`mysite/urls.py` に記載しろよって書いていたので素直に`mysite/urls.py`に記載したのですが実際は`mysite/mysite/urls.py`に記載する必要があったのです．  
**くだらない単純なミス！** でも公式ちょっとわかりにくいよ！

[amazonjs asin="B071S25M33" locale="JP" title="1日で理解するDjango超基礎入門"] 
