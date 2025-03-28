import re
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_xml_file(input_file, output_file):
    """
    不正なXMLを修正する
    
    Args:
        input_file: 入力XMLファイルのパス
        output_file: 修正後のXMLファイルの出力先パス
    """
    logger.info(f"XMLファイル修正: {input_file} -> {output_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # 修正1: 無効なXML文字の置換
        content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', content)
        
        # 修正2: 不正なHTML/XMLエンティティの置換
        content = re.sub(r'&(?!(amp;|lt;|gt;|quot;|apos;|#\d+;|#x[0-9a-fA-F]+;))', '&amp;', content)
        
        # 修正3: XMLタグ内の無効な属性値の修正
        content = re.sub(r'(<[^>]*)(=\s*"[^"]*\x1A[^"]*")', r'\1=""', content)
        
        # 修正4: 閉じられていないCDATAセクションをチェック
        content = re.sub(r'<!\[CDATA\[(.*?)(?:(?=\]\]>)|\Z)', r'<![CDATA[\1]]>', content, flags=re.DOTALL)
        
        # 修正5: 特定の行の問題を特定
        lines = content.split('\n')
        if len(lines) > 40784:  # エラーが報告された行の前後をチェック
            logger.info(f"問題の行を確認: {lines[40784][:100]}...")
        
        # 修正したコンテンツを保存
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"XMLファイルを修正しました: {output_file}")
        return True
    
    except Exception as e:
        logger.error(f"XMLファイル修正エラー: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用法: python fix_wordpress_xml.py <入力XMLファイル> <出力XMLファイル>")
        sys.exit(1)
    
    if fix_xml_file(sys.argv[1], sys.argv[2]):
        print("XMLファイルの修正が完了しました。")
    else:
        print("XMLファイルの修正に失敗しました。")
        sys.exit(1)
