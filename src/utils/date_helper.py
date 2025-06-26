"""
Date Helper Utilities
AI Melody Kobo - 日付と時間関連のヘルパー関数
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import calendar
import pytz


class DateHelper:
    """日付関連のヘルパークラス"""
    
    @staticmethod
    def get_current_year() -> int:
        """現在の年を取得"""
        return datetime.now().year
    
    @staticmethod
    def get_current_month() -> int:
        """現在の月を取得"""
        return datetime.now().month
    
    @staticmethod
    def get_current_quarter() -> str:
        """現在の四半期を取得（Q1-Q4）"""
        month = datetime.now().month
        quarter = (month - 1) // 3 + 1
        return f"Q{quarter}"
    
    @staticmethod
    def get_japanese_date_info() -> Dict[str, str]:
        """日本の日付情報を取得"""
        now = datetime.now(pytz.timezone('Asia/Tokyo'))
        
        # 和暦の計算（令和）
        reiwa_year = now.year - 2018
        
        # 月の和名
        month_names = [
            "睦月", "如月", "弥生", "卯月", "皐月", "水無月",
            "文月", "葉月", "長月", "神無月", "霜月", "師走"
        ]
        
        return {
            'year': str(now.year),
            'month': str(now.month),
            'day': str(now.day),
            'japanese_era': f'令和{reiwa_year}年',
            'japanese_month': month_names[now.month - 1],
            'quarter': DateHelper.get_current_quarter(),
            'formatted_date': now.strftime('%Y年%m月%d日')
        }
    
    @staticmethod
    def get_time_based_keywords() -> List[str]:
        """時期に基づいたキーワードを生成"""
        current_year = DateHelper.get_current_year()
        current_month = DateHelper.get_current_month()
        current_quarter = DateHelper.get_current_quarter()
        
        keywords = [
            f"{current_year}年",
            f"{current_year}年最新",
            f"{current_year}年{current_month}月",
            f"{current_year}年{current_quarter}",
        ]
        
        # 季節のキーワード
        season_keywords = {
            (12, 1, 2): ["冬", "年末年始"],
            (3, 4, 5): ["春", "新生活"],
            (6, 7, 8): ["夏", "夏休み"],
            (9, 10, 11): ["秋", "芸術の秋"]
        }
        
        for months, season_words in season_keywords.items():
            if current_month in months:
                keywords.extend([f"{current_year}年{word}" for word in season_words])
                break
        
        return keywords
    
    @staticmethod
    def format_article_date(date: datetime = None) -> str:
        """記事用の日付フォーマット"""
        if date is None:
            date = datetime.now()
        
        return date.strftime('%Y年%m月%d日')
    
    @staticmethod
    def get_trending_period() -> str:
        """トレンド期間の表現を取得"""
        now = datetime.now()
        
        # 月初めの場合
        if now.day <= 7:
            return f"{now.year}年{now.month}月最新"
        # 月半ばの場合
        elif now.day <= 20:
            return f"{now.year}年{now.month}月中旬"
        # 月末の場合
        else:
            next_month = now.month + 1 if now.month < 12 else 1
            next_year = now.year if now.month < 12 else now.year + 1
            return f"{next_year}年{next_month}月直前"
    
    @staticmethod
    def calculate_days_until(target_date: datetime) -> int:
        """指定日までの日数を計算"""
        today = datetime.now().date()
        target = target_date.date()
        return (target - today).days
    
    @staticmethod
    def is_weekend() -> bool:
        """週末かどうかを判定"""
        return datetime.now().weekday() >= 5
    
    @staticmethod
    def get_publishing_schedule() -> Dict[str, str]:
        """最適な投稿スケジュールを取得"""
        now = datetime.now()
        
        # 平日の朝（7-9時）または夕方（17-19時）が最適
        if now.weekday() < 5:  # 平日
            if 7 <= now.hour < 9:
                return {'timing': 'morning', 'description': '朝の通勤時間帯'}
            elif 17 <= now.hour < 19:
                return {'timing': 'evening', 'description': '夕方の帰宅時間帯'}
            else:
                return {'timing': 'regular', 'description': '通常時間帯'}
        else:  # 週末
            if 10 <= now.hour < 12:
                return {'timing': 'weekend_morning', 'description': '週末の午前中'}
            else:
                return {'timing': 'weekend', 'description': '週末'}