# Shinonome-doki

Hugo で作っているブログ「シノノメドキ」（https://shinonono.net ）のソース。

- テーマ: [hugo_theme_robust](https://github.com/dim0627/hugo_theme_robust)（git submodule。`themes/robust`）
- 配信: S3 + CloudFront。インフラとデプロイの手順は別リポジトリ `Shinonome-doki-infra` で管理している

## Setup

初回 clone 時、テーマが git submodule のため展開が必要。

```bash
git submodule update --init --recursive
```

Hugo は **Extended 版が必須**。テーマの SCSS は Dart Sass でコンパイルする（libsass は Hugo v0.153.0 で deprecated）。

```bash
brew install hugo dart-sass
hugo version # '+extended' が含まれることを確認
sass --version
```

本番ビルドの Hugo / Dart Sass のバージョンは `Shinonome-doki-infra` の `deploy.yml` で固定している。
ローカルもそれに揃える。

## Usage

### 記事の作成

```bash
hugo new content/posts/<記事のディレクトリ名>/index.md
```

`archetypes/default.md` の雛形から front matter 付きで生成される（`draft: true`）。

### 記事テンプレ

```md
---
title: デレ老人の見たデレステ10thツアー東京公演DAY2
date: 2025-04-28 12:00:00
slug: the-idolmaster-cinderella-girls-starlight-stage-10th-tokyo-day2
draft: False
description: デレステ10thツアー東京公演DAY2の感想。セットリストと印象に残った演出を振り返る。
thumbnail: newgene.JPG
categories:
  - シンデレラガールズ
  - 日記
---
```

| キー | 補足 |
|---|---|
| `slug` | **URL を決める**（`/posts/<slug>/`）。公開後に変えるとリンクが切れる |
| `description` | 検索結果に出る説明文。**全角80〜120文字程度**。未記入だと本文冒頭が自動で使われ、意図した要約にならない |
| `thumbnail` | 一覧・記事上部のサムネイルと OGP 画像。**記事と同じディレクトリ（page bundle）に置き、ファイル名で指定する**。Hugo が縮小・WebP 化して表示する（`static/` の画像は縮小できず、ビルド時に警告が出る）。未指定だと表示は `assets/images/default.jpg`、OGP は `/images/default.png` になる |
| `categories` | 既存のカテゴリ名に揃える |

### 画像の置き場所

記事と同じディレクトリ（page bundle）に置き、本文からは**相対パス**で参照する。

```
content/posts/<記事のディレクトリ名>/
├── index.md
└── photo.jpg     ←  ![](photo.jpg) で参照
```

こうすると、レンダーフック（`layouts/_default/_markup/render-image.html`）が次を行う。
`static/` に置いた画像はこの対象外で、元のサイズのまま配信される。

- 幅1280pxを超える画像を縮小する
- `width` / `height` と `loading="lazy"` を付ける（記事の最初の画像だけは遅延させない）
- スマホで縦に撮った写真（EXIF の向き指示付き）を、正しい向きに回転させる

iPhone の HEIC はそのまま使えないので、JPEG に変換してから置く。

```bash
sips -s format jpeg image.heic --out image.jpg
```

### ショートコード

#### ブログカード

ビルド時にリンク先のタイトルや画像を取得して、カードを表示する。

```md
{{< blogcard "https://www.sakaseru.jp/mina/event/54d62b47f90d4ae0281d7b6809ad78c5" >}}
```

#### 画像（キャプション・リンク付き）

```md
{{< figure
  src="photo.jpg"
  caption="すばらしかったフラスタ"
  link="https://www.sakaseru.jp/mina/event/54d62b47f90d4ae0281d7b6809ad78c5"
  width="400"
>}}
```

`figure` はレンダーフックを通らないので、縮小されない。キャプションが要らなければ `![](photo.jpg)` を使う。

#### ポスト（X）の埋め込み

```md
{{< x id="ポストのID" user="ユーザーID" theme="light" >}}
```

#### YouTube

```md
{{< youtube id="動画ID" loading="lazy" title="動画のタイトル" >}}
```

### アフィリエイト

アフィリエイトリンクは、もしもアフィリエイトに統一している。

- **新しい記事**: もしもの管理画面で「かんたんリンク」の HTML を作り、本文にそのまま貼る
  （`config/_default/config.toml` の `markup.goldmark.renderer.unsafe = true` で HTML を通している）
- **古い記事**: `affiliate` ショートコードが残っている。リンク先は、もしものクリックURLに置き換え済み

```md
{{< affiliate
    title="August Burns Red / Constellations"
    summary=""
    image-url="商品画像のURL"
    amazon-url="もしも経由の Amazon リンク"
    rakuten-url="もしも経由の楽天リンク"
>}}
```

## Build

ローカルで確認（下書きも表示する）

```bash
hugo server -D
```

本番と同じ条件でビルドできるかの確認

```bash
rm -rf resources/ public/ && hugo --minify --logLevel warn
```

ローカルでは `resources/_gen` のキャッシュが使われるため、`sass` が無くてもビルドが通ることがある。
CI にはキャッシュが無いので失敗する。`resources/` を消してからビルドすれば、CI と同じ条件になる。
警告が出たら、本番でも同じ警告が出る。

## Deploy

`main` へ push（PR のマージ）すると、`.github/workflows/trigger_deploy.yml` が
`Shinonome-doki-infra` の deploy ワークフローを起動する。infra 側で Hugo のビルド、S3 への同期、
CloudFront のキャッシュ削除を行う。進み具合は次で確かめられる。

```bash
gh run list -R Shinogasa/Shinonome-doki-infra --limit 3
```

`main` 以外のブランチは、Actions の画面から `Trigger Deploy` を手動で実行し、ブランチ名を指定してデプロイできる。

## 表示速度のための決まり

PageSpeed Insights（モバイル）で 62 点だったものを、2026-11 に 100 点まで上げた。
次のものを足すと、また遅くなるので注意する。

- **外部の CSS・フォント・スクリプトを全ページに読み込まない。** Google Fonts、Font Awesome、AdSense、
  Google アナリティクスは外した。本文はシステムフォント（`config/_default/config.toml` の `fontfamily`）で表示している
- **アイコンは `layouts/partials/icon.html` のインライン SVG を使う。** 新しいアイコンが要るときは、
  Font Awesome Free の SVG をこのファイルに足す
- **サムネイルは `layouts/partials/thumb.html` が縮小・WebP 化した `<img>` で出す。** 背景画像の CSS には戻さない

## テーマの上書き

テーマのファイルは直接編集せず、同じパスで `layouts/` に置いて上書きしている。テーマを更新するときは、
次のファイルとテーマ側の差分を確かめる。

- `layouts/_default/`: `baseof.html`、`list.html`、`single.html`、`summary.html`、`li_sm.html`
- `layouts/partials/`: `author.html`、`meta.html`、`share.html`、`single_meta.html`、`single_json_ld.html`

CSS の追加・上書きは `layouts/partials/custom.css` に書く（`baseof.html` がインラインで埋め込む）。
