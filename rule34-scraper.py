#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rule34 图片爬虫脚本
功能：爬取图片及其完整标签信息（艺术家、角色、版权等）
输出：图片文件 + JSON元数据文件
"""

import requests
import json
import os
import time
from urllib.parse import urlparse, parse_qs
import xml.etree.ElementTree as ET
from pathlib import Path

class Rule34Scraper:
    def __init__(self, output_dir="rule34_downloads"):
        self.base_url = "https://api.rule34.xxx/index.php"
        self.output_dir = output_dir
        self.metadata_file = os.path.join(output_dir, "metadata.json")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)
        
        # 加载已存在的元数据
        self.existing_metadata = self.load_existing_metadata()
        self.existing_ids = {item['id'] for item in self.existing_metadata}
        
        # 标签分类
        self.tag_categories = {
            'artist': [],      # 艺术家
            'character': [],   # 角色
            'copyright': [],   # 版权/作品
            'general': []      # 一般标签
        }
    
    def load_existing_metadata(self):
        """加载已存在的元数据"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def get_posts(self, tags="", limit=100, page=0):
        """获取帖子列表"""
        params = {
            'page': 'dapi',
            's': 'post',
            'q': 'index',
            'tags': tags,
            'limit': limit,
            'pid': page
        }
        
        try:
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            
            # 解析XML响应
            root = ET.fromstring(response.content)
            posts = []
            
            for post in root.findall('.//post'):
                post_data = {
                    'id': post.get('id'),
                    'file_url': post.get('file_url'),
                    'preview_url': post.get('preview_url'),
                    'tags': post.get('tags', '').split(),
                    'score': post.get('score'),
                    'rating': post.get('rating'),
                    'width': post.get('width'),
                    'height': post.get('height'),
                    'created_at': post.get('created_at'),
                    'md5': post.get('md5')
                }
                posts.append(post_data)
            
            return posts
            
        except Exception as e:
            print(f"获取帖子失败: {e}")
            return []
    
    def get_tag_info(self, tag_name):
        """获取标签的详细信息（类型：艺术家/角色/版权等）"""
        params = {
            'page': 'dapi',
            's': 'tag',
            'q': 'index',
            'name': tag_name
        }
        
        try:
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            tag = root.find('.//tag')
            
            if tag is not None:
                return {
                    'name': tag.get('name'),
                    'type': int(tag.get('type', 0)),  # 0=general, 1=artist, 3=copyright, 4=character
                    'count': int(tag.get('count', 0))
                }
            
        except Exception as e:
            print(f"获取标签信息失败 {tag_name}: {e}")
        
        return None
    
    def categorize_tags(self, tags):
        """将标签分类为艺术家、角色、版权等"""
        categorized = {
            'artist': [],
            'character': [],
            'copyright': [],
            'general': []
        }
        
        for tag in tags:
            tag_info = self.get_tag_info(tag)
            if tag_info:
                tag_type = tag_info['type']
                if tag_type == 1:
                    categorized['artist'].append(tag)
                elif tag_type == 4:
                    categorized['character'].append(tag)
                elif tag_type == 3:
                    categorized['copyright'].append(tag)
                else:
                    categorized['general'].append(tag)
            else:
                categorized['general'].append(tag)
            
            # 避免请求过快
            time.sleep(0.1)
        
        return categorized
    
    def download_image(self, url, filename):
        """下载图片"""
        filepath = os.path.join(self.output_dir, "images", filename)
        
        # 检查文件是否已存在
        if os.path.exists(filepath):
            print(f"  ⏭️  文件已存在，跳过下载: {filename}")
            return True
        
        try:
            response = self.session.get(url, stream=True)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"  ✅ 下载完成: {filename}")
            return True
        except Exception as e:
            print(f"  ❌ 下载图片失败 {url}: {e}")
            return False
    
    def process_posts(self, posts):
        """处理帖子列表"""
        new_metadata = []
        skipped_count = 0
        
        for i, post in enumerate(posts):
            print(f"\n处理帖子 {i+1}/{len(posts)}: ID {post['id']}")
            
            # 检查是否已经爬取过
            if post['id'] in self.existing_ids:
                print(f"  ⏭️  已存在，跳过: ID {post['id']}")
                skipped_count += 1
                continue
            
            # 获取文件扩展名
            file_ext = os.path.splitext(urlparse(post['file_url']).path)[1]
            filename = f"{post['id']}{file_ext}"
            
            # 下载图片
            if self.download_image(post['file_url'], filename):
                # 分类标签
                print("  🏷️  分析标签类型...")
                categorized_tags = self.categorize_tags(post['tags'])
                
                # 创建元数据
                meta = {
                    'id': post['id'],
                    'filename': filename,
                    'file_path': f"images/{filename}",
                    'width': post['width'],
                    'height': post['height'],
                    'rating': post['rating'],
                    'score': post['score'],
                    'created_at': post['created_at'],
                    'tags': {
                        'all': post['tags'],
                        'artist': categorized_tags['artist'],
                        'character': categorized_tags['character'],
                        'copyright': categorized_tags['copyright'],
                        'general': categorized_tags['general']
                    },
                    'category': self.determine_category(categorized_tags),
                    'supabase_tags': self.generate_supabase_tags(categorized_tags)
                }
                
                new_metadata.append(meta)
                self.existing_ids.add(post['id'])  # 添加到已存在列表
                
                print(f"  📊 完成！艺术家: {len(categorized_tags['artist'])}, "
                      f"角色: {len(categorized_tags['character'])}, "
                      f"版权: {len(categorized_tags['copyright'])}, "
                      f"一般: {len(categorized_tags['general'])}")
            
            # 避免请求过快
            time.sleep(1)
        
        # 合并新旧元数据并保存
        all_metadata = self.existing_metadata + new_metadata
        self.save_metadata(all_metadata)
        
        print(f"\n📈 处理完成统计:")
        print(f"  📥 新增: {len(new_metadata)} 个")
        print(f"  ⏭️  跳过: {skipped_count} 个")
        print(f"  📚 总计: {len(all_metadata)} 个")
        
        return new_metadata
    
    def determine_category(self, categorized_tags):
        """根据标签判断分类"""
        # 可以根据标签内容判断分类
        # 这里是一个简单的示例
        if any('anime' in tag for tag in categorized_tags['general']):
            return 'anime'
        elif any('furry' in tag for tag in categorized_tags['general']):
            return 'furry'
        elif any('3d' in tag for tag in categorized_tags['general']):
            return '3d'
        else:
            return 'general'
    
    def generate_supabase_tags(self, categorized_tags):
        """生成适合Supabase的标签数组"""
        # 合并所有标签，但优先显示重要标签
        tags = []
        
        # 按重要性排序：艺术家 > 角色 > 版权 > 一般
        for artist in categorized_tags['artist']:
            tags.append(f"artist:{artist}")
        
        for character in categorized_tags['character']:
            tags.append(f"character:{character}")
        
        for copyright in categorized_tags['copyright']:
            tags.append(f"copyright:{copyright}")
        
        # 只添加部分一般标签（避免太多）
        for tag in categorized_tags['general'][:10]:
            tags.append(tag)
        
        return tags
    
    def save_metadata(self, metadata):
        """保存元数据到JSON文件"""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        print(f"\n💾 元数据已保存到: {self.metadata_file}")
    
    def generate_upload_script(self, metadata):
        """生成批量上传脚本"""
        upload_script = """
// 批量上传脚本 - 在上传工具的控制台中运行
// 首先确保已经连接到Supabase

async function batchUpload() {
    const metadata = %s;
    
    for (const item of metadata) {
        console.log(`上传图片: ${item.filename}`);
        
        // 这里需要先通过文件选择器选择对应的图片文件
        // 或者使用其他方式获取文件对象
        
        const uploadData = {
            file_path: `rule/${item.filename}`,
            category: item.category,
            tags: item.supabase_tags
        };
        
        console.log('元数据:', uploadData);
        
        // 实际上传代码需要配合上传工具实现
    }
}

// 执行批量上传
// batchUpload();
""" % json.dumps(metadata, ensure_ascii=False)
        
        script_file = os.path.join(self.output_dir, "upload_script.js")
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(upload_script)
        print(f"📜 上传脚本已生成: {script_file}")


def main():
    """主函数"""
    scraper = Rule34Scraper()
    
    # 示例：搜索特定标签
    search_tags = "score:>100"  # 搜索评分大于100的图片
    limit = 10  # 每页数量
    page = 0    # 页码
    
    print(f"🚀 开始爬取 Rule34...")
    print(f"🔍 搜索标签: {search_tags}")
    print(f"📄 每页数量: {limit}")
    print(f"📚 已有数据: {len(scraper.existing_metadata)} 个")
    
    # 获取帖子
    posts = scraper.get_posts(search_tags, limit, page)
    print(f"🎯 找到 {len(posts)} 个帖子")
    
    if posts:
        # 处理帖子
        new_metadata = scraper.process_posts(posts)
        
        # 生成上传脚本
        if new_metadata:
            scraper.generate_upload_script(new_metadata)
        
        print("\n🎉 爬取完成！")
        print(f"📁 图片保存在: {scraper.output_dir}/images/")
        print(f"📋 元数据保存在: {scraper.metadata_file}")
        print("\n🔄 下一步：")
        print("1. 使用 metadata.json 中的信息")
        print("2. 配合 batch-upload-tool.html 批量上传")
        print("3. 或使用生成的 upload_script.js")


if __name__ == "__main__":
    main() 