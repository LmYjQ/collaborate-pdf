# collaborate-pdf
合奏的时候每个人用ipad打开这个链接，指挥翻谱的时候，其他人自动同时翻页

# 使用方法
## 系统启动
- python app.py启动flask后端，提供文件上传和查看接口
- python websocket.py启动websocket通信server
- live-server启动web服务器

## 系统使用
- 先打开upload.html上传一份pdf，copy得到的url
- 每个client打开http://127.0.0.1:8080/view.html?file=xxxxxxxxxx.pdf，大家都看到相同的pdf
- 任意一个client翻页，其他人都一起翻页