# 腾讯云服务器OpenClaw网关连接问题专项解决方案

## 🔍 问题诊断

### 当前情况：
- **服务器**：腾讯云服务器（IP: 43.162.103.96）
- **端口**：18789
- **问题**：能访问页面，但显示"已断开与网关的连接"
- **已尝试**：多种方案仍无效

### 问题分析：
1. **页面能访问** → HTTP服务正常
2. **连接断开** → WebSocket连接失败
3. **云服务器环境** → 有特殊网络和安全限制

## 🎯 云服务器特有问题

### 1. 腾讯云安全组限制
腾讯云默认有严格的安全组规则，可能阻止了WebSocket连接。

### 2. 跨域问题（CORS）
云服务器访问可能涉及跨域问题。

### 3. WebSocket协议支持
某些云环境对WebSocket支持不完整。

### 4. 反向代理配置
可能需要Nginx反向代理来正确处理WebSocket。

## 🚀 解决方案（按优先级）

### 方案一：检查并配置腾讯云安全组（最重要）

#### 步骤1：登录腾讯云控制台
1. 访问：https://console.cloud.tencent.com/lighthouse
2. 找到你的服务器实例

#### 步骤2：检查安全组规则
1. 进入"安全组"配置
2. 查看入站规则（Inbound Rules）

#### 步骤3：添加必要的端口规则
需要开放的端口：
- **TCP 18789**：OpenClaw HTTP/WebSocket端口
- **TCP 443**：如果要用HTTPS
- **TCP 80**：如果要用HTTP

#### 步骤4：配置安全组规则
```bash
# 规则示例：
协议类型：TCP
端口范围：18789
来源：0.0.0.0/0（或限制为你的IP）
策略：允许
```

#### 步骤5：验证端口开放
```bash
# 在服务器上检查端口监听
netstat -tlnp | grep 18789

# 从外部测试端口
telnet 43.162.103.96 18789
# 或
nc -zv 43.162.103.96 18789
```

### 方案二：配置Nginx反向代理（推荐）

#### 为什么需要Nginx：
1. 正确处理WebSocket升级
2. 解决跨域问题
3. 提供HTTPS支持
4. 负载均衡和缓存

#### 步骤1：安装Nginx
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx -y

# CentOS
sudo yum install nginx -y
```

#### 步骤2：配置Nginx反向代理
创建配置文件：
```bash
sudo nano /etc/nginx/sites-available/openclaw
```

配置文件内容：
```nginx
server {
    listen 80;
    server_name 43.162.103.96;  # 或你的域名
    
    # 静态文件服务（如果有）
    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket支持
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
        
        # CORS头
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
        add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
    }
    
    # WebSocket特定路径
    location /ws/ {
        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        
        # WebSocket超时设置
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
}
```

#### 步骤3：启用配置
```bash
# 创建符号链接
sudo ln -s /etc/nginx/sites-available/openclaw /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx
```

#### 步骤4：修改OpenClaw配置
```bash
# 告诉OpenClaw使用正确的地址
openclaw config set gateway.bind "127.0.0.1:18789"
openclaw config set gateway.controlUi.allowInsecureAuth true

# 重启OpenClaw
openclaw gateway restart
```

#### 步骤5：测试访问
现在通过Nginx访问：
- `http://43.162.103.96`（端口80）
- 或配置域名后访问

### 方案三：配置HTTPS（生产环境必须）

#### 步骤1：获取SSL证书
```bash
# 使用Certbot获取免费证书
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

#### 步骤2：更新Nginx配置支持HTTPS
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # SSL配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # 其他配置同上
    location / {
        proxy_pass http://127.0.0.1:18789;
        # ... 其他配置
    }
}

# HTTP重定向到HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

### 方案四：OpenClaw特定配置调整

#### 步骤1：检查当前配置
```bash
# 查看完整配置
openclaw config get gateway

