# Rule34-lite 图片画廊前端

这是一个基于 Bootstrap 5 和 Supabase 的现代化图片画廊前端页面。

## 功能特性

- 🖼️ **图片浏览** - 响应式网格布局，支持无限滚动
- 🏷️ **分类筛选** - 侧边栏显示所有分类及数量统计
- 🔍 **标签搜索** - 搜索特定标签的图片
- 📱 **响应式设计** - 完美适配移动端和桌面端
- 🌙 **暗色主题** - 护眼的深色界面设计
- 💾 **图片下载** - 支持查看原图和下载
- ⚡ **高性能** - 懒加载和分页加载优化

## 快速部署

### 1. 配置 Supabase

在 `index.html` 文件中找到以下代码（约第220行）：

```javascript
const SUPABASE_URL = 'YOUR-PROJECT-URL';
const SUPABASE_ANON_KEY = 'YOUR-ANON-KEY';
```

将其替换为你的 Supabase 项目配置：
- `YOUR-PROJECT-URL` - 从 Supabase Dashboard → Settings → API → Project URL 复制
- `YOUR-ANON-KEY` - 从 Supabase Dashboard → Settings → API → anon public 复制

### 2. 确保数据库设置正确

确保你的 Supabase 数据库有以下配置：

**images 表结构**：
- `id` (uuid) - 主键
- `file_path` (text) - 存储路径，如 "public/image.jpg"
- `category` (text) - 分类，如 "anime", "western", "furry"
- `tags` (text[]) - 标签数组
- `uploaded_at` (timestamp) - 上传时间

**存储桶**：
- 创建名为 `public` 的公开存储桶

### 3. 部署方式

#### 方式一：GitHub Pages

1. 将 `index.html` 推送到 GitHub 仓库
2. 在仓库设置中启用 GitHub Pages
3. 选择分支和目录，保存后即可访问

#### 方式二：静态托管服务

直接上传 `index.html` 到任何静态托管服务：
- Vercel
- Netlify  
- Cloudflare Pages
- 阿里云 OSS
- 腾讯云 COS

#### 方式三：本地预览

```bash
# 使用 Python
python -m http.server 8000

# 或使用 Node.js
npx serve .
```

## 使用说明

1. **浏览图片** - 页面加载后自动显示所有图片，向下滚动自动加载更多
2. **分类筛选** - 点击左侧分类名称筛选该分类下的图片
3. **搜索标签** - 在顶部搜索框输入标签名称进行搜索
4. **查看详情** - 点击缩略图查看大图和详细信息
5. **标签导航** - 在详情弹窗中点击标签可快速搜索相关图片
6. **下载图片** - 在详情弹窗中点击下载按钮保存图片

## 自定义配置

### 修改每页加载数量

找到第 `PAGE_SIZE` 常量（约第234行）：
```javascript
const PAGE_SIZE = 40; // 修改为你想要的数量
```

### 修改主题颜色

在 CSS 部分（第14-124行）修改颜色变量：
```css
body {
    background-color: #111; /* 背景色 */
    color: #fafafa; /* 文字颜色 */
}
```

### 添加新分类图标

在 `loadCategories` 函数中（约第305行）修改图标映射：
```javascript
const icon = category === 'anime' ? 'bi-stars' : 
           category === 'western' ? 'bi-palette' : 
           category === 'furry' ? 'bi-emoji-smile' : 
           category === 'your-category' ? 'bi-your-icon' : 'bi-folder';
```

## 故障排查

### 图片不显示
- 检查 Supabase URL 和 ANON KEY 是否正确
- 确认存储桶名称为 `public` 且已设置为公开
- 检查 `file_path` 格式是否正确（应为 "public/filename.jpg"）

### 分类统计不准确
- 确保 `images` 表中的 `category` 字段有值
- 检查是否有 RLS 策略限制了数据访问

### 搜索无结果
- 确认 `tags` 字段类型为 `text[]`（数组）
- 标签格式应为 `{tag1,tag2}` 或通过 Supabase Dashboard 添加

## 性能优化建议

1. **图片优化**
   - 上传前压缩图片
   - 使用 WebP 格式
   - 生成不同尺寸的缩略图

2. **CDN 加速**
   - 使用 Cloudflare 等 CDN 服务
   - 启用浏览器缓存

3. **数据库索引**
   - 为 `category` 字段创建索引
   - 为 `tags` 字段创建 GIN 索引

## 许可证

MIT License - 可自由使用和修改 