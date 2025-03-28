import os
import re
import frontmatter
import html2text
import tempfile
import shutil
import sys
import logging
from bs4 import BeautifulSoup
from datetime import datetime

# ロギング設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def convert_wordpress_export_bs4(xml_file, output_dir):
    """
    WordPressエクスポートXMLをBeautifulSoupで解析してHugo用Markdownに変換
    
    Args:
        xml_file (str): WordPressエクスポートXMLファイル
        output_dir (str): 出力ディレクトリ
    """
    logger.info(f"BeautifulSoupを使用した変換開始: {xml_file} -> {output_dir}")
    
    # 1. 画像ディレクトリ作成
    images_dir = os.path.join(output_dir, 'static', 'images')
    posts_dir = os.path.join(output_dir, 'content', 'posts')
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(posts_dir, exist_ok=True)
    logger.info(f"ディレクトリ作成: {images_dir}, {posts_dir}")
    
    try:
        # XMLファイルを読み込む
        with open(xml_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # BeautifulSoupで解析
        soup = BeautifulSoup(content, 'lxml-xml')
        
        # 記事情報を抽出
        items = soup.find_all('item')
        logger.info(f"見つかった記事項目数: {len(items)}")
        
        # HTMLからMarkdown変換用のコンバーター
        converter = html2text.HTML2Text()
        converter.ignore_links = False
        converter.ignore_images = False
        converter.body_width = 0  # 行の折り返しを防止
        
        post_count = 0
        for item in items:
            # 投稿タイプを確認（記事のみ処理）
            post_type = item.find('wp:post_type')
            if not post_type or post_type.text != 'post':
                continue
            
            # 記事ステータスを確認（公開済みのみ処理）
            status = item.find('wp:status')
            if not status or status.text != 'publish':
                continue
            
            # 記事メタデータ抽出
            title = item.find('title')
            title_text = title.text if title else "無題"
            logger.info(f"記事処理中: {title_text}")
            
            pub_date = item.find('wp:post_date')
            pub_date_text = pub_date.text if pub_date else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            slug = item.find('wp:post_name')
            slug_text = slug.text if slug and slug.text else f"post-{abs(hash(title_text))}"
            
            content_elem = item.find('content:encoded')
            content_text = content_elem.text if content_elem else ""
            
            # カテゴリとタグの抽出
            categories = []
            tags = []
            for cat in item.find_all('category'):
                domain = cat.get('domain')
                if domain == 'category':
                    categories.append(cat.text)
                elif domain == 'post_tag':
                    tags.append(cat.text)
            
            # HTMLからMarkdownに変換
            try:
                markdown_content = converter.handle(content_text) if content_text else ""
            except Exception as e:
                logger.error(f"Markdown変換エラー: {str(e)}")
                markdown_content = f"<!-- 変換エラー: {str(e)} -->\n\n{content_text}"
            
            # 画像パスの修正 (WordPress形式からHugo形式へ)
            markdown_content = re.sub(r'!\[([^\]]*)\]\((?:https?://[^/]+)?/wp-content/uploads/([^)]+)\)',
                                     r'![\1](/images/\2)', markdown_content)
            
            # Front Matter用のデータ作成
            data = {
                'title': title_text,
                'date': pub_date_text,
                'slug': slug_text,
                'draft': False
            }
            
            # カテゴリとタグを追加（存在する場合のみ）
            if categories:
                data['categories'] = categories
            if tags:
                data['tags'] = tags
            
            # スラグの安全性確保
            safe_slug = "".join([c if c.isalnum() or c in "._-" else "_" for c in slug_text])
            output_file = os.path.join(posts_dir, f'{safe_slug}.md')
            
            # マークダウンファイル作成
            try:
                # frontmatterとコンテンツを手動で組み立て
                frontmatter_text = "---\n"
                for key, value in data.items():
                    if isinstance(value, list):
                        frontmatter_text += f"{key}:\n"
                        for item in value:
                            frontmatter_text += f"  - {item}\n"
                    else:
                        frontmatter_text += f"{key}: {value}\n"
                frontmatter_text += "---\n\n"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(frontmatter_text + markdown_content)
                
                post_count += 1
                logger.info(f"記事を保存しました: {output_file}")
            except Exception as e:
                logger.error(f"ファイル保存エラー: {str(e)}")
        
        logger.info(f"合計 {post_count} 件の記事を変換しました")
        
        return True
    
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("""
使用法: python wordpress_to_hugo_fixed.py <XMLファイル> <出力ディレクトリ>

入力ファイル:
- WordPress標準のエクスポートXMLファイル

出力ディレクトリ:
- Hugoサイトのルートディレクトリ
        """)
        sys.exit(1)
    
    # 必要なパッケージの確認
    try:
        import bs4
        import html2text
    except ImportError:
        print("必要なパッケージをインストールしてください:")
        print("pip install beautifulsoup4 lxml html2text")
        sys.exit(1)
    
    try:
        if convert_wordpress_export_bs4(sys.argv[1], sys.argv[2]):
            print("変換が完了しました。")
        else:
            print("変換に失敗しました。")
            sys.exit(1)
    except Exception as e:
        logger.error(f"変換失敗: {str(e)}")
        sys.exit(1)
