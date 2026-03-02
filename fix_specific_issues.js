// Node.js script to fix specific Chinese encoding issues in frontend-legacy HTML files

const fs = require('fs');
const path = require('path');

// Define the directory containing frontend-legacy HTML files
const FRONTEND_LEGACY_DIR = 'c:\\BM_Program\\shElter-v3\\frontend-legacy';

// Define specific fixes for remaining issues
const SPECIFIC_FIXES = {
    // Fix trailing question marks in comments
    '/* 加载状态?*/': '/* 加载状态 */',
    '/* 错误状态?*/': '/* 错误状态 */',
    '/* 空状态?*/': '/* 空状态 */',
    '<!-- 加载状态?-->': '<!-- 加载状态 -->',
    '<!-- 错误状态?-->': '<!-- 错误状态 -->',
    '<!-- 空状态?-->': '<!-- 空状态 -->',
    '// 加载状态?': '// 加载状态',
    '// 隐藏所有内容?': '// 隐藏所有内容',
    '// 显示分类列表或空状态?': '// 显示分类列表或空状态',
    '// 显示错误状态?': '// 显示错误状态',
    '// 初始化?': '// 初始化',
    '// 添加重试按钮事件监听器?': '// 添加重试按钮事件监听器',
    
    // Fix specific garbled text
    '技术?': '技术',
    '技术浉鍏崇殑文章': '技术相关的文章',
    '生活相关的文章?': '生活相关的文章',
    '艺术相关的文章?': '艺术相关的文章',
    '科学相关的文章?': '科学相关的文章',
    '音乐相关的文章?': '音乐相关的文章',
    '篇文章?': '篇文章',
    
    // Fix additional issues
    '用户璧勬枡': '用户资料',
    '技术,': '技术',
    '生活相关的文章,': '生活相关的文章',
    '艺术相关的文章,': '艺术相关的文章',
    '科学相关的文章,': '科学相关的文章',
    '音乐相关的文章,': '音乐相关的文章',
    '篇文章/span>': '篇文章</span>',
    
    // Fix unclosed quotes
    'name: \'技术': "name: '技术'",
    'description: \'技术相关的文章': "description: '技术相关的文章'",
    'description: \'生活相关的文章': "description: '生活相关的文章'",
    'description: \'艺术相关的文章': "description: '艺术相关的文章'",
    'description: \'科学相关的文章': "description: '科学相关的文章'",
    'description: \'音乐相关的文章': "description: '音乐相关的文章'",
    
    // Fix edit-article.html issues
    '缂栬緫文章': '编辑文章',
    '寮曞叆Quill瀵屾枃鏈紪杈戝櫎': '引入Quill富文本编辑器',
    '加载文章涓?..': '加载文章中...',
    '鏍囬': '标题',
    '杈撳叆文章鏍囬': '输入文章标题',
    '鎽樿 (鍙€?': '摘要 (可选)',
    '文章鎽樿': '文章摘要',
    '鍐呭': '内容',
    '鏍囩 (閫楀彿鍒嗛殧)': '标签 (逗号分隔)',
    '淇濆瓨鑽夌': '保存草稿',
    '鍙戝竷': '发布',
    'FastAPI鍚庣寮€鍙戞渶浣冲疄璺?': 'FastAPI后端开发最佳实践',
    '鏈枃浠嬬粛浜嗕娇鐢‵astAPI寮€鍙戝悗绔簲鐢ㄧ殑鏈€浣冲疄璺?..': '本文介绍了使用FastAPI开发后端应用的最佳实践...',
    '鍒濆鍖栧瘜鏂囨湰缂栬緫鍣?': '初始化富文本编辑器',
    '模块s: {': 'modules: {',
    '鍦ㄨ繖閲屾挵鍐欎綘鐨勬枃绔犲唴瀹?..': '在这里撰写你的文章内容...',
    '缁戝畾浜嬩欢鐩戝惉鍣?': '绑定事件监听器',
    '妫€鏌ユ槸鍚﹀彲浠ユ彁浜?': '检查是否可以提交',
    '淇濆瓨鑽夌': '保存草稿',
    '鍙戝竷文章': '发布文章',
    '鑾峰彇文章鏁版嵁': '获取文章数据',
    '妯℃嫙API璇锋眰延迟': '模拟API请求延迟',
    '濉厖琛ㄥ崟鏁版嵁': '填写表单数据',
    '澶勭悊提交': '处理提交',
    '更新鎸夐挳状态?': '更新按钮状态',
    '妯℃嫙API鍝嶅簲': '模拟API响应',
    '淇濆瓨成功锛岄噸瀹氬悜鍒版枃绔犺鎯呴〉': '保存成功，重定向到文章详情页',
    '鎭㈠鎸夐挳鏂囨湰': '重置按钮文字'
};

// Function to fix a single file
function fixFile(filePath) {
    console.log(`Processing file: ${filePath}`);
    
    try {
        // Read the file content with UTF-8 encoding
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Apply all specific fixes
        let modified = false;
        for (const [garbled, correct] of Object.entries(SPECIFIC_FIXES)) {
            if (content.includes(garbled)) {
                // Use simple string replacement instead of regex to avoid special character issues
                while (content.includes(garbled)) {
                    content = content.replace(garbled, correct);
                }
                modified = true;
                console.log(`  Fixed: ${garbled} -> ${correct}`);
            }
        }
        
        // Write back the fixed content if any changes were made
        if (modified) {
            fs.writeFileSync(filePath, content, 'utf8');
            console.log(`  Saved changes to: ${filePath}`);
        } else {
            console.log(`  No changes needed for: ${filePath}`);
        }
    } catch (error) {
        console.error(`  Error processing ${filePath}: ${error.message}`);
    }
}

// Function to process all frontend-legacy HTML files
function processFrontendLegacyFiles() {
    const files = fs.readdirSync(FRONTEND_LEGACY_DIR);
    for (const file of files) {
        if (file.endsWith('.html')) {
            // Skip test files
            if (file === 'test-router.html') {
                continue;
            }
            const filePath = path.join(FRONTEND_LEGACY_DIR, file);
            fixFile(filePath);
        }
    }
}

// Main function
console.log('Starting to fix specific Chinese encoding issues in frontend-legacy HTML files...');
processFrontendLegacyFiles();
console.log('All frontend-legacy HTML files have been processed.');
