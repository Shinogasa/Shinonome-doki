# Backlog

2026-08-06 の監査で洗い出した課題。すべてビルド済み生成物（`public/`）の実測に基づく。
着手するものは `tasks/todo.md` へ移して展開する。完了したらここから消す（履歴は git に残る）。

**P1〜P3 は 2026-08-06 に対応済み**（詳細は `tasks/todo.md` のレビュー参照）。以下は結果の記録。

---

## P1: 実害が出ている 【対応済み】

### og:image が存在しないファイルを指していた（139/142記事）

`static/images/default.png` `default.jpg` `logo.png` `favicon.ico` を新規作成して解消。
夜明けモチーフの OGP 画像（1200x630）。

### 参照先が存在しない画像が他に2つあった

`logo.png`（apple-touch-icon）・favicon とも上記で作成済み。

---

## P2: 修正が軽く効果が確実 【対応済み】

### `<html>` に lang 属性が無かった

`baseof.html` に `<html lang="{{ .Site.Language.Locale }}">` を追加（`.LanguageCode` は
Hugo 0.158 で deprecated のため `.Locale` を使用）。

### 画像に `loading="lazy"` と `width`/`height` が無かった

`layouts/_default/_markup/render-image.html` を新規作成。page bundle 同梱の画像（記事内で
実体を持つもの）には `.Resize` で最大幅 1280px に縮小した上で `width`/`height` を付与、
先頭画像のみ `loading="eager" fetchpriority="high"`、以降は `loading="lazy"`。
`static/` 配置・外部URL の画像は寸法を取得できないため lazy 属性のみ付与。

### Hugo の画像処理が未使用だった

上記レンダーフックで page bundle 画像（13枚）が処理対象になった。`static/` 配置の画像
（12記事、WordPress 由来）は Hugo のリソースパイプラインの対象外のため未対応 → P4 へ。

### Google Fonts に `display=swap` が無かった

`config/_default/config.toml` の `googlefonts` に追加済み。

### `profile.jpeg` が 339KB だった

表示サイズ（6rem=96px、Retina考慮192px）に合わせて 1500x1500 → 192x192 にリサイズ、14KBに削減。

---

## P3: セキュリティ・ハードニング 【対応済み】

### 外部CDNアセットに SRI（integrity）が無かった

FontAwesome に実測ハッシュで `integrity` + `crossorigin` + `referrerpolicy` を付与。
highlight.js は下記の理由で削除したため SRI 対応は不要になった。
`fonts.googleapis.com` は動的CSSのため引き続き SRI 不可（対象外）。

### highlight.js が 10.0.0（2020年）で API が deprecated だった

**`enableHighlight` の仕組み自体を削除。** Chroma によるビルド時ハイライトが実際に機能して
いることを確認済み（記事に `style="color:#66d9ef"` 等のインラインカラー77箇所を実測）。
`baseof.html` から highlight.js の `<link>` `<script>` と `config.toml` の
`enableHighlight = true` を除去。CDN依存が1本減り、JSの実行が無くなった。

### GitHub Actions の権限が未宣言だった

`permissions: {}` を追加。`repository-dispatch` を `@v2` → `@v4.0.1`（SHA固定）へ更新。
v2→v4 は依存更新のみで入出力インターフェースの破壊的変更は無いことを changelog で確認済み。

### client-payload の文字列組み立て 【対応済み】

`toJSON(github.event.inputs.branch || github.ref_name)` でエスケープするよう修正。
`actionlint` で構文検証済み。

### PAT の運用

→ **決めること**: `INFRA_REPO_PAT` を fine-grained PAT / GitHub App トークンに
移行するか、現状のまま運用するか。infra リポジトリ側の受け口とセットで決まる話なので、
どちらのリポジトリで管理するかも含めて決める。

### PR マージでデプロイが2回走る

