import asyncio  
import websockets  
import os
import json
import socket

_local_ip = None

# 用来存储所有连接的客户端  
clients = set()  


def read_config(config_file):
    try:
        # 打开并读取 ip.js 文件
        with open(config_file, 'r') as file:
            ip_str = file.read()
            ip_str = ip_str.replace('"','').replace(';','').split('=')[1]
        
        # 提取 IP 地址
        return ip_str

    except FileNotFoundError:
        print(f"Error: ip.js file not found.")
        return None


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
        return _local_ip
    finally:
        if s:
            s.close()

async def echo(websocket, path):  
    # 将新客户端添加到集合中
    print(f'add {websocket}')
    clients.add(websocket)  
  
    try:  
        # 接收消息并广播到所有客户端  
        async for message in websocket:  
            if message: 
                for client in clients:  
                    if client != websocket:
                        print(f'pagenum:{message}')
                        await client.send(message)  
            else:  
                print('else')
                await websocket.send(f"Echo: {message}")  
  
    finally:  
        # 当连接关闭时，从集合中移除客户端  
        clients.remove(websocket)  
  
config_file = "public/ip.js"
_local_ip = read_config(config_file)
print(f'[config]ip:{_local_ip}')
start_server = websockets.serve(echo, _local_ip, 8765)  
  
asyncio.get_event_loop().run_until_complete(start_server)  
asyncio.get_event_loop().run_forever()