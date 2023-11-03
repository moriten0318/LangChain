import os
import openai
from dotenv import load_dotenv
import socket

# 受信用のIPアドレスとポート
HOST = '127.0.0.1' 
recPORT = 50007
senPORT = 50008

#APIキー取得して渡す
load_dotenv()
api_key = os.environ['OPENAI_API_KEY']
print(api_key)
openai.api_key=api_key

# UDP通信ソケットの作成
rec_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rec_socket.bind((HOST, recPORT))
sen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

instruction = "与えられた文章を分析し、その発言を聞いた人がどのような感情を抱くか推察して答えてください。感情は「怒り」「悲しい」「驚き」「嬉しい」の4種類いずれかで答えてください.答える際は単語のみ感情を示す５種類の単語のうちいずれかの単語のみを発言してください。"

def GPT(txt):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": instruction},
        {"role": "user", "content": txt}
    ]  
    )
    print(response["choices"][0]["message"]["content"])
    return(response["choices"][0]["message"]["content"])


def UDP(content):
    #Unityへ結果をUDP送信する
    sen_socket.sendto(content.encode('utf-8'),(HOST,senPORT))

while True:
    # UnityからUDP受信するループ
    data, addr = rec_socket.recvfrom(4096)
    text = data.decode('utf-8')
    print(text)
    gpt=GPT(text)
    UDP(gpt)