`push: main` と `pull_request: closed` の両方が発火する。PR マージは main への
push を伴うため、1回のマージで `repository_dispatch` が2回飛ぶ。
→ **決めること**: `pull_request` トリガーを削るか（`push: main` だけで足りる）、
`workflow_dispatch` 以外を整理するか。infra 側が冪等なら放置も可。

### 確認したが問題なかったもの（再調査の手間を省くため記録）

- **blogcard のリモート `<title>` 注入は XSS にならない。** `htmlUnescape | truncate` を
  経由するが、Hugo（Go html/template）が出力時にエスケープする。スクラッチの Hugo サイトで
  `&lt;img src=x onerror=alert(1)&gt;` を通して実測確認済み。
- blogcard の favicon URL は `/` 始まりか `^https?://` のみ受理するため `javascript:` は入らない。
- `unsafe = true` は自分の記事のみが入力なので実質低リスク。ただし外部由来の HTML を
  記事に貼る運用を始めるなら再評価が必要。
- GA ID / AdSense pub ID / `ads.txt` はいずれも公開前提の識別子。秘匿対象ではない。
- テーマ submodule はブランチではなくコミット `fcf525f` に固定されている（供給網の観点で妥当）。
- AMP は canonical / amphtml が正しく相互リンクされ、`sitemap.xml` に AMP は 0件。
  重複コンテンツにはなっていない。

---

## P4: 判断が必要（コストが高い / 方針次第）

### 外部CDNへのホットリンク 【対応済み: 2026-08-06】

当初「270件がはてなフォトライフ」と記録したが**不正確だった**。全ユニークURLに
HTTPリクエストを投げた結果、実態は以下（`i.moshimo.com` 等のプロトコル相対URL25件を
`static/`配置と誤集計していたのも訂正。真の `static/` 配置は63件）。

| ドメイン | 件数 | 生存 | 対応 |
|---|---|---|---|
| `lh3.googleusercontent.com` | 132 | 99件のみ生存 | 99件を移行 / 33件は除去 |
| `cdn-ak.f.st-hatena.com` | 73 | 200 | 73件を移行 |
| `images-fe.ssl-images-amazon.com` / `ecx.images-amazon.com` | 41 | 200 | 対象外（アフィリエイト） |
| `i.moshimo.com` | 23 | 200 | 対象外（**計測を兼ねるため自前化すると壊れる**） |
| `img.dlsite.jp` / `hbb.afl.rakuten.co.jp` | 3 | 200 | 対象外（アフィリエイト） |
| `i0/i1/i2.wp.com` | 23 | **404** | 除去（復旧不能） |

**移行済み 172件（31MB / 36記事）** を page bundle へ取り込み、相対参照に書き換えた。
レンダーフックの width/height 付与と遅延読み込みが効くようになった。

**除去 56件（3記事）** — いずれも復旧不能と実測で確認:
- Google Photos 33件は認証ページ（HTTP 200 + HTML）が返る。**ブラウザでも表示されない**
  ため、サイト上では既に壊れていた。UA/Referer 変更・サイズ指定除去も試したが同じ
- `i*.wp.com` 23件は元URL・Photonパラメータ無し・Wayback Machine（CDX API）すべて空振り

**教訓**: HTTP 200 は取得成功を意味しない。Google Photos の失効URLは 200 で
サインインページ（HTML）を返す。ダウンロード時は Content-Type ではなく
**バイト列の先頭シグネチャで画像かどうかを検証する**こと（HEAD の Content-Length が
返らないことも失効の兆候だった）。

→ **残る決めること**: 取り込んだ31MBを圧縮するか。現在は原本のまま保持し、
配信サイズはレンダーフックがビルド時に最適化している。

### `static/` 配置の画像（63件・12記事）が最適化対象外 【対応済み: 2026-08-06】

（当初 88件と記録したが、`i.moshimo.com` 等のプロトコル相対URL25件を誤って含めていた。正しくは63件）

