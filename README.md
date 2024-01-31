# wework_url_callback
用Python架设简单的企业微信API接收消息服务器，便于设置企业可信IP。

## 使用方法

### Docker
```
docker run -p 5000:5000 -e QYWX_AESKEY=企业微信应用EncodingAESKey -e QYWX_TOKEN=企业微信应用Token kyeooeyk/wework_url_callback
```
把上面命令中的**企业微信应用EncodingAESKey**和**企业微信应用Token**替换成你自己在企业微信应用API接收消息服务器配置里设置的。
把企业微信应用API接收消息服务器配置里的URL设置成你的**http://YOURIP:5000**,打开你服务器的5000端口。

### 本项目仅为了方便企业微信应用设置可信IP，请不要进行商用，任何商业行为与本项目无关