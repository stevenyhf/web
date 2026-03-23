怎样将_posts中的.md转换成_site里面的.html文件并完成提交到github?

要把 _posts 目录下的 Markdown（*.md）文件编译成 _site 目录里的 HTML，并把生成的结果一次性提交到 GitHub，常见的做法是使用 Jekyll（或其他静态站点生成器）配合 Git 命令。下面给出完整的操作步骤，适用于已经有一个 Jekyll 项目、并且已经把代码托管在 GitHub 上的情况。如果你使用的是其他生成器（如 Hugo、Hexo），思路基本相同，只需把对应的构建命令换掉即可。
1️⃣ 前置条件
条件
检查/安装方法
Git 已安装
git --version
Ruby（≥2.7）和 Bundler
ruby -v、gem list bundler（没有则 gem install bundler）
Jekyll
jekyll -v（没有则 gem install jekyll 或在项目里使用 bundle install）
GitHub 账户 & SSH key
ssh -T git@github.com，确保能免密码 push
项目已克隆
git clone git@github.com:yourname/yourrepo.git
提示：如果你已经在本地有项目文件夹（含 _posts、_config.yml、Gemfile），直接在该文件夹下执行后面的命令即可。
2️⃣ 生成 HTML（本地构建）
在项目根目录执行：
# 如果项目使用 Bundler（Gemfile 中指定了 jekyll）
bundle exec jekyll build   # 默认输出到 _site 目录

# 如果没有 Bundler，直接调用 jekyll
jekyll build
结果：所有 _posts/*.md 会被解析为对应的 .html，并放进 _site 目录（包括其它资源如 CSS、JS、图片等）。
检查：ls _site、打开 index.html 或直接在浏览器里打开 _site 中的文件，确认渲染无误。
3️⃣ 将生成的 HTML 提交到 GitHub
3.1 只提交 _site 产物（常见做法：把 _site 单独作为分支）
推荐：大多数项目不把编译产物直接提交到 main（因为每次构建都可以在 CI 上完成），而是使用 gh-pages、site 或 build 等专用分支。
方法 A：使用 gh-pages 分支（GitHub Pages 常用）
# 1️⃣ 切到或创建 gh-pages 分支（首次执行会创建）
git checkout --orphan gh-pages
git rm -rf .   # 清空旧内容（如果有）

# 2️⃣ 把 _site 内容拷贝到根目录（或保持在子目录）
cp -r _site/* .

# 3️⃣ 提交
git add .
git commit -m "Update site: $(date +"%Y-%m-%d %H:%M")"

# 4️⃣ 推送（强制推送覆盖旧的 gh-pages 内容）
git push -f origin gh-pages
方法 B：把 _site 直接提交到 main（如果你想把产物和源码放在同一分支）
# 1️⃣ 确保在工作分支
git checkout main
git pull

# 2️⃣ 把生成的文件加入暂存区（只加入 _site）
git add _site

# 3️⃣ 提交
git commit -m "Build site @ $(date +"%Y-%m-%d %H:%M")"

# 4️⃣ 推送
git push origin main
注意：如果 .gitignore 中已经把 _site 排除，需要先把对应行注释掉或删除，否则 git add _site 不会起作用。
3.2 自动化（可选）
把上面的流程写进一个小脚本 deploy.sh，以后只需要：
./deploy.sh

示例脚本（放在项目根目录）：
#!/usr/bin/env bash
set -e

# 1. 构建
bundle exec jekyll build   # 或 jekyll build

# 2. 切换到 gh-pages 并强制推送
git checkout gh-pages || git checkout --orphan gh-pages
git rm -rf .  # 清空
cp -r _site/* .
git add .
git commit -m "Deploy $(date '+%Y-%m-%d %H:%M')"
git push -f origin gh-pages

# 回到主分支（如果需要）
git checkout main

记得给脚本执行权限：
chmod +x deploy.sh
4️⃣ 完整示例（一步一步）
# ① 进入项目目录
cd /path/to/your/jekyll_repo

# ② 确认依赖
bundle install   # 安装 Gemfile 中的依赖

# ③ 本地构建
bundle exec jekyll build   # 生成 _site

# ④ 提交到 gh-pages
git checkout --orphan gh-pages   # 创建 gh-pages（首次）
git rm -rf .                     # 清理旧文件
cp -r _site/* .                  # 把生成的文件拷贝到根目录
git add .
git commit -m "Site update: $(date)"
git push -f origin gh-pages       # 强制推送
git checkout main                 # 返回主分支
小技巧：如果你在 GitHub 上启用了 GitHub Actions，可以把构建+推送全放到 CI 中，这样本地只需要 git push 源代码，CI 自动完成构建并更新 gh-pages。
5️⃣ 常见问题排查
症状
可能原因
解决办法
_site 里没有 HTML
jekyll build 报错或 Gemfile 缺少 jekyll
查看终端输出，确保 bundle exec jekyll build 正常完成
推送被拒绝（non‑fast‑forward）
远程 gh-pages 有新提交
用 git push -f 强制覆盖，或先 git pull --rebase origin gh-pages
GitHub Pages 仍显示旧页面
缓存或分支未设置为 gh-pages（或 docs/）
在仓库 Settings → Pages，确认 Source 指向 gh-pages 并根目录
.gitignore 排除 _site
.gitignore 中有 _site/ 行
暂时注释或删除该行，再执行 git add _site
SSH 推送需要密码
未配置 SSH key
参考 GitHub SSH 配置文档，生成并添加公钥到 GitHub
6️⃣ 小结
构建：jekyll build → 生成 _site。
提交：把 _site 内容推送到专用分支（如 gh-pages），或直接提交到主分支。
自动化：写脚本或 CI（GitHub Actions）让部署一步到位。
按上述步骤操作，你就能把 _posts/*.md 转成 _site/*.html 并顺利提交到 GitHub。祝部署顺利 🚀!