当初は page bundle への移行を検討したが、それだと画像URLが
`/images/2018/04/x.jpg` → `/posts/<slug>/x.jpg` に変わる。**対象12記事のうち7記事の
slug が `post-NNN` 形式**で B（slug是正）の候補と重なるため、URLが二度変わる問題があった。
より本質的には、page bundle 化は画像URLを **slug の従属物にする**構造変更である。

**`resources.Copy` で解決した。** assets のリソースは通常 `/images/xxx_hu_<hash>.png` の
ような加工後URLで公開されるが、`resources.Copy` で出力先を元のパスに固定すると
**公開URLを変えないまま**リサイズと寸法取得ができる。スクラッチのHugoサイトで
2000x1000 → 1280x640 の縮小がURL維持のまま効くことを実測確認してから採用した。

- `static/images/{2018,2019,2021,2023,2024}` を `assets/images/` へ移動
- レンダーフックを3経路に対応（page bundle / assets + resources.Copy / 素通し）
- **`default.png` `default.jpg` `logo.png` `profile.jpeg` は `static/` に残す。**
  これらはテンプレートが `absURL "images/default.png"` のようにURLで直接参照しており、
  assets へ移すとレンダーフックを通らないため OGP 画像が再び 404 になる（P1 の退行）

検証: main との画像URL差分ゼロ。日本語ファイル名4件はパーセントエンコードの
大文字小文字差（`%e3` → `%E3`）が出たが RFC 3986 上等価で、両表記とも 200 を確認。
サイト内画像249件すべて 200。git 上は63件すべてリネーム扱いで容量増加なし。

→ **B（slug是正）への依存は解消された。** B を実施しても画像URLは動かない。

**教訓**: 「最適化するには page bundle 化が必要」は思い込みだった。`assets` +
`resources.Copy` なら、URL構造を保ったままリソースパイプラインに載せられる。
構造変更を伴う移行を検討するときは、まず出力先を制御する手段がないか確認する。

### AMP 出力をやめる 【対応済み: 2026-08-06 / infra 側の 301 も完了】

`config/_default/config.toml` の `outputs.page` から `AMP` を外した。

判断の根拠（実施前に再確認済み）: Google は 2021年の Page Experience アップデートで
Top Stories の AMP 必須要件を廃止しており、**AMP に検索上の優遇は無い**。
評価軸は Core Web Vitals に移っている。二重生成のコストだけが残る状態だった。

- ビルド結果: 330ページ → **189ページ**（差分141が AMP 分と一致）
- `rel="amphtml"` はテーマの `partials/meta.html` の `.AlternativeOutputFormats`
  ループ由来のため**自動的に消えた**（テンプレート変更は不要だった）
- トップの RSS `rel="alternate"` は影響を受けず健在
- `sitemap.xml` は 164URL で変化なし（元々 AMP を含んでいなかった）

→ **infra 側の 301 対応は完了済み**（`Shinonome-doki-infra` PR #10、2026-08-07 apply 済み）。
`blog/functions/url-rewrite.js` が `/amp` プレフィックスを落として 301 を返す。
個別マッピング表は不要で、関数サイズは 1,830 → 2,998 バイト（上限 10,240）。

410 ではなく 301 を選んだ理由は、AMPページには元々 HTML への `rel="canonical"` が
張ってあり、Google は既に「正規版は HTML 側」と認識しているため。
410 はその関係を自分から断ち切ることになる。

**このコンテンツ変更をマージしても旧URLは 404 にならない。** 本番で実測確認済み:

| 確認項目 | 結果 |
|---|---|
| `/amp/posts/<slug>/`（末尾スラッシュ有無とも） | 301 → 対応する HTML 版。追従して 200・**1ホップ** |
| `/amp` と `/amp/` | 301 → `/` |
| 誤爆防止 | `/amplifier/` `/posts/amp/` はいずれも転送されず 404 のまま |

### 意味を持たない slug が41記事 【判断済み: 実施しない】

