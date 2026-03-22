# OpenClaw本地部署详细指南

## 🎯 部署目标
在韩立的本地电脑上部署OpenClaw，实现：
1. 本地AI助手服务
2. 与本地IM工具（微信、飞书、QQ）集成
3. 本地文件系统访问
4. 完全控制和安全的数据管理

---

## 📋 部署前检查清单

### 硬件要求检查：
- [ ] **CPU**：4核或以上（Intel i5/i7或AMD Ryzen 5/7）
- [ ] **内存**：16GB或以上（推荐32GB）
- [ ] **存储**：512GB SSD或以上
- [ ] **网络**：稳定互联网连接
- [ ] **操作系统**：Windows 10/11, macOS 10.15+, Ubuntu 20.04+

### 软件环境检查：
- [ ] **Node.js**：v18.0.0或更高版本
- [ ] **npm**：v8.0.0或更高版本
- [ ] **Git**：已安装并可正常使用
- [ ] **Python**：3.8或更高版本（可选，用于某些扩展）
- [ ] **Docker**：可选，用于容器化部署

### 权限检查：
- [ ] 管理员权限（安装软件需要）
- [ ] 防火墙配置权限
- [ ] 网络访问权限

---

## 🚀 部署步骤详解

### 阶段1：基础环境准备

#### 步骤1.1：检查当前系统
```bash
# Windows（PowerShell或CMD）
systeminfo | findstr /C:"OS Name" /C:"OS Version"
wmic cpu get name
wmic memorychip get capacity

# macOS
system_profiler SPHardwareDataType
sysctl -n hw.ncpu
sysctl -n hw.memsize

# Linux
cat /etc/os-release
nproc
free -h
```

#### 步骤1.2：安装Node.js
```bash
# Windows/macOS：从官网下载安装包
# https://nodejs.org/en/download/

# Linux（Ubuntu/Debian）
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# 验证安装
node --version  # 应该显示 v18.x.x 或更高
npm --version   # 应该显示 v8.x.x 或更高
```

#### 步骤1.3：安装Git
```bash
# Windows：从官网下载 Git for Windows
# https://git-scm.com/download/win

# macOS
brew install git

# Linux（Ubuntu/Debian）
sudo apt install git -y

# 验证安装
git --version
```

### 阶段2：OpenClaw安装

#### 步骤2.1：安装OpenClaw CLI
```bash
# 全局安装OpenClaw
npm install -g openclaw

# 验证安装
openclaw --version
```

#### 步骤2.2：创建工作空间
```bash
# 创建专用目录
mkdir ~/openclaw-workspace
cd ~/openclaw-workspace

# 初始化OpenClaw工作空间
openclaw init --workspace .

# 查看生成的文件
ls -la
```

#### 步骤2.3：基础配置
```bash
# 编辑基础配置文件
# Windows：使用记事本或VS Code
# macOS/Linux：使用vim或nano

# 配置示例：config/agents.json
{
  "default": {
    "model": "deepseek/deepseek-chat",
    "temperature": 0.7,
    "max_tokens": 2000
  }
}

# 配置示例：config/channels.json
{
  "local": {
    "type": "console",
    "enabled": true
  }
}
```

### 阶段3：启动和测试

#### 步骤3.1：启动网关服务
```bash
# 启动OpenClaw网关
openclaw gateway start

# 或以后台服务方式启动
openclaw gateway start --daemon

# 检查服务状态
openclaw gateway status
```

#### 步骤3.2：测试基础功能
```bash
# 测试命令行交互
openclaw chat

# 或通过HTTP接口测试
curl http://localhost:18789/health

# 预期响应：{"status":"ok","version":"2026.2.x"}
```

#### 步骤3.3：访问Web界面
```
打开浏览器访问：
http://localhost:18789

如果一切正常，您将看到OpenClaw的Web界面。
```

### 阶段4：IM工具集成

#### 步骤4.1：飞书集成配置

