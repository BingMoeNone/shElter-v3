#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复HTML文件的CSS变量
"""
import os
import re

def get_unified_css():
    """返回统一的CSS变量定义"""
    return '''        /* Wiki Platform V3 统一样式 */
        :root {
            --color-primary: #0D8ABC;
            --color-primary-dark: #096a8f;
            --color-primary-light: #3498db;
            --color-secondary: #9b59b6;
            --color-accent: #ff6b6b;
            --color-success: #27ae60;
            --color-danger: #e74c3c;
            --color-warning: #f39c12;
            --color-text: #ffffff;
            --color-text-muted: #a0a0a0;
            --color-background: #121212;
            --color-surface: #1a1a1a;
            --color-surface-hover: #2a2a2a;
            --color-border: #333333;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif, 'Microsoft YaHei', '微软雅黑', SimHei, '黑体', sans-serif;
            background-color: var(--color-background);
            color: var(--color-text);
            line-height: 1.6;
        }
'''

def fix_file(filepath):
    """修复单个HTML文件的CSS变量"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否需要修复
        if '--color-primary: #00ff9d' not in content and '--color-primary: #00ff88' not in content:
            print(f"跳过: {filepath} (无需修复)")
            return False

        # 查找:root部分的开始和结束
        root_start = content.find(':root {')
        if root_start == -1:
            print(f"跳过: {filepath} (未找到:root)")
            return False

        # 找到:root { 后面的内容
        root_block_start = content.find('{', root_start)
        
        # 找到对应的结束大括号
        brace_count = 1
        i = root_block_start + 1
        while i < len(content) and brace_count > 0:
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
            i += 1
        
        root_block_end = i

        # 找到* { 部分的开始和结束
        star_start = content.find('* {')
        if star_start == -1 or star_start > root_block_end:
            # 没有* {}，需要添加基础样式
            new_content = content[:root_block_end] + '\n' + get_unified_css()[4:]  # 去掉开头的缩进
        else:
            # 替换:root {} 块
            # 先找到* { 的位置来确定root块的结束
            star_brace_start = content.find('{', star_start)
            brace_count = 1
            i = star_brace_start + 1
            while i < len(content) and brace_count > 0:
                if content[i] == '{':
                    brace_count += 1
                elif content[i] == '}':
                    brace_count -= 1
                i += 1
            star_block_end = i

            # 替换从:root到*之前的内容
            new_content = content[:root_start] + get_unified_css() + content[star_block_end:]

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"已修复: {filepath}")
        return True
    except Exception as e:
        print(f"错误: {filepath} - {e}")
        return False

def main():
    """主函数"""
    frontend_dir = r'c:\BM_Program\shElter-v3\frontend-legacy'
    html_files = [f for f in os.listdir(frontend_dir) if f.endswith('.html')]
    
    fixed_count = 0
    for html_file in html_files:
        filepath = os.path.join(frontend_dir, html_file)
        if fix_file(filepath):
            fixed_count += 1
    
    print(f"\n完成! 共修复 {fixed_count} 个文件")

if __name__ == '__main__':
    main()
