import socket
import threading
import time
import sys


class ChatClient:
    def __init__(self, host='localhost', port=12345):
        self.server_address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = None  # 存储用户的名称

    def connect(self):
        try:
            self.socket.connect(self.server_address)
            self.nickname = input("请输入您的聊天名称: ")  # 用户输入名称
            self.socket.sendall(self.nickname.encode('utf-8'))  # 发送名称到服务器
            print("Connected to the chat server.")
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def send_message(self, message):
        try:
            # 在消息前添加用户的名称
            formatted_message = f"{self.nickname}: {message}"
            self.socket.sendall(formatted_message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {e}")

    def receive_messages(self):
        first_message = True  # 标志变量，判断是否是首次接收消息
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    # 清空当前行并打印消息
                    sys.stdout.write("\r" + " " * 80 + "\r")  # 清空当前行
                    print(message)
                    # 重新显示用户输入提示
                    if not first_message:  # 仅在非首次接收消息时重新显示用户输入提示
                        sys.stdout.write(f"{self.nickname}: ")
                        sys.stdout.flush()
                    first_message = False  # 设置为非首次接收消息
                else:
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def close(self):
        self.socket.close()
        print("Disconnected from the chat server.")

if __name__ == "__main__":
    client = ChatClient(host='127.0.0.1', port=12345)
    client.connect()
    
    while True:
        time.sleep(0.1)  # 确保主线程不会过快循环
        print(f"{client.nickname}: ", end="")
        msg = input()
        if msg.lower() == 'exit':
            client.close()
            break
        client.send_message(msg)