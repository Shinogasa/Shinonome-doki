import os
import re
import frontmatter
import html2text
from xml.etree import ElementTree

def convert_wordpress_export(wpress_file, output_dir):
    """
    .wpressファイルからHugo用Markdownに変換
    
    Args:
        wpress_file (str): All-in-One WP Migrationエクスポートファイル
        output_dir (str): 出力ディレクトリ
    """
    # 1. 画像ディレクトリ作成
    images_dir = os.path.join(output_dir, 'static', 'images')
    posts_dir = os.path.join(output_dir, 'content', 'posts')
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(posts_dir, exist_ok=True)

    # 2. .wpressファイルを解凍
    import zipfile
    with zipfile.ZipFile(wpress_file, 'r') as zip_ref:
        # xmlファイルを探す
        xml_files = [f for f in zip_ref.namelist() if f.endswith('.xml')]
        
        if not xml_files:
            raise ValueError("XMLファイルが見つかりません")
        
        # XMLをパース
        with zip_ref.open(xml_files[0]) as xml_file:
            tree = ElementTree.parse(xml_file)
            root = tree.getroot()

    # 3. 記事変換
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = False

    for item in root.findall('.//item'):
        # 記事メタデータ抽出
        title = item.find('title').text
        pub_date = item.find('wp:post_date', namespaces={'wp': 'http://wordpress.org/export/1.2/'}).text
        slug = item.find('wp:post_name', namespaces={'wp': 'http://wordpress.org/export/1.2/'}).text
        content = item.find('content:encoded', namespaces={'content': 'http://purl.org/rss/1.0/modules/content/'}).text
        
        # HTMLからMarkdownに変換
        markdown_content = converter.handle(content)
        
        # Front Matter付きのMarkdownファイル作成
        post = frontmatter.Post(markdown_content)
        post['title'] = title
        post['date'] = pub_date
        post['slug'] = slug

        # ファイル出力
        output_file = os.path.join(posts_dir, f'{slug}.md')
        with open(output_file, 'wb') as f:
            frontmatter.dump(post, f)

    # 4. 画像ファイルコピー
    import shutil
    for f in zip_ref.namelist():
        if f.startswith('wp-content/uploads/'):
            filename = os.path.basename(f)
            if filename:
                dest_path = os.path.join(images_dir, filename)
                with zip_ref.open(f) as source, open(dest_path, 'wb') as dest:
                    shutil.copyfileobj(source, dest)

    print(f"移行完了: {output_dir}を確認してください")

# 使用例
# pip install python-frontmatter html2text
# python wordpress_to_hugo.py export.wpress ./..

