# Shinonome-doki

this is my blog by Hugo
deploy by GitHub Actions

## Theme

https://github.com/dim0627/hugo_theme_robust

## Setup

初回 clone 時、テーマが git submodule のため展開が必要。

```bash
git submodule update --init --recursive
```

Hugo は **Extended 版が必須**（テーマが SCSS を `toCSS` でコンパイルするため）。

```bash
brew install hugo
hugo version # '+extended' が含まれることを確認
```

## Usage

### 記事の作成

```bash
hugo new content/posts/<記事のディレクトリ名>/index.md
```

`archetypes/default.md` の雛形から front matter 付きで生成される。

### 記事テンプレ

```md
---
title: デレ老人の見たデレステ10thツアー東京公演DAY2
date: 2025-04-28 12:00:00
slug: the-idolmaster-cinderella-girls-starlight-stage-10th-tokyo-day2
draft: False
description: デレステ10thツアー東京公演DAY2の感想。セットリストと印象に残った演出を振り返る。
thumbnail: /posts/frgments-of-the-idolmster-cinderella-girls/newgene.JPG
categories:
  - シンデレラガールズ
  - 日記
---
```

| キー | 補足 |
|---|---|
| `slug` | **URL を決める**（`/posts/<slug>/`）。公開後に変えるとリンクが切れる |
| `description` | 検索結果に出る説明文。**全角80〜120文字程度**。未記入だと本文冒頭が自動で使われ、意図した要約にならない |
| `thumbnail` | OGP 画像。未指定だと `/images/default.png` にフォールバックする |
| `categories` | 既存のカテゴリ名に揃える |

### 画像の置き場所

記事と同じディレクトリ（page bundle）に置き、本文からは**相対パス**で参照する。

```
content/posts/<記事のディレクトリ名>/
├── index.md
└── photo.jpg     ←  ![](photo.jpg) で参照
```

こうすると Hugo が自動でリサイズし、`loading="lazy"` と `width`/`height` を付与する
（`layouts/_default/_markup/render-image.html`）。`static/` に置いた画像はこの対象外。

### ショートコード

#### ブログカード

```md
{{< blogcard "https://www.sakaseru.jp/mina/event/54d62b47f90d4ae0281d7b6809ad78c5" >}}
```

#### 画像

```md
{{< figure
  src="/images/examples/zion-national-park.jpg"
  alt="A photograph of Zion National Park"
  link="https://www.nps.gov/zion/index.htm"
  caption="Zion National Park"
  class="ma0 w-75"
  width="800"
  height="600"
>}}
```

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
{{< x id="ツイートid" user="ユーザーid" theme="light" >}}
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
