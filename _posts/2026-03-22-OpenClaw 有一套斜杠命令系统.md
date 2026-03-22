OpenClaw 有一套斜杠命令系统，在聊天里直接输入 / 开头的指令就能控制小龙虾的行为。如果你是通过飞书机器人接入，是无法用这个斜杠命令的。最常用的几个：/status 查看当前状态。当小龙虾卡住不回复的时候，先发这个看看怎么回事。如果显示正在运行但一直没反应，通常是跑某个任务时卡住了，发 /stop 就能让它停下来恢复正常。这两个命令是排障第一步，记住它们。/compact 压缩上下文。聊太久 token 快满了，用这个压缩一下继续聊，压缩后它还记得之前的内容。/new 开启新会话，聊完一个话题想换下一个时用，避免上下文污染。比如你刚跟它聊完工作，现在想聊个人的事，开个新会话更干净。但我更建议通过拉不同群组的方式来开多窗口。（看后文）/model <名字> 切换模型。这是省钱的关键。简单问题用便宜模型（如 GLM、Kimi），复杂任务切强模型（如 Claude Opus），能省不少钱。/think <级别> 调整思考深度。日常闲聊用 off 就行，复杂问题开 high。/think off 关掉思考能省不少 token，日常闲聊不需要深度思考。以上命令，都比较好理解，自己玩一下就知道是什么意思了，我就不演示了。


官网命令行文档：https://docs.openclaw.ai/cli1. 基础配置 (General & Config)
命令说明openclaw onboard首次使用：启动交互式配置向导openclaw config get <key>查看配置项：读取指定配置的值openclaw config set <key> <value>设置配置项：修改指定配置的值openclaw doctor诊断修复：执行健康检查并自动修复环境问题2. 网关管理 (Gateway Management)
命令说明openclaw gateway启动网关（前台运行）openclaw gateway start后台启动网关服务 (Daemon)openclaw gateway stop停止网关服务openclaw gateway status查看网关当前运行状态openclaw logs查看网关实时运行日志3. 频道配置 (Channel Configuration)
命令说明openclaw channels list列出系统中所有频道openclaw channels status查看各频道的激活/在线状态openclaw channels enable <频道名>启用指定的频道openclaw channels disable <频道名>禁用指定的频道4. 插件与技能 (Plugins & Skills)

命令说明openclaw plugins list列出已安装的插件openclaw plugins install <插件名>安装新的功能插件openclaw skills list列出当前可用的技能库5. 控制面板 (Dashboard)
命令说明openclaw dashboard在浏览器中打开 Web 可视化控制面板


基础命令话不多说，先看最基本的几个命令，这几个是入门必会的：openclaw --version        # 查看当前安装版本
openclaw --help           # 查看帮助信息
openclaw onboard          # 全流程引导配置（首次安装必用）
openclaw onboard --force  # 强制重新初始化（配置搞乱了就用这个）配置管理配置管理是使用频率非常高的命令，特别是查看和修改模型、通道配置的时候：openclaw config list                    # 查看所有配置项
openclaw config get all                 # 获取全部配置详情
openclaw config get models              # 单独查看模型配置
openclaw config get channels            # 单独查看通道配置
openclaw config set gateway.port 18789  # 设置网关端口
openclaw config reset                   # 重置所有配置（慎用）模型管理模型是OpenClaw的核心，下面这几个命令帮你管理和排查模型问题：openclaw models list                          # 列出所有已配置模型
openclaw models status                        # 查看模型在线状态
openclaw models probe                         # 探测模型可用性（排障神器）
openclaw models set default "deepseek-v3.2"   # 设置默认模型通道管理通道就是OpenClaw和你聊天的桥梁，管理通道的命令如下：openclaw channels list            # 列出所有通道
openclaw channels status          # 查看通道连接状态
openclaw channels login telegram  # 登录Telegram通道
openclaw channels logout all      # 登出所有通道网关管理（最常用）好家伙，网关管理可以说是日常运维用得最多的命令了，启动、停止、重启、查状态，还能设置开机自启：openclaw gateway start     # 启动网关服务
openclaw gateway stop      # 停止网关服务
openclaw gateway restart   # 重启网关（改完配置后必用）
openclaw gateway status    # 查看网关运行状态
openclaw gateway install   # 安装为系统服务（开机自启，强烈推荐）
openclaw gateway uninstall # 卸载系统服务日志与调试遇到问题别慌，先看日志，再跑健康检查：openclaw logs          # 查看最近日志
openclaw logs -f       # 实时跟踪日志（像tail -f一样）
openclaw logs --error  # 只看错误日志
openclaw doctor        # 健康检查（自动诊断问题）
openclaw doctor --fix  # 自动修复发现的问题插件与技能管理OpenClaw的强大离不开丰富的插件和技能生态：openclaw plugins list              # 列出已安装插件
openclaw plugins install [插件名]   # 安装新插件
openclaw plugins enable [插件名]    # 启用插件
openclaw plugins disable [插件名]   # 禁用插件
openclaw skills list               # 列出所有技能
openclaw skills enable [技能名]     # 启用指定技能
openclaw skills disable [技能名]    # 禁用指定技能智能体管理OpenClaw支持创建多个智能体，不同智能体可以配置不同模型和技能：openclaw agent list            # 列出所有智能体
openclaw agent create myagent  # 创建新智能体
openclaw agent delete myagent  # 删除智能体
openclaw agent use main        # 切换到主智能体
openclaw agent chat "你好"     # 直接和智能体对话常用一键组合（完整启动流程）最后给大家一个从零启动的完整命令流程，按顺序执行就完事了：# 1. 检查配置
openclaw config get all

# 2. 探测模型是否可用
openclaw models probe

# 3. 检查通道状态
openclaw channels status

# 4. 安装为系统服务（首次执行）
openclaw gateway install

# 5. 启动网关
openclaw gateway start

# 6. 查看运行状态
openclaw gateway status

# 7. 实时查看日志
openclaw logs -f