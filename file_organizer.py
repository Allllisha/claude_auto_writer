#!/usr/bin/env python3
"""
File Organizer - ファイル整理・アーカイブシステム
AI Melody Kobo - 投稿されたファイルと関連データを整理保存
"""

import os
import sys
import shutil
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import hashlib
import re

# プロジェクトのパスを追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FileOrganizer:
    """ファイル整理・アーカイブシステム"""
    
    def __init__(self, base_dir: str = None):
        """
        初期化
        
        Args:
            base_dir: プロジェクトのベースディレクトリ
        """
        self.base_dir = Path(base_dir or os.path.dirname(os.path.abspath(__file__)))
        self.archives_dir = self.base_dir / "archives"
        
        # アーカイブディレクトリ構造
        self.archive_structure = {
            'articles': self.archives_dir / "articles",
            'images': self.archives_dir / "images", 
            'logs': self.archives_dir / "logs",
            'backup': self.archives_dir / "backup",
            'generated': self.archives_dir / "generated",
            'published': self.archives_dir / "published"
        }
        
        # ディレクトリを作成
        self._create_directories()
        
        # インデックスファイル
        self.index_file = self.archives_dir / "file_index.json"
        self.index_data = self._load_index()
    
    def _create_directories(self):
        """アーカイブディレクトリ構造を作成"""
        for dir_path in self.archive_structure.values():
            dir_path.mkdir(parents=True, exist_ok=True)
            
        # 日付別サブディレクトリ
        today = datetime.now().strftime("%Y/%m")
        for main_dir in ['articles', 'images', 'generated', 'published']:
            monthly_dir = self.archive_structure[main_dir] / today
            monthly_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_index(self) -> Dict:
        """インデックスファイルを読み込み"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"インデックス読み込みエラー: {e}")
        
        return {
            'files': [],
            'articles': [],
            'images': [],
            'last_updated': None,
            'total_files': 0,
            'statistics': {
                'articles_count': 0,
                'images_count': 0,
                'total_size_mb': 0
            }
        }
    
    def _save_index(self):
        """インデックスファイルを保存"""
        self.index_data['last_updated'] = datetime.now().isoformat()
        self.index_data['total_files'] = len(self.index_data['files'])
        
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.index_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"インデックス保存エラー: {e}")
    
    def archive_generated_article(self, 
                                 article_content: str,
                                 metadata: Dict,
                                 title: str = None) -> str:
        """
        生成された記事をアーカイブ
        
        Args:
            article_content: 記事のMarkdownコンテンツ
            metadata: 記事のメタデータ
            title: 記事タイトル（自動抽出も可能）
            
        Returns:
            アーカイブされたファイルのパス
        """
        if not title:
            # タイトルを抽出
            title = self._extract_title_from_content(article_content)
        
        # ファイル名を生成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = self._sanitize_filename(title)
        filename = f"{timestamp}_{safe_title}.md"
        
        # 月別ディレクトリに保存
        month_dir = self.archive_structure['generated'] / datetime.now().strftime("%Y/%m")
        month_dir.mkdir(parents=True, exist_ok=True)
        file_path = month_dir / filename
        
        # メタデータヘッダーを追加
        full_content = self._add_metadata_header(article_content, metadata, title)
        
        # ファイル保存
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        # インデックスに追加
        file_info = {
            'id': hashlib.md5(str(file_path).encode()).hexdigest()[:8],
            'type': 'generated_article',
            'path': str(file_path.relative_to(self.base_dir)),
            'title': title,
            'filename': filename,
            'created_at': datetime.now().isoformat(),
            'size_bytes': file_path.stat().st_size,
            'metadata': metadata,
            'tags': metadata.get('tags', []),
            'article_type': metadata.get('article_type', 'unknown'),
            'tool_name': metadata.get('tool_name'),
            'status': 'generated'
        }
        
        self.index_data['files'].append(file_info)
        self.index_data['articles'].append(file_info)
        self.index_data['statistics']['articles_count'] += 1
        self._save_index()
        
        logger.info(f"記事をアーカイブしました: {file_path}")
        return str(file_path)
    
    def archive_published_article(self,
                                 post_id: int,
                                 post_url: str,
                                 title: str,
                                 content: str,
                                 metadata: Dict) -> str:
        """
        投稿済み記事をアーカイブ
        
        Args:
            post_id: WordPressの投稿ID
            post_url: 投稿URL
            title: 記事タイトル
            content: 記事コンテンツ
            metadata: メタデータ
            
        Returns:
            アーカイブされたファイルのパス
        """
        # ファイル名を生成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = self._sanitize_filename(title)
        filename = f"published_{post_id}_{timestamp}_{safe_title}.md"
        
        # 月別ディレクトリに保存
        month_dir = self.archive_structure['published'] / datetime.now().strftime("%Y/%m")
        month_dir.mkdir(parents=True, exist_ok=True)
        file_path = month_dir / filename
        
        # 投稿情報ヘッダーを追加
        publish_info = {
            'post_id': post_id,
            'post_url': post_url,
            'published_at': datetime.now().isoformat(),
            **metadata
        }
        
        full_content = self._add_metadata_header(content, publish_info, title)
        
        # ファイル保存
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        # インデックスに追加
        file_info = {
            'id': hashlib.md5(str(file_path).encode()).hexdigest()[:8],
            'type': 'published_article',
            'path': str(file_path.relative_to(self.base_dir)),
            'title': title,
            'filename': filename,
            'created_at': datetime.now().isoformat(),
            'size_bytes': file_path.stat().st_size,
            'post_id': post_id,
            'post_url': post_url,
            'metadata': publish_info,
            'status': 'published'
        }
        
        self.index_data['files'].append(file_info)
        self.index_data['articles'].append(file_info)
        self.index_data['statistics']['articles_count'] += 1
        self._save_index()
        
        logger.info(f"投稿済み記事をアーカイブしました: {file_path}")
        return str(file_path)
    
    def archive_image(self, 
                     image_data: bytes,
                     filename: str,
                     metadata: Dict = None) -> str:
        """
        画像をアーカイブ
        
        Args:
            image_data: 画像のバイナリデータ
            filename: ファイル名
            metadata: メタデータ
            
        Returns:
            アーカイブされたファイルのパス
        """
        # 月別ディレクトリに保存
        month_dir = self.archive_structure['images'] / datetime.now().strftime("%Y/%m")
        month_dir.mkdir(parents=True, exist_ok=True)
        
        # タイムスタンプを追加
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(filename)
        timestamped_filename = f"{timestamp}_{name}{ext}"
        file_path = month_dir / timestamped_filename
        
        # 画像保存
        with open(file_path, 'wb') as f:
            f.write(image_data)
        
        # メタデータファイルも保存
        if metadata:
            metadata_path = file_path.with_suffix('.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        # インデックスに追加
        file_info = {
            'id': hashlib.md5(str(file_path).encode()).hexdigest()[:8],
            'type': 'image',
            'path': str(file_path.relative_to(self.base_dir)),
            'filename': timestamped_filename,
            'original_filename': filename,
            'created_at': datetime.now().isoformat(),
            'size_bytes': file_path.stat().st_size,
            'metadata': metadata or {},
            'has_metadata_file': bool(metadata)
        }
        
        self.index_data['files'].append(file_info)
        self.index_data['images'].append(file_info)
        self.index_data['statistics']['images_count'] += 1
        self._save_index()
        
        logger.info(f"画像をアーカイブしました: {file_path}")
        return str(file_path)
    
    def organize_old_files(self):
        """既存の散らばったファイルを整理"""
        logger.info("既存ファイルの整理を開始...")
        
        # 整理対象のパターン
        patterns = {
            'articles': ['*.md', 'final_article_*.md', 'sample_article_*.md'],
            'images': ['*.png', '*.jpg', '*.jpeg'],
            'logs': ['*.log'],
            'generated': ['generate_*.py', '*_article.py']
        }
        
        organized_count = 0
        
        for category, file_patterns in patterns.items():
            for pattern in file_patterns:
                for file_path in self.base_dir.glob(pattern):
                    if file_path.is_file() and not file_path.name.startswith('.'):
                        self._move_to_archive(file_path, category)
                        organized_count += 1
        
        logger.info(f"ファイル整理完了: {organized_count}個のファイルを移動")
    
    def _move_to_archive(self, file_path: Path, category: str):
        """ファイルをアーカイブディレクトリに移動"""
        target_dir = self.archive_structure[category]
        
        # 同名ファイルがある場合はタイムスタンプを追加
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if (target_dir / file_path.name).exists():
            name, ext = os.path.splitext(file_path.name)
            new_name = f"{name}_{timestamp}{ext}"
        else:
            new_name = file_path.name
        
        target_path = target_dir / new_name
        shutil.move(str(file_path), str(target_path))
        logger.info(f"移動: {file_path.name} -> {target_path}")
    
    def _extract_title_from_content(self, content: str) -> str:
        """Markdownコンテンツからタイトルを抽出"""
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()
            elif line.startswith('## ') and not line.startswith('### '):
                return line[3:].strip()
        
        # タイトルが見つからない場合
        return f"記事_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _sanitize_filename(self, filename: str) -> str:
        """ファイル名を安全な形式に変換"""
        # 危険な文字を除去
        safe_chars = re.sub(r'[<>:"/\\|?*]', '', filename)
        # 長さ制限
        if len(safe_chars) > 50:
            safe_chars = safe_chars[:50]
        return safe_chars or "unnamed"
    
    def _add_metadata_header(self, content: str, metadata: Dict, title: str) -> str:
        """記事にメタデータヘッダーを追加"""
        header = "---\n"
        header += f"title: {title}\n"
        header += f"archived_at: {datetime.now().isoformat()}\n"
        
        for key, value in metadata.items():
            if key not in ['title']:
                header += f"{key}: {value}\n"
        
        header += "---\n\n"
        return header + content
    
    def get_statistics(self) -> Dict:
        """アーカイブ統計情報を取得"""
        total_size = sum(
            Path(self.base_dir / file_info['path']).stat().st_size 
            for file_info in self.index_data['files']
            if Path(self.base_dir / file_info['path']).exists()
        )
        
        return {
            'total_files': len(self.index_data['files']),
            'articles_count': len(self.index_data['articles']),
            'images_count': len(self.index_data['images']),
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'last_updated': self.index_data['last_updated'],
            'archive_directories': list(self.archive_structure.keys())
        }
    
    def search_files(self, query: str, file_type: str = None) -> List[Dict]:
        """ファイルを検索"""
        results = []
        query_lower = query.lower()
        
        for file_info in self.index_data['files']:
            if file_type and file_info['type'] != file_type:
                continue
            
            # タイトル、ファイル名、タグで検索
            if (query_lower in file_info.get('title', '').lower() or
                query_lower in file_info['filename'].lower() or
                any(query_lower in tag.lower() for tag in file_info.get('tags', []))):
                results.append(file_info)
        
        return results
    
    def list_recent_files(self, limit: int = 10, file_type: str = None) -> List[Dict]:
        """最近のファイルを取得"""
        filtered_files = self.index_data['files']
        
        if file_type:
            filtered_files = [f for f in filtered_files if f['type'] == file_type]
        
        # 作成日時でソート
        sorted_files = sorted(
            filtered_files,
            key=lambda x: x['created_at'],
            reverse=True
        )
        
        return sorted_files[:limit]


def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='AI Melody Kobo - ファイル整理・アーカイブシステム'
    )
    parser.add_argument(
        '--organize',
        action='store_true',
        help='既存ファイルを整理'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='統計情報を表示'
    )
    parser.add_argument(
        '--search',
        help='ファイルを検索'
    )
    parser.add_argument(
        '--recent',
        type=int,
        default=10,
        help='最近のファイルを表示（件数指定）'
    )
    parser.add_argument(
        '--type',
        choices=['generated_article', 'published_article', 'image'],
        help='ファイルタイプでフィルター'
    )
    
    args = parser.parse_args()
    
    organizer = FileOrganizer()
    
    if args.organize:
        organizer.organize_old_files()
    
    if args.stats:
        stats = organizer.get_statistics()
        print("\n📊 アーカイブ統計:")
        print(f"   総ファイル数: {stats['total_files']}")
        print(f"   記事数: {stats['articles_count']}")
        print(f"   画像数: {stats['images_count']}")
        print(f"   総サイズ: {stats['total_size_mb']} MB")
        print(f"   最終更新: {stats['last_updated']}")
    
    if args.search:
        results = organizer.search_files(args.search, args.type)
        print(f"\n🔍 検索結果: '{args.search}'")
        for file_info in results[:10]:
            print(f"   {file_info['filename']} ({file_info['type']})")
    
    if not any([args.organize, args.stats, args.search]):
        recent_files = organizer.list_recent_files(args.recent, args.type)
        print(f"\n📁 最近のファイル ({len(recent_files)}件):")
        for file_info in recent_files:
            print(f"   {file_info['created_at'][:16]} - {file_info['filename']}")


if __name__ == "__main__":
    main()