**A. 创建飞书应用**：
1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 登录您的飞书账号
3. 创建"企业自建应用"
4. 获取以下信息：
   - App ID
   - App Secret
   - Verification Token
   - Encrypt Key（可选）

**B. 配置OpenClaw**：
```bash
# 编辑飞书扩展配置
vim ~/openclaw-workspace/extensions/feishu/config.json
```

```json
{
  "app_id": "您的App ID",
  "app_secret": "您的App Secret",
  "verification_token": "您的Verification Token",
  "encrypt_key": "您的Encrypt Key（如果有）",
  "webhook": {
    "enabled": true,
    "path": "/feishu/webhook"
  }
}
```

**C. 配置飞书事件**：
1. 在飞书开放平台配置"事件订阅"
2. 请求地址：`http://您的公网IP:18789/feishu/webhook`
3. 启用事件：`im.message.receive_v1`
4. 保存并发布应用

#### 步骤4.2：微信集成配置（可选）

**使用微信网页版协议**：
```bash
# 安装微信集成扩展
cd ~/openclaw-workspace/extensions
git clone https://github.com/openclaw/wechat-integration.git wechat
cd wechat
npm install

# 配置微信
cp config.example.json config.json
# 编辑config.json，配置相关参数
```

**配置说明**：
```json
{
  "wechat": {
    "enabled": true,
    "login_method": "qrcode",
    "auto_reply": false,
    "forward_to_openclaw": true,
    "monitored_chats": ["工作群", "家人群"]
  }
}
```

#### 步骤4.3：QQ集成配置（可选）

```bash
# 安装QQ集成
cd ~/openclaw-workspace/extensions
git clone https://github.com/openclaw/qq-integration.git qq
cd qq
npm install
```

### 阶段5：文件系统集成

#### 步骤5.1：配置文件访问权限
```json
// ~/openclaw-workspace/config/permissions.json
{
  "file_access": {
    "enabled": true,
    "allowed_paths": [
      "~/Documents/",
      "~/Downloads/",
      "~/Desktop/OpenClawProjects/",
      "C:/Users/韩立/Documents/"  // Windows路径示例
    ],
    "restricted_paths": [
      "~/Library/",      // macOS系统文件
      "/etc/",           // Linux系统配置
      "C:/Windows/"      // Windows系统文件
    ],
    "max_file_size_mb": 50
  }
}
```

#### 步骤5.2：创建文件操作技能
```bash
# 创建自定义技能目录
mkdir -p ~/openclaw-workspace/skills/file-manager

# 创建技能配置文件
cat > ~/openclaw-workspace/skills/file-manager/SKILL.md << 'EOF'
# 文件管理器技能

## 功能
- 浏览本地文件
- 搜索文件内容
- 整理文件
- 文件格式转换

## 使用方式
```
查看文件 [路径]
搜索文件 [关键词]
整理文件夹 [路径]
```

## 权限
需要文件访问权限。
EOF
```

### 阶段6：安全配置

#### 步骤6.1：配置防火墙
```bash
# Windows防火墙
# 允许端口18789入站

# macOS
sudo pfctl -f /etc/pf.conf

# Linux (Ubuntu)
sudo ufw allow 18789/tcp
sudo ufw enable
```

#### 步骤6.2：配置访问控制
```json
// ~/openclaw-workspace/config/security.json
{
  "authentication": {
    "enabled": true,
    "api_keys": ["your-secret-api-key"],
    "require_auth_for_local": false
  },
  "rate_limiting": {
    "enabled": true,
    "requests_per_minute": 60
  },
  "audit_logging": {
    "enabled": true,
    "log_file": "audit.log",
    "retention_days": 30
  }
}
```

#### 步骤6.3：配置自动更新
```bash
# 创建更新脚本
cat > ~/openclaw-workspace/update.sh << 'EOF'
#!/bin/bash
echo "开始更新OpenClaw..."
cd ~/openclaw-workspace

# 备份当前配置
tar -czf backup-$(date +%Y%m%d).tar.gz config/ extensions/ skills/

# 更新OpenClaw CLI
npm update -g openclaw

# 更新扩展
for ext in extensions/*; do
  if [ -d "$ext" ] && [ -f "$ext/package.json" ]; then
    echo "更新扩展: $(basename $ext)"
    cd "$ext" && npm update
    cd -
  fi
done

echo "更新完成！"
EOF

chmod +x ~/openclaw-workspace/update.sh
```

