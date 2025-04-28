# Shinonome-doki
this is my blog by Hugo

## Theme

https://github.com/dim0627/hugo_theme_robust

## Usage

### Build

ローカルで確認

```bash
hugo server -D
```

記事ビルド

```bash
hugo
```

### Deploy

```bash
AWS_PROFILE=private aws s3 sync public/ s3://shinonono.net --delete                                                                 ```