# 查看WebSocket配置
openclaw config get gateway.websocket
```

#### 步骤2：调整WebSocket配置
```bash
# 增加WebSocket超时时间
openclaw config set gateway.websocket.timeout 86400000

# 允许跨域
openclaw config set gateway.controlUi.cors true

# 设置允许的来源
openclaw config set gateway.controlUi.allowedOrigins "http://43.162.103.96,http://localhost"

# 启用详细日志
openclaw config set gateway.logLevel debug
```

#### 步骤3：重启并检查
```bash
# 重启服务
openclaw gateway restart

# 查看日志
openclaw logs --follow

# 检查状态
openclaw gateway status --json
```

## 🔧 详细诊断步骤

### 1. 网络诊断
```bash
# 检查服务器网络
ping 43.162.103.96

# 检查端口开放
nmap -p 18789 43.162.103.96

# 检查防火墙
sudo ufw status
sudo firewall-cmd --list-all  # CentOS
```

### 2. OpenClaw服务诊断
```bash
# 查看服务状态
systemctl status openclaw

# 查看进程
ps aux | grep openclaw

# 查看端口占用
ss -tlnp | grep 18789

# 测试本地连接
curl http://127.0.0.1:18789
```

### 3. WebSocket测试
```bash
# 使用wscat测试WebSocket
npm install -g wscat
wscat -c ws://43.162.103.96:18789

# 或使用curl测试WebSocket握手
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Host: 43.162.103.96:18789" -H "Origin: http://43.162.103.96" http://43.162.103.96:18789
```

### 4. 浏览器控制台检查
1. 打开浏览器开发者工具（F12）
2. 访问 `http://43.162.103.96:18789`
3. 查看Console和Network标签
4. 注意WebSocket连接错误

## 🛠️ 一键修复脚本

### 脚本：腾讯云OpenClaw修复
```bash
#!/bin/bash
echo "=== 腾讯云OpenClaw网关连接修复脚本 ==="

# 1. 停止服务
echo "1. 停止OpenClaw服务..."
openclaw gateway stop
sleep 2

# 2. 备份配置
echo "2. 备份当前配置..."
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.$(date +%Y%m%d)

# 3. 配置调整
echo "3. 调整配置..."
openclaw config set gateway.bind "0.0.0.0:18789"
openclaw config set gateway.controlUi.allowInsecureAuth true
openclaw config set gateway.controlUi.cors true
openclaw config set gateway.websocket.timeout 86400000
openclaw config set gateway.logLevel debug

# 4. 重启服务
echo "4. 重启服务..."
openclaw gateway start
sleep 5

# 5. 检查状态
echo "5. 检查服务状态..."
openclaw gateway status

# 6. 检查端口
echo "6. 检查端口监听..."
netstat -tlnp | grep 18789

# 7. 测试本地连接
echo "7. 测试本地连接..."
curl -s http://127.0.0.1:18789 > /dev/null && echo "本地连接成功" || echo "本地连接失败"

echo "=== 修复完成 ==="
echo "请检查腾讯云安全组规则，确保端口18789已开放"
echo "访问地址：http://43.162.103.96:18789"
```

## 📋 腾讯云安全组配置指南

### 1. 控制台操作步骤：
1. 登录腾讯云控制台
2. 进入"轻量应用服务器"
3. 选择你的实例
4. 点击"防火墙"或"安全组"
5. 点击"添加规则"

### 2. 需要添加的规则：
```
规则1：
- 类型：自定义
- 来源：0.0.0.0/0
- 协议端口：TCP:18789
- 策略：允许
- 备注：OpenClaw HTTP/WebSocket

规则2（可选）：
- 类型：自定义
- 来源：0.0.0.0/0
- 协议端口：TCP:80
- 策略：允许
- 备注：HTTP访问

规则3（可选）：
- 类型：自定义
- 来源：0.0.0.0/0
- 协议端口：TCP:443
- 策略：允许
- 备注：HTTPS访问
```

