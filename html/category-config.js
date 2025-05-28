// 分类和标签配置文件
// 修改这个文件来添加新的分类和标签建议

const GALLERY_CONFIG = {
    // 支持的分类列表
    categories: [
        { value: 'anime', label: '动漫', icon: 'bi-stars' },
        { value: 'western', label: '西方', icon: 'bi-palette' },
        { value: 'furry', label: '兽人', icon: 'bi-emoji-smile' },
        { value: 'game', label: '游戏', icon: 'bi-controller' },
        { value: 'comic', label: '漫画', icon: 'bi-book' },
        { value: 'photo', label: '摄影', icon: 'bi-camera' },
        { value: '3d', label: '3D渲染', icon: 'bi-box' },
        { value: 'ai', label: 'AI生成', icon: 'bi-cpu' }
    ],
    
    // 每个分类的推荐标签
    tagSuggestions: {
        anime: {
            characters: ['girl', 'boy', 'woman', 'man', 'loli', 'shota'],
            appearance: ['cute', 'kawaii', 'beautiful', 'handsome', 'cool'],
            hair: ['long_hair', 'short_hair', 'blonde', 'brunette', 'black_hair', 'white_hair', 'pink_hair'],
            clothing: ['school_uniform', 'dress', 'kimono', 'casual', 'formal'],
            expressions: ['smile', 'blush', 'angry', 'sad', 'surprised'],
            poses: ['standing', 'sitting', 'lying', 'running', 'dancing']
        },
        
        western: {
            style: ['realistic', 'art', 'painting', 'digital_art', 'sketch', 'watercolor'],
            subjects: ['portrait', 'landscape', 'still_life', 'abstract'],
            quality: ['detailed', 'high_quality', 'masterpiece', 'professional'],
            techniques: ['oil_painting', 'acrylic', 'pencil', 'charcoal', 'digital']
        },
        
        furry: {
            species: ['wolf', 'cat', 'fox', 'dragon', 'dog', 'rabbit', 'bear', 'tiger'],
            characteristics: ['anthropomorphic', 'character', 'cute', 'fluffy', 'muscular'],
            features: ['tail', 'ears', 'paws', 'fangs', 'claws']
        },
        
        game: {
            types: ['character', 'screenshot', 'concept_art', 'fanart'],
            quality: ['3d', 'render', 'high_poly', 'low_poly'],
            genres: ['rpg', 'fps', 'moba', 'strategy', 'indie'],
            platforms: ['pc', 'console', 'mobile']
        },
        
        comic: {
            styles: ['manga', 'comic', 'illustration', 'webcomic'],
            elements: ['panel', 'page', 'cover', 'character_sheet'],
            genres: ['action', 'romance', 'comedy', 'horror', 'sci_fi', 'fantasy']
        },
        
        photo: {
            types: ['portrait', 'landscape', 'street', 'nature', 'architecture'],
            quality: ['high_resolution', 'professional', 'candid'],
            lighting: ['natural_light', 'studio', 'golden_hour', 'night'],
            equipment: ['dslr', 'mirrorless', 'film', 'smartphone']
        },
        
        '3d': {
            software: ['blender', 'maya', 'max', 'cinema4d', 'zbrush'],
            types: ['character', 'environment', 'product', 'architectural'],
            quality: ['high_poly', 'low_poly', 'sculpt', 'retopo'],
            rendering: ['cycles', 'eevee', 'arnold', 'vray', 'octane']
        },
        
        ai: {
            models: ['stable_diffusion', 'midjourney', 'dalle', 'niji'],
            quality: ['high_quality', 'detailed', 'masterpiece'],
            styles: ['photorealistic', 'artistic', 'anime_style', 'cartoon'],
            techniques: ['txt2img', 'img2img', 'inpainting', 'upscale']
        },
        
        // 通用标签（适用于所有分类）
        common: {
            composition: ['solo', 'duo', 'group', 'crowd'],
            viewpoint: ['looking_at_viewer', 'looking_away', 'profile', 'back_view'],
            environment: ['outdoors', 'indoors', 'nature', 'urban', 'fantasy'],
            time: ['day', 'night', 'sunset', 'sunrise', 'twilight'],
            mood: ['peaceful', 'dramatic', 'mysterious', 'cheerful', 'melancholic'],
            quality: ['high_quality', 'detailed', 'masterpiece', 'best_quality']
        }
    },
    
    // 预设标签模板
    tagTemplates: {
        anime_girl: {
            name: '动漫女孩',
            tags: ['anime', 'girl', 'cute', 'kawaii', 'solo', 'looking_at_viewer']
        },
        anime_boy: {
            name: '动漫男孩',
            tags: ['anime', 'boy', 'handsome', 'cool', 'solo']
        },
        western_portrait: {
            name: '西方肖像',
            tags: ['western', 'portrait', 'realistic', 'detailed', 'high_quality']
        },
        furry_character: {
            name: '兽人角色',
            tags: ['furry', 'anthropomorphic', 'character', 'cute']
        },
        game_screenshot: {
            name: '游戏截图',
            tags: ['game', 'screenshot', '3d', 'high_quality']
        },
        ai_artwork: {
            name: 'AI艺术',
            tags: ['ai', 'stable_diffusion', 'high_quality', 'detailed', 'masterpiece']
        }
    },
    
    // 标签颜色配置（用于UI显示）
    tagColors: {
        // 角色相关
        'girl': '#ff69b4',
        'boy': '#4169e1',
        'cute': '#ff1493',
        'kawaii': '#ff69b4',
        
        // 质量相关
        'high_quality': '#32cd32',
        'masterpiece': '#ffd700',
        'detailed': '#00ced1',
        
        // 风格相关
        'anime': '#ff6347',
        'western': '#4682b4',
        'furry': '#daa520',
        'realistic': '#696969',
        
        // 默认颜色
        'default': '#6c757d'
    }
};

// 导出配置（如果在模块环境中使用）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GALLERY_CONFIG;
}

// 使用说明：
// 1. 添加新分类：在 categories 数组中添加新项
// 2. 添加标签建议：在 tagSuggestions 中为对应分类添加标签
// 3. 创建标签模板：在 tagTemplates 中添加常用组合
// 4. 自定义标签颜色：在 tagColors 中设置标签的显示颜色

// 示例：如何添加新分类 "video"
/*
categories: [
    // ... 现有分类
    { value: 'video', label: '视频', icon: 'bi-play-circle' }
],

tagSuggestions: {
    // ... 现有建议
    video: {
        types: ['animation', 'live_action', 'music_video', 'trailer'],
        quality: ['4k', 'hd', 'high_framerate'],
        duration: ['short', 'medium', 'long']
    }
}
*/ 