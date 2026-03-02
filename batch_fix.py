# -*- coding: utf-8 -*-
import os
import sys

base = r'c:\BM_Program\shElter-v3\frontend-legacy'

# 乱码替换映射
rep = {
    '用户鍚': '用户名',
    '璇疯緭鍏': '请输入',
    '浠ュ姟': '请',
    '绔嬪嵆': '立即',
    '涓婁竴': '上一',
    '涓嬩竴': '下一',
    '椤?': '页',
    '绗?': '第',
    '加载涓': '加载中',
    '鍏抽敭': '关键',
    '璇嶆悳': '词搜索',
    '閾': '播',
    '鎾€': '播放',
    '閬€': '评',
    '閮€': '评',
    '杩欐槸涓€': '这是一个',
    '绠€浠': '简介',
    '鏍峰紡': '表单',
    '鍔ㄦ€': '动态',
    '娴佺生成': '动态生成',
    '浠€': '要',
    '鍏€': '成功',
    '閰€': '生',
    '鍙€': '可以',
    '鍐€': '对',
    '涓€': '一个',
    '閭€': '里',
    '澶€': '大',
    '闂€': '错误',
    '閯€': '验',
    '绐': '认证',
    '鍚': '用户',
    '浠': '请',
    '涓': '的',
    '璇': '请',
    '绾': '编',
    '濮': '页',
    '楂': '最',
    '浼': '删',
    '閮': '评',
    '閫': '通',
    '涔': '时',
    '澶': '发',
    '闂': '错',
    '閭': '邮',
    '闂': '错',
}

files = ['user-profile.html','tag-articles.html','search.html','register.html','profile.html','music.html','category-articles.html','admin-users.html','admin-moderation.html','admin-dashboard.html','edit-article.html','admin-comments.html']

for f in files:
    p = os.path.join(base, f)
    if os.path.exists(p):
        try:
            with open(p, 'r', encoding='utf-8') as fobj:
                c = fobj.read()
            orig = c
            
            # 移除"状态"前缀
            c = c.replace('状态', '')
            
            # 应用替换
            for w, r in rep.items():
                c = c.replace(w, r)
            
            if c != orig:
                with open(p, 'w', encoding='utf-8') as fobj:
                    fobj.write(c)
                print(f'Fixed: {f}')
        except Exception as e:
            print(f'Error {f}: {e}')

print('Done')