### 阶段7：测试和验证

#### 步骤7.1：功能测试清单

**基础功能测试**：
- [ ] 网关服务启动正常
- [ ] Web界面可访问
- [ ] 命令行交互正常
- [ ] 健康检查接口正常

**IM集成测试**：
- [ ] 飞书消息接收测试
- [ ] 飞书消息回复测试
- [ ] 微信登录测试（如果配置）
- [ ] 微信消息转发测试

**文件系统测试**：
- [ ] 文件浏览功能测试
- [ ] 文件搜索功能测试
- [ ] 权限控制测试
- [ ] 大文件处理测试

**安全测试**：
- [ ] 防火墙配置验证
- [ ] 访问控制测试
- [ ] 审计日志记录测试
- [ ] 备份功能测试

#### 步骤7.2：性能测试
```bash
# 压力测试脚本示例
cat > ~/openclaw-workspace/performance-test.js << 'EOF'
const http = require('http');

const options = {
  hostname: 'localhost',
  port: 18789,
  path: '/health',
  method: 'GET'
};

let success = 0;
let failure = 0;

for (let i = 0; i < 100; i++) {
  const req = http.request(options, (res) => {
    if (res.statusCode === 200) {
      success++;
    } else {
      failure++;
    }
  });
  
  req.on('error', (e) => {
    failure++;
  });
  
  req.end();
}

setTimeout(() => {
  console.log(`测试完成：成功 ${success}，失败 ${failure}`);
  console.log(`成功率：${(success / 100 * 100).toFixed(2)}%`);
}, 2000);
EOF

node ~/openclaw-workspace/performance-test.js
```

### 阶段8：优化和调优

#### 步骤8.1：性能优化
```json
// ~/openclaw-workspace/config/performance.json
{
  "cache": {
    "enabled": true,
    "ttl_seconds": 300,
    "max_size_mb": 100
  },
  "concurrency": {
    "max_parallel_requests": 10,
    "queue_size": 50
  },
  "memory": {
    "max_heap_mb": 1024,
    "gc_interval_seconds": 60
  }
}
```

#### 步骤8.2：日志配置
```json
// ~/openclaw-workspace/config/logging.json
{
  "level": "info",
  "transports": [
    {
      "type": "file",
      "filename": "logs/openclaw.log",
      "maxsize": 10485760,
      "maxFiles": 10
    },
    {
      "type": "console",
      "colorize": true
    }
  ]
}
```

#### 步骤8.3：监控配置
```bash
# 安装监控工具
npm install prom-client express --save

# 创建监控端点
cat > ~/openclaw-workspace/monitor.js << 'EOF'
const express = require('express');
const client = require('prom-client');

const app = express();
const register = new client.Registry();

// 添加默认指标
client.collectDefaultMetrics({ register });

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

app.listen(9090, () => {
  console.log('监控服务运行在 http://localhost:9090/metrics');
});
EOF
```

### 阶段9：故障排除

#### 常见问题及解决方案：

**问题1：端口被占用**
```bash
# 检查端口占用
netstat -ano | findstr :18789  # Windows
lsof -i :18789                 # macOS/Linux

# 解决方案：修改端口
openclaw gateway start --port 18790
```

**问题2：权限不足**
```bash
# Windows：以管理员身份运行
# macOS/Linux：使用sudo
sudo openclaw gateway start
```

**问题3：Node.js版本不兼容**
```bash
# 检查Node.js版本
node --version

# 升级Node.js
# Windows/macOS：重新下载安装包
# Linux：使用nvm管理版本
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

**问题4：内存不足**
```bash
# 查看内存使用
top  # 或 htop, taskmgr

