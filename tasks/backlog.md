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

### 新たに見つかったもの: client-payload の文字列組み立て

`client-payload: '{"branch": "${{ ... github.ref_name }}"}'` は `github.ref_name` を
JSON文字列へ直接埋め込んでいる。ブランチ名に `"` 等が含まれると壊れる可能性はあるが、
ブランチ作成には push 権限が要るため悪用は現実的に低リスク。
→ **決めること**: `toJSON(...)` 相当で安全にエスケープするか、放置するか。

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

### 記事画像の7割（270/371件）が他社CDN（はてなフォトライフ）へのホットリンク

P2 のレンダーフック実装時に判明。`content/posts/` 配下の画像参照371件の内訳は
外部URL 270件・`static/`配置 88件・page bundle同梱 13件。**自前ブログの画像の7割が
`cdn-ak.f.st-hatena.com` に依存**している。相手サービスの仕様変更・閉鎖・ホットリンク拒否で
一括リンク切れになるリスクがある。
→ **決めること**: 静観する／将来的にダウンロードして自前ホスティングへ移行するか。
270件規模なので着手するなら別タスクとして切り出す。

### `static/` 配置の画像（88件・12記事）はレンダーフックで最適化できない

`static/` は Hugo のリソースパイプラインの対象外のため `.Resize` や寸法取得が効かない。
→ **決めること**: page bundle への移行（slugとの結合が強まる）を行うか、
このまま未最適化で運用するか。

### AMP 出力をやめるか

141ページを二重生成している。Google は 2021年に Top Stories の AMP 必須要件を廃止済みで、
現在 AMP に検索上の優遇は無い。害は無いが、テンプレート変更のたびに AMP 側の
影響を考える必要がある（`themes/robust/layouts/_default/baseof.amp.html` 経由）。
→ **決めること**: `config/_default/config.toml` の `outputs.page` から `AMP` を外すか。
外す場合、既に `/amp/**` がインデックスされている可能性があるため、
infra 側で 301 か 410 を返す必要があるかを併せて判断する。

### 意味を持たない slug が40記事

`post-0` `post-327` … WordPress 移行時の残骸。URL が内容を示していない。
→ **決めること**: 直すか放置か。直す場合、公開済み URL の変更なので
**301 リダイレクトが必須**（Hugo の `aliases` は 200 の meta refresh なので SEO 的には劣る。
infra 側でのリダイレクト設定が本筋）。infra リポジトリの管轄も絡む。

### 記事ごとの `description` が未設定

全記事が `.Summary`（本文冒頭の自動切り出し）にフォールバック。実測で165文字＋改行2つ。
Google が日本語で表示するのは概ね全角80文字程度なので、意図した要約になっていない。
→ **決めること**: 全記事に手書きする（コスト高）／新記事から書く運用にする／放置する。

---

## P5: ディレクトリ・設定の整理

- **`content/posts/2025−06-11-blogcard-robust/` のディレクトリ名に U+2212（全角マイナス）が混入。**
  URL は `slug` が決めるので表示に影響は無いが、パス指定やスクリプトが確実に踏む。改名する。
- **`content/posts/about/`** が記事扱いで `/posts/about/` になっている。固定ページなら
  `content/about/` へ移す。front matter の `description: Zzo about page` は
  **別テーマ（Zzo）の残骸**がそのまま meta description に出ているので消す。
- **`.hugo_build.lock` が git に追跡されていた。** 【対応済み】`git rm --cached` で解除。
- **root `hugo.toml` にダミーの `baseURL = 'https://example.org/'` / `title = 'My New Hugo Site'`**
  が残っている。実効値は `config/_default/` 側。誤診の元なので削除し、
  `ignoreLogs` と `markup` も `config/_default/config.toml` へ寄せて設定を1箇所にする。
- **`title` と `description` が `config.toml` と `languages.toml` で二重定義**されている。
  片方に寄せる。
- **`tags` を使っている記事が0件**なのに `baseof.html` が `partials/tags.html` を呼んでいる。
  出力は空なので無害だが、タグ運用を始めないなら呼び出しを消す。
- **`migration/*.py` はデッドコード**（WordPress 移行の使い捨て）。削除するか
  `docs/` 等へ退避する。
- **README に submodule 初期化手順が無い。** 実際にこれで環境構築が詰まった。
  `git submodule update --init --recursive` と Hugo Extended 必須である旨を追記する。
- **Hugo のバージョンピンが無い。** ローカルと infra 側の乖離を検知できない
  （`tasks/todo.md` の残課題と同一）。
