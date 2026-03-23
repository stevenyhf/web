import os
import re

# 配置：需要处理的 HTML 文件目录
html_dir = '.'  # 当前目录，或修改为你的路径

# 配置：需要排除的文件
exclude_files = ['add_frontmatter.py', 'nav.js', 'index.html']

def get_title_from_html(content):
    """从 HTML 中提取标题"""
    # 尝试从 <title> 标签提取
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    if title_match:
        return title_match.group(1).strip()
    
    # 尝试从 <h1> 标签提取
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    if h1_match:
        # 去除 HTML 标签
        title = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
        return title
    
    return "未命名页面"

def add_frontmatter(filepath):
    """给 HTML 文件添加 Front Matter"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已有 Front Matter
    if content.strip().startswith('---'):
        print(f"⏭️  跳过 (已有 Front Matter): {filepath}")
        return
    
    # 提取标题
    title = get_title_from_html(content)
    
    # 生成 Front Matter
    frontmatter = f"""---
title: {title}
---

"""
    
    # 插入到文件开头
    new_content = frontmatter + content
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 已处理：{filepath} (标题：{title})")

def main():
    print("🚀 开始批量添加 Front Matter...\n")
    
    count = 0
    for filename in os.listdir(html_dir):
        if filename.endswith('.html') or filename.endswith('.htm'):
            if filename not in exclude_files:
                filepath = os.path.join(html_dir, filename)
                if os.path.isfile(filepath):
                    add_frontmatter(filepath)
                    count += 1
    
    print(f"\n🎉 完成！共处理 {count} 个文件。")

if __name__ == '__main__':
    main()