# 解决方案：
# 1. 增加虚拟内存
# 2. 优化OpenClaw配置
# 3. 升级硬件
```

**问题5：网络连接问题**
```bash
# 测试本地连接
curl http://localhost:18789/health

# 测试外部访问（如果有公网IP）
curl http://您的公网IP:18789/health

# 检查防火墙
# Windows：检查Windows Defender防火墙
# macOS：检查系统偏好设置->安全->防火墙
# Linux：sudo ufw status
```

### 阶段10：维护和备份

#### 步骤10.1：创建备份脚本
```bash
cat > ~/openclaw-workspace/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/path/to/backup/folder"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/openclaw-backup-$DATE.tar.gz"

echo "开始备份OpenClaw工作空间..."

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 备份重要文件
tar -czf "$BACKUP_FILE" \
  ~/openclaw-workspace/config/ \
  ~/openclaw-workspace/extensions/ \
  ~/openclaw-workspace/skills/ \
  ~/openclaw-workspace/workspace/ \
  ~/openclaw-workspace/*.json \
  ~/openclaw-workspace/*.md

# 备份数据库（如果有）
if [ -f ~/openclaw-workspace/data/database.sqlite ]; then
  cp ~/openclaw-workspace/data/database.sqlite "$BACKUP_DIR/database-$DATE.sqlite"
fi

echo "备份完成：$BACKUP_FILE"
echo "备份大小：$(du -h "$BACKUP_FILE" | cut -f1)"

# 清理旧备份（保留最近7天）
find "$BACKUP_DIR" -name "openclaw-backup-*.tar.gz" -mtime +7 -delete
find "$BACKUP_DIR" -name "database-*.sqlite" -mtime +7 -delete
EOF

chmod +x ~/openclaw-workspace/backup.sh
```

#### 步骤10.2：设置自动备份
```bash
# Linux/macOS：使用cron
crontab -e
# 添加以下行（每天凌晨2点备份）
0 2 * * * /home/韩立/openclaw-workspace/backup.sh

# Windows：使用任务计划程序
# 1. 打开"任务计划程序"
# 2. 创建基本任务
# 3. 设置触发器：每天2:00 AM
# 4. 操作：启动程序，选择backup.sh
```

#### 步骤10.3：创建恢复脚本
```bash
cat > ~/openclaw-workspace/restore.sh << 'EOF'
#!/bin/bash
if [ -z "$1" ]; then
  echo "使用方法: $0 <备份文件>"
  echo "示例: $0 /path/to/backup/openclaw-backup-20260301.tar.gz"
  exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
  echo "错误：备份文件不存在: $BACKUP_FILE"
  exit 1
fi

echo "警告：这将覆盖当前的OpenClaw配置！"
read -p "是否继续？(y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "恢复操作已取消"
  exit 0
fi

echo "开始恢复OpenClaw配置..."

# 停止OpenClaw服务
openclaw gateway stop 2>/dev/null || true

# 备份当前配置
CURRENT_BACKUP="/tmp/openclaw-current-$(date +%s).tar.gz"
tar -czf "$CURRENT_BACKUP" ~/openclaw-workspace/config/ ~/openclaw-workspace/extensions/ ~/openclaw-workspace/skills/

# 解压备份文件
tar -xzf "$BACKUP_FILE" -C ~/openclaw-workspace/

echo "恢复完成！"
echo "当前配置已备份到: $CURRENT_BACKUP"
echo "请重新启动OpenClaw服务: openclaw gateway start"
EOF

chmod +x ~/openclaw-workspace/restore.sh
```

---

## 📊 部署进度跟踪表

### 部署阶段跟踪：
| 阶段 | 任务 | 状态 | 预计时间 | 实际时间 | 备注 |
|------|------|------|----------|----------|------|
| 1 | 环境准备 | □ | 30分钟 | | |
| 2 | OpenClaw安装 | □ | 20分钟 | | |
| 3 | 启动测试 | □ | 15分钟 | | |
| 4 | IM工具集成 | □ | 60分钟 | | |
| 5 | 文件系统集成 | □ | 30分钟 | | |
| 6 | 安全配置 | □ | 30分钟 | | |
| 7 | 测试验证 | □ | 45分钟 | | |
| 8 | 优化调优 | □ | 30分钟 | | |
| 9 | 故障排除 | □ | 可变 | | |
| 10 | 维护备份 | □ | 20分钟 | | |

**总预计时间**：约4小时

---

## 🎯 部署成功标准

### 必须完成：
- [ ] OpenClaw网关服务正常启动
- [ ] Web界面可正常访问
- [ ] 基础对话功能正常
- [ ] 文件访问功能正常
- [ ] 至少一个IM工具集成正常

### 建议完成：
- [ ] 飞书集成配置完成
- [ ] 微信集成配置完成（可选）
- [ ] 安全配置完成
- [ ] 备份机制设置完成
- [ ] 监控配置完成

### 高级功能（可选）：
- [ ] 自动化工作流配置
- [ ] 自定义技能开发
- [ ] 多用户支持配置
- [ ] 高级监控和告警

---

## ⚠️ 注意事项

### 安全注意事项：
1. **不要**在配置文件硬编码敏感信息（API密钥等）
2. **务必**配置防火墙，只开放必要端口
3. **定期**更新OpenClaw和依赖包
4. **启用**操作审计日志
5. **设置**定期备份

### 性能注意事项：
1. 监控内存使用，避免内存泄漏
2. 配置合理的缓存策略
3. 优化数据库查询（如果有）
4. 定期清理日志文件

### 维护注意事项：
1. 定期检查服务状态
2. 监控磁盘空间使用
3. 查看错误日志
4. 测试备份恢复流程

---

## 🔧 故障排除工具箱

### 诊断命令：
```bash
# 检查服务状态
openclaw gateway status

# 查看日志
tail -f ~/openclaw-workspace/logs/openclaw.log

# 检查端口占用
netstat -tulpn | grep :18789

# 检查进程
ps aux | grep openclaw

# 检查网络连接
curl -v http://localhost:18789/health
```

### 重置命令：
```bash
# 重置配置（危险！备份先！）
openclaw init --force --workspace ~/openclaw-workspace

# 重新安装
npm uninstall -g openclaw
npm install -g openclaw

# 清理缓存
npm cache clean --force
```

### 调试模式：
```bash
# 启动调试模式
openclaw gateway start --debug

# 查看详细日志
openclaw gateway start --log-level debug

# 测试特定功能
openclaw test --all
```

---

## 📞 支持资源

### 官方资源：
1. **OpenClaw文档**：https://docs.openclaw.ai
2. **GitHub仓库**：https://github.com/openclaw/openclaw
3. **Discord社区**：https://discord.gg/clawd
4. **问题反馈**：GitHub Issues

### 社区资源：
1. **技术博客**：相关技术博客和教程
2. **Stack Overflow**：OpenClaw相关问答
3. **Reddit社区**：r/openclaw
4. **中文社区**：相关技术论坛

### 本地支持：
1. **系统日志**：`~/openclaw-workspace/logs/`
2. **配置文档**：本指南及相关配置文件
3. **备份文件**：定期备份的配置和数据

---

## 🎉 部署完成确认

### 最终检查清单：
- [ ] 所有必须完成的项目都已勾选
- [ ] 服务运行稳定超过24小时
- [ ] 关键功能测试通过
- [ ] 安全配置检查完成
- [ ] 备份恢复测试通过
- [ ] 文档整理完成

### 部署成功标志：
1. ✅ OpenClaw服务稳定运行
2. ✅ IM工具集成正常工作
3. ✅ 文件访问功能正常
4. ✅ 安全配置生效
5. ✅ 监控和备份运行正常

---

**文档版本**：v1.0  
**创建时间**：2026年3月1日  
**适用系统**：Windows/macOS/Linux  
**目标用户**：韩立  
**部署类型**：本地单机部署

**下一步**：按照本指南逐步执行，遇到问题时参考故障排除部分。