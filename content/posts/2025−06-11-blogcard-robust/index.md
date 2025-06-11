---
title: Hugo v0.141.0以降でブログカードを利用する
date: 2025-06-11 10:00:00
slug: blogcard-robust-and-hugo-after-v0.141.0
draft: False
categories:
  - プログラミング
---

ブログをHugoに移行してブログカードを表示できないか探していたところ、ありがたいことに先駆者様がいらっしゃいました。

{{< blogcard "https://rkd3.dev/post/linkcard/" >}}

こちらのコードをそのまま`layouts/shortcodes/blogcard.html`へ記載して
`{{</* blogcard "https://rkd3.dev/post/linkcard/" */>}}`
とショートコードを設定したところエラーが発生して記事がビルドできませんでした。

```
Error: error building site: render: failed to render pages: render of "/Users/sasaki-no/garage/Shinonome-doki/content/posts/hoge/index.md" failed: "/Users/sasaki-no/garage/Shinonome-doki/layouts/_default/single.html:8:3": execute of template failed: template: _default/single.html:8:3: executing "main" at <.Render>: error calling Render: failed to execute template _default/summary.html: "/Users/sasaki-no/garage/Shinonome-doki/themes/robust/layouts/_default/summary.html:33:31": execute of template failed: template: _default/summary.html:33:31: executing "_default/summary.html" at <.Content>: error calling Content: "/Users/sasaki-no/garage/Shinonome-doki/content/posts/hoge/index.md:296:1": failed to render shortcode "blogcard": failed to process shortcode: "/Users/sasaki-no/garage/Shinonome-doki/layouts/shortcodes/blogcard.html:8:20": execute of template failed: template: shortcodes/blogcard.html:8:20: executing "shortcodes/blogcard.html" at <$result.Err>: can't evaluate field Err in type resource.Resource: Resource.Err was removed in Hugo v0.141.0 and replaced with a new try keyword, see https://gohugo.io/functions/go-template/try/
```

調べたところ、Hugoのバージョンアップデートにより、`resources.GetRemote`の戻り値の扱い方が変更されたことが原因のようです。  
Hugo v0.141.0以降では、`resources.GetRemote`の結果からエラーを取得する方法が変更され、`$result.Err`プロパティが削除され、代わりに`try`キーワードを使う必要があるとのこと。  

{{< blogcard "https://gohugo.io/functions/go-template/try/">}}

うまく起動するようコードを修正しました。

## 修正後

### /layouts/shortcodes/blogcard.html

```html
{{- $url := (.Get 0) -}}
{{- $target_url := urls.Parse $url -}}

{{- $title := "" -}}
{{- $favicon_url := "" -}}
{{- $content := "" -}}

<!-- try構文を使用してリモートリソースを取得 -->
{{- $resource := false -}}
{{- with resources.GetRemote $url -}}
    {{- $resource = . -}}
    <!-- このスコープ内では$resourceは正常に取得できたリソース -->
    {{- $content = $resource.Content -}}
    
    <!-- headを取得 -->
    {{- $head := index (findRE "<head[^>]*?>(.|\n)*?</head>" $content) 0 -}}

    <!-- headからタイトルを取得 -->
    {{- $title = index (findRE "<title.*?>(.|\n)*?</title>" $head) 0 -}}
    {{- if $title -}}
        {{- $title = replaceRE "</?title>" "" $title -}}
    {{- end -}}

    <!-- headからfaviconを取得 -->
    {{- $linktag := index (findRE "<link[^<>]*rel=[\"']?icon[\"']?.*?>" $head) 0 -}}
    {{- if not $linktag -}}
        {{- $linktag = index (findRE "<link[^<>]*?rel=[\"']?shortcut icon[\"']?.*?>" $head) 0 -}}
    {{- end -}}
    {{- if $linktag -}}
        {{- $href := index (findRE "href=[\"']?[^ >]*[\"']?" $linktag) 0 -}}
        {{- $href = replace $href "href=" "" | replaceRE "[\"']" "" -}}
        {{- if eq (strings.Substr $href 0 1) "/"  -}}
            {{- $favicon_url = print $target_url.Scheme "://" $target_url.Hostname $href -}}
        {{- else if gt (len (findRE "^http[s]?://" $href)) 0 -}}
            {{- $favicon_url = $href -}}
        {{- end -}}
    {{- end -}}

    <!-- /favicon.icoを取得 -->
    {{- if not $favicon_url -}}
        {{- range $favicon_ext := (slice ".ico" ".png" ".gif") -}}
            {{- $root_favicon_path := print $target_url.Scheme "://" $target_url.Hostname "/favicon" $favicon_ext -}}
            {{- $favicon_res := resources.GetRemote $root_favicon_path -}}
            {{- with $favicon_res -}}
                {{- $favicon_url = $root_favicon_path -}}
                {{- break -}}
            {{- end -}}
        {{- end -}}
    {{- end -}}
{{- else -}}
    {{- $title = (print $url "にアクセスできませんでした") -}}
{{- end -}}

<!-- HTMLを生成 -->
<a href="{{- $url -}}">
  <div class="link-card">
    <div class="link-card-title">
      {{- $title | htmlUnescape | truncate 100 -}}
    </div>
    <div class="link-card-hostname">
      {{ if $favicon_url }}
      <div class="link-card-hostname-img">
        <img alt="icon" src="{{- $favicon_url -}}">
      </div>
      {{ end }}
      <span>
        {{- $target_url.Hostname -}}
      </span>
    </div>
  </div>
</a>
```

### /layouts/partials/custom.css

こちらのCSSは元のブログ記事から一切変更しておりません。  

```css
.link-card {
  display: flex;
  flex-direction: column;
  padding: 1.5em;
  margin-top: 1em;
  margin-bottom: 1em;
  /* 以下はお好みで */
  border:solid 2px rgba(0,0,0,0.15);
  border-radius:5px;
}

/* マウスホバー時の挙動 */
.link-card:hover {
  opacity: 0.6;
  transition: 0.1s;
}

.link-card-title {
  font-weight: bold;
  margin-bottom: 0.8em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.link-card-hostname {
  display: flex;
  align-items: center;
  height: 1.5em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.link-card-hostname-img {
  height: 100%;
  display: flex;
  align-items: center;
}

.link-card-hostname-img img {
  max-height: 100%;
  width: auto;
  margin-right: 1em;
}

.link-card-hostname span {
  font-size: 0.9em;
}
```

### 使い方

記事内で以下のようにショートコードを使用します。

```
{{</* blogcard "https://example.com" */>}}
```
{{< blogcard "https://example.com" >}}

これでエラーなくブログカードが表示されるようになりました。

## 参考リンク

{{< blogcard "https://rkd3.dev/post/linkcard/" >}}
{{< blogcard "https://gohugo.io/functions/go-template/try/">}}
