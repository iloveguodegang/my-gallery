// Supabase 配置文件
const SUPABASE_CONFIG = {
    // Supabase 项目配置
    url: 'https://ibehtwiqwopghgeblflg.supabase.co',
    anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImliZWh0d2lxd29wZ2hnZWJsZmxnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg0MDM1NzYsImV4cCI6MjA2Mzk3OTU3Nn0.yQaK5fo25uU_sDWAnMQilGAsoX4v4uY2eemt5SVg5tI',
    
    // 存储桶配置
    bucketName: 'public',
    
    // 应用配置
    itemsPerPage: 20,
    maxFileSize: 10 * 1024 * 1024, // 10MB
    allowedFileTypes: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
    
    // 默认分类列表
    defaultCategories: ['anime', 'western', 'furry', 'game', 'comic', 'photo', '3d', 'ai'],
    
    // 分类图标映射
    categoryIcons: {
        'anime': 'bi-stars',
        'western': 'bi-palette', 
        'furry': 'bi-emoji-smile',
        'game': 'bi-controller',
        'comic': 'bi-book',
        'photo': 'bi-camera',
        '3d': 'bi-box',
        'ai': 'bi-cpu'
    }
};

// 导出配置
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SUPABASE_CONFIG;
} 