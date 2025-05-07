import socket
import threading

class ChatServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.nicknames = []

    def broadcast(self, message, sender=None):
        """广播消息给所有客户端"""
        for client in self.clients:
            if client != sender:  # 不发送给消息的发送者
                client.send(message)

    def handle_client(self, client):
        while True:
            try:
                # 接收消息并解码
                message = client.recv(1024).decode('utf-8')
                index = self.clients.index(client)
                nickname = self.nicknames[index]
                # 在消息前添加发送者昵称
                formatted_message = f"{message}"
                self.broadcast(formatted_message.encode('utf-8'), sender=client)
            except:
                # 处理客户端断开连接
                index = self.clients.index(client)
                nickname = self.nicknames[index]
                print(f"{nickname} has disconnected.")  # 服务端提示玩家断开连接
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast(f'{nickname} has left the chat.'.encode('utf-8'))
                self.nicknames.remove(nickname)
                break

    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f'Connected with {str(address)}')

            nickname = client.recv(1024).decode('utf-8')
            self.nicknames.append(nickname)
            self.clients.append(client)

            print(f'Nickname of the client is {nickname}')
            self.broadcast(f'{nickname} has joined the chat.'.encode('utf-8'))
            client.send('Connected to the server!'.encode('utf-8'))

            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

def start_server():
    print("聊天服务器正在运行...")
    chat_server = ChatServer()
    chat_server.receive()