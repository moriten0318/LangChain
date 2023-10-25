import socket

# 受信用のIPアドレスとポート
HOST = '127.0.0.1' 
recPORT = 50007
senPORT = 50008

# UDP通信ソケットの作成
rec_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rec_socket.bind((HOST, recPORT))
sen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def UDP(content):
    #Unityへ結果をUDP送信する
    sen_socket.sendto(content.encode('utf-8'),(HOST,senPORT))

while True:
    # UnityからUDP受信するループ
    data, addr = rec_socket.recvfrom(4096)
    text = data.decode('utf-8')
    print(text)
    UDP("pythonがデータを受信しました:"+text)