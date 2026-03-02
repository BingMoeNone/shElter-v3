# -*- coding: utf-8 -*-
"""
检测Python文件中的乱码字符
"""
import os
import re

def is_garbled(text):
    """检测文本是否为乱码（GBK编码被误读）"""
    try:
        text.encode('gbk')
        return False
    except:
        return True

def has_chinese(text):
    """检测是否包含中文字符"""
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    return bool(chinese_pattern.search(text))

def check_file(filepath):
    """检查单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')
        garbled_lines = []

        for i, line in enumerate(lines, 1):
            # 跳过注释行
            if line.strip().startswith('#'):
                continue

            # 检查是否有乱码（排除UTF-8中文字符）
            # 乱码通常是非ASCII且不能被正确识别的字符
            for char in line:
                if ord(char) > 127:
                    # 检查是否是有效的中文字符
                    if not ('\u4e00' <= char <= '\u9fff'):
                        # 这可能是乱码
                        garbled_lines.append((i, line.strip()[:80]))
                        break

        return garbled_lines
    except Exception as e:
        return []

def main():
    src_dir = r'c:\BM_Program\shElter-v3\backend\src'
    all_garbled = {}

    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                garbled_lines = check_file(filepath)
                if garbled_lines:
                    all_garbled[filepath] = garbled_lines

    if all_garbled:
        print("发现乱码的文件：")
        for filepath, lines in all_garbled.items():
            print(f"\n{filepath}:")
            for line_num, line in lines[:3]:
                print(f"  行 {line_num}: {line}")
    else:
        print("未发现乱码字符！")

if __name__ == '__main__':
    main()