`post-0` `post-327` `2015-06-10-231752` … WordPress 移行時の残骸。URL が内容を示していない。
（当初 40記事と記録していたが、`2020-09-19-22` が日付+連番形式で判定から漏れていた。正しくは41件）

**2026-08-07 に「一括是正は実施しない」と決定した。** 判断は infra 側の
[ADR-0001](https://github.com/Shinogasa/Shinonome-doki-infra/blob/main/docs/adr/0001-no-bulk-slug-normalization.md)
に記録されている（調査資料は同リポジトリ `docs/handoff-slug-redirect.md`）。

要点:
- リダイレクトは「スラッグを変える」選択の結果として発生するコストであり、変えなければ発生しない。
  放置は劣化ではなく現状維持
- 41件の対応表（約2.5KB）が CloudFront Function の 10KB 上限を恒久的に占有し、
  削除すると旧リンクが死ぬため永久に保守対象になる

→ **運用方針**: 新規記事のみ意味のあるスラッグを用い、既存の旧スラッグURLはそのまま維持する。
再検討の条件は ADR の Risks 参照（GTM で旧スラッグ記事の流入が多いと判明した場合）。

補足: E の対応で画像URLは slug から独立したままになったため、
将来もし是正する場合でも記事URLの301だけを考えればよい。

### 記事ごとの `description` が未設定 【対応済み: 2026-08-06】

全記事に手書きするのは非現実的なため、「既存記事にも効く整形」と「新規記事の運用整備」の
2本立てで対応した。

- `partials/normalized-description.html` を新設し、meta / OGP / Twitter / JSON-LD で共通利用。
  plainify + htmlUnescape + 空白畳み込み + 120字制限。
  **従来は `single_meta.html` 側が無加工で JSON-LD 側だけ plainify 済みという不整合**があった
  （実測: 改行混入 83/141件・最長 4242文字 → 改行0件・最長121文字）
- `archetypes/default.md` を実運用の YAML 形式に修正し、`slug`/`description`/`categories` を含めた
  （従来は TOML で乖離しており `hugo new` が使われていなかった）
- README に記事作成手順・front matter 各キーの意味・画像の置き場所を追記

→ **残る運用ルール**: 新規記事では front matter に `description` を書く（全角80〜120文字）。
既存記事への遡及は行わない。

---

## P5: ディレクトリ・設定の整理

以下、`content/posts/2025−06-11-blogcard-robust/` 改名から README 追記までの7件は
**2026-08-06 に対応済み**。

- `content/posts/2025−06-11-blogcard-robust/` の U+2212（全角マイナス）を半角へ改名
  （`git mv`。slugが別に定義されているためURLへの影響なし）
- `content/posts/about/` の `description: Zzo about page`（別テーマ Zzo の残骸）を
  実内容に合わせた文言に修正（ページ自体は `/posts/about/` のまま、type別レイアウトが
  存在しないため移動は見送り）
- root `hugo.toml` を削除し、`ignoreLogs` と `markup.goldmark.renderer.unsafe` を
  `config/_default/config.toml` へ集約。root 削除後も `config/_default/` のみで
  ビルド・実効値が変わらないことを実測確認
- `title`/`description` の二重定義を解消。`hugo config` で実効値を確認したところ
  **`config.toml` 側の `[params].description` は既に `languages.toml` の
  `[ja.params].description` に上書きされ死んでいた**（意図せず無効化されていた設定）。
  実際に効いていた `languages.toml` 側を正としてコメントで明示し、`config.toml` 側は削除
- `tags` 利用0件のため `baseof.html` から `partials/tags.html` の呼び出しを削除
- `migration/*.py`（WordPress移行の使い捨てスクリプト）を削除
- README に `git submodule update --init --recursive` と Hugo Extended 必須の旨を追記

### 未対応（判断待ちのまま）

- **Hugo のバージョンピンが無い。** ローカルと infra 側の乖離を検知できない
  （`tasks/todo.md` の残課題と同一）。
