#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rule34 演示爬虫 - 只获取元数据，不下载图片
"""

import requests
import json
import xml.etree.ElementTree as ET

def demo_scraper():
    """演示爬虫，只获取前3个帖子的元数据"""
    base_url = "https://api.rule34.xxx/index.php"
    
    # 获取帖子列表
    params = {
        'page': 'dapi',
        's': 'post',
        'q': 'index',
        'tags': 'score:>100',
        'limit': 3,
        'pid': 0
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        # 解析XML响应
        root = ET.fromstring(response.content)
        posts = []
        
        for post in root.findall('.//post'):
            post_data = {
                'id': post.get('id'),
                'file_url': post.get('file_url'),
                'tags': post.get('tags', '').split(),
                'score': post.get('score'),
                'rating': post.get('rating'),
                'width': post.get('width'),
                'height': post.get('height'),
                'created_at': post.get('created_at')
            }
            posts.append(post_data)
        
        # 生成元数据示例
        metadata = []
        for post in posts:
            # 模拟标签分类（简化版）
            tags = post['tags']
            
            # 简单的标签分类示例
            artist_tags = [tag for tag in tags if 'artist' in tag or any(name in tag for name in ['sakimichan', 'cutesexyrobutts', 'nyantcha'])]
            character_tags = [tag for tag in tags if any(char in tag for char in ['miku', 'rem', 'asuka', 'zelda', 'peach'])]
            copyright_tags = [tag for tag in tags if any(series in tag for series in ['pokemon', 'zelda', 'mario', 'evangelion', 'fate'])]
            general_tags = [tag for tag in tags if tag not in artist_tags + character_tags + copyright_tags][:10]
            
            meta = {
                'id': post['id'],
                'filename': f"{post['id']}.jpg",
                'width': post['width'],
                'height': post['height'],
                'rating': post['rating'],
                'score': post['score'],
                'created_at': post['created_at'],
                'tags': {
                    'all': tags,
                    'artist': artist_tags,
                    'character': character_tags,
                    'copyright': copyright_tags,
                    'general': general_tags
                },
                'category': 'anime',
                'supabase_tags': []
            }
            
            # 生成supabase标签
            supabase_tags = []
            for artist in artist_tags:
                supabase_tags.append(f"artist:{artist}")
            for character in character_tags:
                supabase_tags.append(f"character:{character}")
            for copyright in copyright_tags:
                supabase_tags.append(f"copyright:{copyright}")
            supabase_tags.extend(general_tags[:5])
            
            meta['supabase_tags'] = supabase_tags
            metadata.append(meta)
        
        # 保存元数据示例
        with open('demo_metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print("✅ 演示元数据已生成！")
        print(f"📁 文件位置: demo_metadata.json")
        print(f"📊 包含 {len(metadata)} 个图片的元数据")
        
        # 显示第一个示例
        if metadata:
            print("\n📋 第一个图片的元数据示例:")
            print(json.dumps(metadata[0], ensure_ascii=False, indent=2))
        
        return metadata
        
    except Exception as e:
        print(f"❌ 获取数据失败: {e}")
        return []

if __name__ == "__main__":
    demo_scraper() 