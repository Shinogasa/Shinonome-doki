# Shinonome-doki

this is my blog by Hugo
deploy by GitHub Actions

## Theme

https://github.com/dim0627/hugo_theme_robust

## Usage

### 記事テンプレ

```md
---
title: デレ老人の見たデレステ10thツアー東京公演DAY2
date: 2025-04-28 12:00:00
slug: the-idolmaster-cinderella-girls-starlight-stage-10th-tokyo-day2
draft: False
categories:
  - シンデレラガールズ
  - 日記
---
```

### ショートコード

#### アフィリエイト

```md
{{< affiliate
    title="August Burns Red / Constellations"
    summary=""
    image-url="Amazonから取ってきた画像URL"
    amazon-url="Amazonアフィリエイトリンク"
    rakuten-url="楽天アフィリエイトリンク"
>}}
```

#### ツイート埋込み

```md
{{< tweet id="ツイートid" user="ユーザーid" theme="light" >}}
```

## Build

ローカルで確認

```bash
hugo server -D
```

記事ビルド

```bash
hugo
```

## その他

### 画像変換

```bash
sips -s format jpeg image.heic --out image.jpg
```
