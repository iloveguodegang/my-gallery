// Supabase 配置示例
// 将此文件复制为 config.js 并填入你的实际配置

const SUPABASE_CONFIG = {
    // 从 Supabase Dashboard → Settings → API → Project URL 复制
    url: 'https://your-project-id.supabase.co',
    
    // 从 Supabase Dashboard → Settings → API → anon public 复制
    anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
    
    // 可选配置
    options: {
        // 存储桶名称
        storageBucket: 'public',
        
        // 每页加载的图片数量
        pageSize: 40,
        
        // 支持的分类
        categories: ['anime', 'western', 'furry'],
        
        // 分类图标映射
        categoryIcons: {
            'anime': 'bi-stars',
            'western': 'bi-palette',
            'furry': 'bi-emoji-smile',
            'default': 'bi-folder'
        }
    }
};

// 使用说明：
// 1. 将此文件重命名为 config.js
// 2. 填入你的 Supabase URL 和 ANON KEY
// 3. 在 index.html 中添加 <script src="config.js"></script>
// 4. 修改 index.html 中的配置引用：
//    const SUPABASE_URL = SUPABASE_CONFIG.url;
//    const SUPABASE_ANON_KEY = SUPABASE_CONFIG.anonKey; 