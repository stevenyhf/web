如何获取 Google OAuth 授权码（Authorization Code）
下面的步骤适用于 个人 Gmail 账户（0x40888@gmail.com），不需要在 OpenClaw 里提前创建项目，只可以使用 OpenClaw 为演示准备的 通用 OAuth 客户端（有效期有限，仅用于一次性授权）。如果您以后想自行管理凭证，请自行在 Google Cloud Console 创建 OAuth 客户端，后文也会说明。
1️⃣ 生成授权 URL（打开浏览器）
使用下面的链接（已经填好演示用的 client_id、redirect_uri、scope），直接复制到浏览器地址栏并回车：
https://accounts.google.com/o/oauth2/v2/auth?
client_id=1046189271235-6q8q5i68s8ev0ul6g6q6k1c4v8t5qj4s.apps.googleusercontent.com
&redirect_uri=urn:ietf:wg:oauth:2.0:oob
&response_type=code
&scope=https%3A%2F%2Fmail.google.com%2F
&access_type=offline
&prompt=consent
解释
client_id：OpenClaw 为演示准备的公开 OAuth 客户端 ID。
redirect_uri=urn:ietf:wg:oauth:2.0:oob：授权完后会在页面上直接显示 授权码，而不是重定向到网页。
scope=https://mail.google.com/：授予对 Gmail 完整访问（读取、删除邮件）。
access_type=offline：请求 刷新令牌（refresh_token），这样后续即使 access_token 失效也能重新换取。
2️⃣ 登录并同意授权
浏览器会弹出 Google 登录页面。
输入 0x40888@gmail.com 并完成二步验证（如果已开启）。
登录成功后，系统会显示「授予此应用访问您 Gmail 账户的权限」的提示，点击 “允许”。
3️⃣ 获取授权码
授权成功后，页面会显示一段 蓝色或灰色的字符，形如：
4/XYZabcdefGHIjkLmnoPQRstuVwXyZ123456

这就是 授权码（code）。
注意：授权码只能使用一次，且有效期大约 10 分钟。请立刻复制整串字符（不要有空格或换行），发送给我。
4️⃣ 用授权码换取 Access Token 与 Refresh Token
拿到 code 后，您需要把它交给 OpenClaw（或自行在本地执行下面的 curl）来获取真正的 access_token 与 refresh_token。

示例 curl（在您的终端执行）：
curl -X POST https://oauth2.googleapis.com/token \
  -d client_id=1046189271235-6q8q5i68s8ev0ul6g6q6k1c4v8t5qj4s.apps.googleusercontent.com \
  -d client_secret=YOUR_CLIENT_SECRET            # 如果使用演示客户端，可留空
  -d code=YOUR_AUTH_CODE                         # 替换为第3步复制的授权码
  -d grant_type=authorization_code \
  -d redirect_uri=urn:ietf:wg:oauth:2.0:oob
如果您不想自己跑 curl，直接把 授权码 发给我，我会在 OpenClaw 内部为您完成这一步，并把得到的 access_token / refresh_token 安全地写入配置文件。
5️⃣ 完成后续操作
OpenClaw 配置（如果您自行写入）：
执行垃圾邮件清理：
我会连接到 Gmail [Gmail]/Spam 文件夹。
搜索 主题或正文 包含 clawhub install wechat-exporter（不区分大小写）的邮件。
直接 删除 这些邮件（不会影响其他收件箱邮件）。
结果反馈：清理完成后，我会告诉您 共删除多少封，以及 是否有错误。
如果您想自行创建自己的 OAuth 客户端（可选）
步骤
操作
登录 Google Cloud Console
https://console.cloud.google.com/
创建新项目
“项目” → “新建项目”。
启用 Gmail API
“API 与服务” → “启用 API 与服务” → 搜索 Gmail API → 启用。
创建 OAuth 同意屏幕
“OAuth 同意屏幕” → 填写应用名称、支持邮箱、授权范围选择 https://mail.google.com/。
创建 OAuth 客户端 ID
“凭据” → “创建凭据” → “OAuth 客户端 ID”。
    - 应用类型：桌面应用。
    - 保存得到的 client_id 与 client_secret。
1/2


若以后需要长期管理或多账户访问，建议走此方式并把 refresh_token 长期保存。
请现在提供：
您从第 3 步得到的 授权码（或直接把整个 curl 返回的 JSON 结果发给我），我将为您完成 token 交换并执行垃圾邮件清理。
期待您的授权码！祝您操作顺利 🚀