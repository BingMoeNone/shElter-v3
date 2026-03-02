# 快速修复脚本 - 直接生成正确的HTML文件
import os

base_dir = r"c:\BM_Program\shElter-v3\frontend-legacy"

# 通用修复函数 - 移除所有"状态"前缀和乱码字符
def fix_content(content):
    # 移除"状态"前缀（这是编码损坏的结果）
    content = content.replace('状态', '')
    return content

# 检查并修复文件
files_to_check = [
    "user-profile.html",
    "tag-articles.html", 
    "search.html",
    "register.html",
    "profile.html",
    "music.html",
    "category-articles.html",
    "admin-users.html",
    "admin-moderation.html",
    "admin-dashboard.html",
    "admin-articles.html",
    "edit-article.html",
    "admin-comments.html",
]

for filename in files_to_check:
    filepath = os.path.join(base_dir, filename)
    if os.path.exists(filepath):
        try:
            # 尝试用不同编码读取
            content = None
            for encoding in ['utf-8', 'utf-8-sig', 'gbk', 'gb2312']:
                try:
                    with open(filepath, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except:
                    continue
            
            if content:
                # 检查是否有乱码
                has_garbled = '状态' in content or '鍚' in content or '浠' in content
                
                if has_garbled:
                    fixed = fix_content(content)
                    if fixed:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(fixed)
                        print(f"Fixed: {filename}")
                    else:
                        print(f"Failed to fix: {filename}")
                else:
                    print(f"No garbled text: {filename}")
            else:
                print(f"Could not read: {filename}")
        except Exception as e:
            print(f"Error with {filename}: {e}")

print("Done!")
