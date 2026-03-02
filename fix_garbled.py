#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复HTML文件中的乱码
"""
import os
import re

def fix_garbled(text):
    """修复常见乱码"""
    replacements = {
        # 常见乱码映射
        '鈿狅笍': '⚠️',
        '馃彿': '📂',
        '馃摑': '📂',
        '馃搨': '📂',
        '馃攳': '🔍',
        '馃懁': '👤',
        '馃搮': '📅',
        '馃敆': '📤',
        '馃憗': '👁️',
        '馃挰': '💬',
        '馃摑': '📝',
        '管理员?,': '管理员",
        '鐗堜富': '版主',
        '娴嬭瘯用户名': '测试用户',
        '鏅€€€€€€€?,': '普通用户",
        '鍚庣寮€鍙戞渶浣冲疄璺?': '后端开发最佳实践',
        '鎴戞湁涓嶅悇鐨勭湅娉?': '我有不同的看法...',
        '鎰熻阿鍒嗕韩锛屽鍒颁簡寰堝': '感谢分享，学到了很多',
        'FastAPI绠€浠?/h2>': 'FastAPI简介</h2>',
        'FastAPI鏄€€€€€€€?,': 'FastAPI是一个现代化的Python Web框架...',
        '閿欒€€€€€€€?,': '错误：',
        '绛惧悕涓€€€€€€€?,': '签名中...',
    }
    
    # 处理特殊的多字节乱码
    # "鏅€€€€€€€?" -> "普通用户"
    text = re.sub(r'鏅\$+€+€+€+€+\?+[,"]', '普通用户",', text)
    
    # 处理 "鍚庣€€€€€€€?, " 类似的乱码
    text = re.sub(r'鍚庣\$+€+€+€+€+\?+[,"]', '后端",', text)
    
    # "鏅€€€€€€€?, " -> "普通用户"
    text = re.sub(r'鏅€€€€€€€\?+[,"]', '普通用户",', text)
    
    # 简单的替换
    for garbled, correct in replacements.items():
        text = text.replace(garbled, correct)
    
    # 处理 HTML 实体编码的问题
    text = text.replace('&gt;', '>')
    text = text.replace('&lt;', '<')
    
    return text

def process_file(filepath):
    """处理单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        content = fix_garbled(content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"修复: {filepath}")
            return True
        return False
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
        if process_file(filepath):
            fixed_count += 1
    
    print(f"\n完成! 共修复 {fixed_count} 个文件")

if __name__ == '__main__':
    main()
