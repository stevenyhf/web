完整的 OpenClaw 接入飞书的详细步骤：

OpenClaw 接入飞书详细指南

一、准备工作

1.1 飞书开发者账号准备

1. 注册飞书开放平台账号
  • 访问 飞书开放平台 (https://open.feishu.cn/)
  • 使用企业管理员账号登录
2. 创建企业自建应用
  • 进入"开发者后台"
  • 点击"创建企业自建应用"
  • 填写应用信息：
    • 应用名称：OpenClaw AI Assistant
    • 应用描述：AI智能助手
    • 应用图标：可选

1.2 获取必要的凭证

需要获取以下凭证：

• App ID：应用唯一标识
• App Secret：应用密钥
• Encryption Key：事件加密密钥（可选）
• Verification Token：验证令牌（可选）

二、飞书应用配置

2.1 权限配置

在应用配置页面，添加以下权限：

必选权限：

• 获取用户 user_id：contact:user.id:readonly
• 获取用户基本信息：contact:user.base:readonly
• 获取用户邮箱：contact:user.email:readonly
• 获取用户手机号：contact:user.phone:readonly
• 获取用户所在部门信息：contact:user.department:readonly
• 获取部门信息：contact:department.base:readonly
• 获取部门用户列表：contact:department.user:readonly
• 获取部门列表：contact:department.list:readonly
• 获取自定义机器人消息：im:message
• 发送消息：im:message:send_as_bot
• 接收消息：im:message:receive
• 上传图片：im:image
• 获取群组信息：im:chat:readonly
• 获取与发送单聊、群组消息：im:message:readonly

文档相关权限（如果需要）：

• 云文档读权限：drive:drive:readonly
• 云文档写权限：drive:drive
• 知识库读权限：wiki:wiki:readonly
• 知识库写权限：wiki:wiki
• 多维表格读权限：bitable:record:readonly
• 多维表格写权限：bitable:record

2.2 事件订阅配置

1. 启用事件订阅
2. 添加事件：
  • im.message.receive_v1（接收消息）
  • 其他需要的事件
3. 配置请求地址：https://你的域名或IP:端口/feishu/webhook
或使用 OpenClaw Gateway 地址

2.3 安全设置

1. 启用消息卡片请求网址校验
2. 配置加密密钥（如果需要）

三、OpenClaw 配置

3.1 安装飞书扩展（如果未安装）

# 如果飞书扩展未安装，需要安装
npm install @openclaw/feishu

3.2 配置 OpenClaw

方法一：使用配置向导

# 运行配置向导
openclaw configure --section channels

# 选择 Feishu 进行配置
# 输入以下信息：
# - App ID
# - App Secret
# - Encryption Key（如有）
# - Verification Token（如有）

方法二：手动编辑配置文件

编辑 ~/.openclaw/config.yaml：

workspace: ~/.openclaw/workspace
model: deepseek/deepseek-chat

gateway:
  mode: local
  port: 18789
  bind: 0.0.0.0  # 如果需要外部访问

channels:
  feishu:
    enabled: true
    app_id: "你的App ID"
    app_secret: "你的App Secret"
    encrypt_key: "你的Encryption Key"  # 可选
    verification_token: "你的Verification Token"  # 可选
    # 其他配置项...

3.3 启动 Gateway

# 重启 Gateway 服务
openclaw gateway restart

# 查看 Gateway 状态
openclaw gateway status

四、网络配置

4.1 本地开发环境

如果需要公网访问，可以使用：

选项一：Ngrok（推荐用于测试）

# 安装 ngrok
ngrok http 18789

# 将生成的 https URL 配置到飞书事件订阅

选项二：Cloudflare Tunnel

# 安装 cloudflared
cloudflared tunnel --url http://localhost:18789

选项三：服务器部署

如果部署在服务器上：

1. 确保防火墙开放 18789 端口
2. 配置域名解析
3. 配置 SSL 证书（HTTPS）

4.2 端口转发配置

# 如果需要外部访问，修改绑定地址
# 在 config.yaml 中：
gateway:
  bind: 0.0.0.0  # 允许所有IP访问
  port: 18789

五、测试连接

5.1 验证配置

# 检查飞书通道状态
openclaw channels list

# 应该显示：Feishu default: configured, enabled

5.2 飞书应用发布

1. 在飞书开放平台提交应用版本
2. 申请发布
3. 企业管理员审核通过

5.3 测试消息

1. 在飞书中找到你的应用
2. 发送测试消息
3. 检查 OpenClaw 是否收到并回复

六、高级配置

6.1 多租户配置

如果需要支持多个飞书租户：

channels:
  feishu:
    enabled: true
    tenants:
      - tenant_key: "tenant1"
        app_id: "app_id_1"
        app_secret: "app_secret_1"
      - tenant_key: "tenant2"
        app_id: "app_id_2"
        app_secret: "app_secret_2"

6.2 自定义消息处理器

创建自定义处理器：

// 在扩展中创建自定义处理器
module.exports = {
  name: 'feishu-custom',
  async onMessage(message, context) {
    // 自定义处理逻辑
    if (message.text.includes('特定关键词')) {
      return { text: '自定义回复' };
    }
    // 默认处理
    return null;
  }
};

6.3 飞书工具使用

OpenClaw 已经集成了飞书工具，可以直接使用：

# 在对话中可以直接使用飞书工具
# 例如：读取飞书文档、管理云盘等

七、故障排除

7.1 常见问题

问题1：Gateway 无法启动

# 检查端口占用
netstat -tlnp | grep 18789

# 查看日志
openclaw gateway logs

问题2：飞书消息无法接收

1. 检查事件订阅配置
2. 验证请求地址可访问
3. 检查权限配置
4. 查看 Gateway 日志

问题3：权限不足

1. 检查应用权限是否齐全
2. 重新申请权限并发布新版本
3. 确保管理员已审核通过

7.2 日志查看

# 查看 Gateway 日志
openclaw gateway logs

# 查看特定通道日志
openclaw gateway logs --channel feishu

八、安全建议

8.1 凭证安全

1. 不要将 App Secret 提交到代码仓库
2. 使用环境变量存储敏感信息
3. 定期轮换密钥

8.2 访问控制

1. 限制可访问的 IP 范围
2. 启用飞书的安全设置
3. 监控异常访问

8.3 数据保护

1. 遵守数据最小化原则
2. 加密存储敏感数据
3. 定期清理日志

九、最佳实践

9.1 开发环境

1. 使用测试企业进行开发
2. 配置开发、测试、生产环境
3. 使用版本控制管理配置

9.2 监控告警

1. 监控 Gateway 运行状态
2. 设置消息处理异常告警
3. 定期检查服务健康状态

9.3 性能优化

1. 合理配置 Gateway 资源
2. 使用连接池管理数据库连接
3. 优化消息处理逻辑

十、当前状态检查

根据我检查的结果，你的 OpenClaw 已经：

✅ 飞书工具已注册：

• feishu_doc：文档操作工具
• feishu_wiki：知识库工具
• feishu_drive：云盘工具
• feishu_bitable：多维表格工具

mr123, [2026/2/26 11:41]
✅ 飞书通道已配置并启用

❓ 需要确认：

1. 飞书应用的详细配置（App ID、Secret 等）
2. 网络访问配置
3. 事件订阅配置

下一步建议

1. 检查飞书应用配置：确保已获取所有必要凭证
2. 配置网络访问：确保飞书可以访问你的 Gateway
3. 测试连接：发送测试消息验证集成
4. 配置权限：根据需求调整应用权限

需要我帮你检查具体的配置细节，或者指导你完成某个特定步骤吗？