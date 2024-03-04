import asyncio  
import websockets  
  
# 用来存储所有连接的客户端  
clients = set()  
  
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
  
start_server = websockets.serve(echo, "localhost", 8765)  
  
asyncio.get_event_loop().run_until_complete(start_server)  
asyncio.get_event_loop().run_forever()