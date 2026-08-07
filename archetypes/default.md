---
title: '{{ replace .File.ContentBaseName "-" " " | title }}'
date: {{ .Date }}
slug: {{ .File.ContentBaseName }}
draft: true
# 検索結果に出る説明文。全角80〜120文字程度で書く。
# 未記入だと本文冒頭が自動で使われる（意図した要約にはならない）。
description: ''
# 既存のカテゴリ名に揃える（例: 日記 / プログラミング / 音楽 / ライブ）
categories: []
---