### 3. 验证安全组：
```bash
# 在服务器上验证
sudo iptables -L -n | grep 18789

# 从外部验证
telnet 43.162.103.96 18789
```

## ⚠️ 常见云服务器问题

### 问题1：端口被云厂商屏蔽
**现象**：本地能访问，外部不能访问
**解决**：检查云控制台安全组、防火墙、网络ACL

### 问题2：WebSocket握手失败
**现象**：HTTP能访问，WebSocket连接失败
**解决**：配置Nginx反向代理，正确设置Upgrade头

### 问题3：跨域问题
**现象**：浏览器控制台显示CORS错误
**解决**：配置CORS头，或使用Nginx统一代理

### 问题4：连接超时
**现象**：连接建立后很快断开
**解决**：增加超时时间，检查网络稳定性

## 🎯 推荐部署架构

### 简单架构（适合测试）：
```
用户浏览器 → 腾讯云安全组 → OpenClaw (18789)
```

### 生产架构（推荐）：
```
用户浏览器 → 腾讯云安全组 → Nginx (80/443) → OpenClaw (18789)
                    ↓
                SSL证书
```

### 高可用架构：
```
用户 → 腾讯云负载均衡 → 多台Nginx → 多台OpenClaw
```

## 📊 故障排查流程图

```
开始
  ↓
检查页面是否能访问
  ├── 不能访问 → 检查安全组/防火墙
  └── 能访问但连接断开 → 继续
  ↓
检查浏览器控制台错误
  ├── WebSocket错误 → 配置Nginx反向代理
  ├── CORS错误 → 配置CORS头
  └── 其他错误 → 查看具体错误信息
  ↓
检查服务器日志
  ├── OpenClaw日志 → openclaw logs --follow
  ├── Nginx日志 → tail -f /var/log/nginx/error.log
  └── 系统日志 → journalctl -u openclaw
  ↓
根据日志调整配置
  ↓
测试验证
  ↓
问题解决 ✓
```

## 🆘 紧急恢复

如果所有方法都失败，尝试完全重新部署：

### 步骤1：备份数据
```bash
# 备份配置
cp -r ~/.openclaw ~/.openclaw.backup

# 备份数据库（如果有）
cp -r /var/lib/openclaw /var/lib/openclaw.backup
```

### 步骤2：重新安装
```bash
# 卸载旧版本
npm uninstall -g openclaw

# 清理残留
rm -rf ~/.openclaw/cache
rm -rf ~/.openclaw/logs

# 重新安装
npm install -g openclaw@latest
```

### 步骤3：重新配置
```bash
# 初始配置
openclaw configure

# 使用推荐配置
openclaw config set gateway.bind "0.0.0.0:18789"
openclaw config set gateway.controlUi.allowInsecureAuth true
openclaw config set gateway.auth.mode "token"
openclaw config set gateway.auth.token "你的安全token"

# 启动服务
openclaw gateway start
```

## 📞 腾讯云特定支持

### 1. 腾讯云文档：
- 轻量应用服务器：https://cloud.tencent.com/document/product/1207
- 安全组配置：https://cloud.tencent.com/document/product/213/39740

### 2. 联系腾讯云支持：
- 控制台提交工单
- 描述问题：OpenClaw服务端口18789无法外部访问

### 3. 社区资源：
- 腾讯云开发者社区
- OpenClaw官方文档

---

**总结建议**：
1. **先检查腾讯云安全组** - 这是最常见的问题
2. **配置Nginx反向代理** - 解决WebSocket问题
3. **查看详细日志** - 定位具体错误

根据你的描述，**最可能的问题是腾讯云安全组没有开放18789端口**，或者**需要Nginx来处理WebSocket连接**。

你可以先运行我提供的一键修复脚本，然后重点检查安全组配置。如果需要，我可以帮你查看具体的错误日志。