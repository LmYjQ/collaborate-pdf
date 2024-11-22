from flask import Flask, send_file, request, jsonify
import os
from flask_cors import CORS
import uuid
import socket
import json

app = Flask(__name__)
CORS(app)  # 启用 CORS

UPLOAD_FOLDER = './upload'  # 上传文件的目录
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
_local_ip = None


def read_config(file_path):
    try:
        # 打开并读取 JSON 文件
        with open(file_path, 'r') as file:
            config = json.load(file)
        
        # 提取 IP 地址和端口
        server_ip = config.get("server_ip", "127.0.0.1")  # 默认值为 127.0.0.1
        server_port = config.get("server_port", "80")    # 默认值为 80
        return server_ip, server_port

    except FileNotFoundError:
        print(f"Error: Config file {file_path} not found.")
        return None, None
    except json.JSONDecodeError:
        print(f"Error: Config file {file_path} is not valid JSON.")
        return None, None

def get_host_ip():
    """
    这个方法是目前见过最优雅获取本机服务器的IP方法了。没有任何的依赖，也没有去猜测机器上的网络设备信息。
    而且是利用 UDP 协议来实现的，生成一个UDP包，把自己的 IP 放如到 UDP 协议头中，然后从UDP包中获取本机的IP。
    这个方法并不会真实的向外部发包，所以用抓包工具是看不到的。但是会申请一个 UDP 的端口，所以如果经常调用也会比较耗时的，这里如果需要可以将查询到的IP给缓存起来，性能可以获得很大提升。
    :return:
    """
    global _local_ip
    s = None
    try:
        if not _local_ip:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            _local_ip = s.getsockname()[0]

            # host_name = socket.gethostname()
            # print(host_name)
            # _local_ip = socket.gethostbyname(host_name)
            # print(_local_ip)
        return _local_ip
    finally:
        if s:
            s.close()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdfFile' not in request.files:
        return 'No file part'
    file = request.files['pdfFile']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = str(uuid.uuid4())+'.pdf' # + os.path.splitext(file.filename)[1]
        print(filename)
        file.save('./upload/' + filename)
        return jsonify({'uuid': filename})


@app.route('/view/<filename>', methods=['GET'])
def view_pdf(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return 'File not found', 404


@app.route('/get_local_ip', methods=['GET'])  
def get_local_ip():  
    # 将局域网IP地址作为JSON响应返回  
    return jsonify({'local_ip': _local_ip})  


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = f'http://{_local_ip}:8080'
    # Add other CORS headers if needed
    return response
    
if __name__ == '__main__':
    # get_host_ip()
    config_file = "public/config.json"
    _local_ip, port = read_config(config_file)
    print(f'[config]ip:{_local_ip}')
    app.run(debug=True, host=_local_ip)


