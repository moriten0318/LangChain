import os
import openai
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
import gspread
import socket
import time

#APIキー取得して渡す
load_dotenv()
api_key = os.environ['OPENAI_API_KEY']
print(api_key)
openai.api_key=api_key

#Googleスプレッドシート認証用
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
json_pass="gspread-400109-00716d87edde.json"
#認証用のJSONファイルのパスを貼る(\は2個に変えること！)
#ここ変更しないと別環境では動かないので注意！
credentials = Credentials.from_service_account_file(
    (os.path.dirname(__file__)).replace("C","c")+"\\"+json_pass,
    scopes=scopes
)
gc = gspread.authorize(credentials)#GoogleAPIにログイン
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1g4g0UNh74WJmemhGR3ftCQUWyt2_GbmYonw6CHo0XHo/edit#gid=0"

#UDP通信用設定
HOST = '127.0.0.1'
PORT = 50007
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
lastnum = 0
null = ""
current_list = []

setting ="あなたの名前=ハル\
    あなたの背景設定=バーチャル世界に存在するAI教師\
    日本語で答えてください。質問に関係ないことは、話さないでください。\
    出力は必ず簡潔に答えてください。それが不可能な場合でもできるだけ、少なくなるようにして下さい。"

lesson =""


#スプレッドシートを取得するための関数
def get_sheet():        
    spreadsheet = gc.open_by_url(spreadsheet_url).sheet1
    import_value = spreadsheet.col_values(2)#B行の要素を取得
    print(import_value)
    return import_value
    #spreadsheet.acell('B'+cell_number).value

#返答生成
def generate_text(prompt, conversation_history):
    # プロンプトを会話履歴に追加
    conversation_history.append({"role": "user", "content": prompt})
    # GPT-4モデルを使用する場合
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=conversation_history
    )
    message = ""
    for choice in response.choices:
        message += choice.message['content']

    # 応答文を会話履歴に追加
    conversation_history.append({"role": "assistant", "content": message})
    return message

#UDP通信周りの関数
def UDP(content):
    client.sendto(content.encode('utf-8'),(HOST,PORT))

if __name__ == "__main__":
    # 会話履歴を格納するためのリストを初期化
    conversation_history = []
    #設定を追加
    conversation_history.append({"role": "system", "content": setting+lesson})
    

    #mainループ
    while True:
        new_list = get_sheet()    
        if new_list==current_list:
            print("更新はありません")
            time.sleep(5.0)
            continue
        else:
        #スプレッドシートに更新があったときの処理
            for i in range(lastnum,len(new_list)):
                print(new_list[i])
                ans=generate_text(new_list[i], conversation_history)
                UDP(new_list[i]+"@"+str(ans))
            current_list = new_list
            lastnum = len(current_list)
            time.sleep(5.0)