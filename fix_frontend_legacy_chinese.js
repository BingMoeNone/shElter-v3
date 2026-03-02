// Node.js script to fix Chinese encoding issues in frontend-legacy HTML files

const fs = require('fs');
const path = require('path');

// Define the directory containing frontend-legacy HTML files
const FRONTEND_LEGACY_DIR = 'c:\\BM_Program\\shElter-v3\\frontend-legacy';

// Define the mapping of garbled Chinese text to correct text
const CHINESE_FIXES = {
    // Common text
    '棣栭〉': '首页',
    '鏂囩珷': '文章',
    '鍒嗙被': '分类',
    '鐧诲綍': '登录',
    '娉ㄥ唽': '注册',
    '涓汉璧勬枡': '个人资料',
    '閫€鍑?': '退出',
    '鎼滅储': '搜索',
    '鍐欐枃绔?': '写文章',
    '鏂囩珷璁烘枃': '文章编辑',
    '鍦伴搧': '地铁',
    '闊充箰': '音乐',
    '鐢ㄦ埛鍚嶇О': '用户名',
    '瀵嗙爜': '密码',
    '閭': '邮箱',
    '鎻愪氦': '提交',
    '鍑嗗': '重置',
    '鏂囩珷鏍囬': '文章标题',
    '鏂囩珷鍐呭': '文章内容',
    '鏂囩珷浠ｈ〃': '文章摘要',
    '鍒嗙被': '分类',
    '鍒嗙爜': '标签',
    '鎴愬姛': '成功',
    '閿欒': '错误',
    '淇℃伅': '信息',
    '鏈嶅姟鍣ㄥ彂鐢熸梾棰?': '服务器发生错误',
    '璇锋鏌ヨ姹傚叧娉?': '请检查请求参数',
    '鐢ㄦ埛涓嶅瓨鍦?': '用户不存在',
    '瀵嗙爜涓嶆': '密码错误',
    '鐢ㄦ埛鍚嶇О宸茬粡瀛樺湪': '用户名已存在',
    '閭宸茬粡瀹氫箟': '邮箱已注册',
    '娉ㄥ唽鎴愬姛': '注册成功',
    '鐧诲綍鎴愬姛': '登录成功',
    '娉ㄩ攢鎴愬姛': '注销成功',
    '鏂囩珷鍒涘缓鎴愬姛': '文章创建成功',
    '鏂囩珷淇敼鎴愬姛': '文章修改成功',
    '鏂囩珷鍒犻櫎鎴愬姛': '文章删除成功',
    '璇勮鎻愪氦鎴愬姛': '评论提交成功',
    '璇勮鍒犻櫎鎴愬姛': '评论删除成功',
    '鐧诲綍鍚庡氨鍙互鍐欐枃绔?': '登录后就可以写文章了',
    '甯屾湜鐧诲綍鎴愬姛': '欢迎登录成功',
    '甯屾湜鏉ュ埌Wiki Platform': '欢迎来到Wiki Platform',
    '甯屾湜浣跨敤Wiki Platform': '欢迎使用Wiki Platform',
    '鏇存柊鏃堕棿': '更新时间',
    '鐢ㄦ埛鍚嶇О': '用户名',
    '鍐欐枃鏃堕棿': '写作时间',
    '鏂囩珷鏁伴噺': '文章数量',
    '璇勮鏁伴噺': '评论数量',
    '瀛楁鏁伴噺': '字数',
    '璁块棶鏁伴噺': '访问量',
    '鐩稿唽鏃堕棿': '注册时间',
    '寮€濮嬫墜浣?': '开始写作',
    '璁块棶鐧诲綍': '点击登录',
    '璁块棶娉ㄥ唽': '点击注册',
    '鐧诲綍鎴愬姛锛屾杩庡洖鏉ャ€?': '登录成功，欢迎回来！',
    '涓ゆ杈撳叆鐨勫瘑鐮佷笉涓€鑷?': '两次输入的密码不一致',
    '瀵嗙爜闀垮害鑷冲皯涓?8 涓瓧绗?': '密码长度至少为 8 个字符',
    '娉ㄥ唽鎴愬姛锛佹鍦ㄤ负鎮ㄨ嚜鍔ㄧ櫥褰?..': '注册成功，正在为您自动登录...',
    '鏂囩珷鏈瓨鍦?': '文章不存在',
    '鎮ㄨ鎼滅储鐨勬枃绔犱笉瀛樺湪': '您要搜索的文章不存在',
    '娌℃湁鎵惧埌瀵瑰簲鐨勬枃绔?': '没有找到对应的文章',
    '娌℃湁瀛樺湪鏈夊叧鐨勫垎绫?': '不存在有关的分类',
    '娌℃湁瀛樺湪鏈夊叧鐨勫垎鏍?': '不存在有关的标签',
    '甯屾湜浣跨敤鏂囩珷鐩稿唽': '欢迎使用文章注册',
    '鐢ㄦ埛涓嶅瓨鍦?': '用户不存在',
    '瀵嗙爜涓嶆': '密码错误',
    '鐢ㄦ埛鍚嶇О宸茬粡瀛樺湪': '用户名已存在',
    '閭宸茬粡瀹氫箟': '邮箱已注册',
    '娉ㄥ唽鎴愬姛': '注册成功',
    '鐧诲綍鎴愬姛': '登录成功',
    '娉ㄩ攢鎴愬姛': '注销成功',
    '鏂囩珷鍒涘缓鎴愬姛': '文章创建成功',
    '鏂囩珷淇敼鎴愬姛': '文章修改成功',
    '鏂囩珷鍒犻櫎鎴愬姛': '文章删除成功',
    '璇勮鎻愪氦鎴愬姛': '评论提交成功',
    '璇勮鍒犻櫎鎴愬姛': '评论删除成功',
    '鐧诲綍鍚庡氨鍙互鍐欐枃绔?': '登录后就可以写文章了',
    '甯屾湜鐧诲綍鎴愬姛': '欢迎登录成功',
    '甯屾湜鏉ュ埌Wiki Platform': '欢迎来到Wiki Platform',
    '甯屾湜浣跨敤Wiki Platform': '欢迎使用Wiki Platform',
    '鏇存柊鏃堕棿': '更新时间',
    '鐢ㄦ埛鍚嶇О': '用户名',
    '鍐欐枃鏃堕棿': '写作时间',
    '鏂囩珷鏁伴噺': '文章数量',
    '璇勮鏁伴噺': '评论数量',
    '瀛楁鏁伴噺': '字数',
    '璁块棶鏁伴噺': '访问量',
    '鐩稿唽鏃堕棿': '注册时间',
    '寮€濮嬫墜浣?': '开始写作',
    '璁块棶鐧诲綍': '点击登录',
    '璁块棶娉ㄥ唽': '点击注册',
    '鐧诲綍鎴愬姛锛屾杩庡洖鏉ャ€?': '登录成功，欢迎回来！',
    '涓ゆ杈撳叆鐨勫瘑鐮佷笉涓€鑷?': '两次输入的密码不一致',
    '瀵嗙爜闀垮害鑷冲皯涓?8 涓瓧绗?': '密码长度至少为 8 个字符',
    '娉ㄥ唽鎴愬姛锛佹鍦ㄤ负鎮ㄨ嚜鍔ㄧ櫥褰?..': '注册成功，正在为您自动登录...',
    '鏂囩珷鏈瓨鍦?': '文章不存在',
    '鎮ㄨ鎼滅储鐨勬枃绔犱笉瀛樺湪': '您要搜索的文章不存在',
    '娌℃湁鎵惧埌瀵瑰簲鐨勬枃绔?': '没有找到对应的文章',
    '娌℃湁瀛樺湪鏈夊叧鐨勫垎绫?': '不存在有关的分类',
    '娌℃湁瀛樺湪鏈夊叧鐨勫垎鏍?': '不存在有关的标签',
    '甯屾湜浣跨敤鏂囩珷鐩稿唽': '欢迎使用文章注册',
    '鐢ㄦ埛涓嶅瓨鍦?': '用户不存在',
    '瀵嗙爜涓嶆': '密码错误',
    '鐢ㄦ埛鍚嶇О宸茬粡瀛樺湪': '用户名已存在',
    '閭宸茬粡瀹氫箟': '邮箱已注册',
    '娉ㄥ唽鎴愬姛': '注册成功',
    '鐧诲綍鎴愬姛': '登录成功',
    '娉ㄩ攢鎴愬姛': '注销成功',
    '鏂囩珷鍒涘缓鎴愬姛': '文章创建成功',
    '鏂囩珷淇敼鎴愬姛': '文章修改成功',
    '鏂囩珷鍒犻櫎鎴愬姛': '文章删除成功',
    '璇勮鎻愪氦鎴愬姛': '评论提交成功',
    '璇勮鍒犻櫎鎴愬姛': '评论删除成功'
};

// Function to fix a single file
function fixFile(filePath) {
    console.log(`Processing file: ${filePath}`);
    
    try {
        // Read the file content with UTF-8 encoding
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Apply all fixes
        let modified = false;
        for (const [garbled, correct] of Object.entries(CHINESE_FIXES)) {
            if (content.includes(garbled)) {
                content = content.replace(new RegExp(garbled, 'g'), correct);
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
console.log('Starting to fix Chinese encoding issues in frontend-legacy HTML files...');
processFrontendLegacyFiles();
console.log('All frontend-legacy HTML files have been processed.');