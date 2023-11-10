import os
import openai
from dotenv import load_dotenv

from google.oauth2.service_account import Credentials
import gspread
import socket
import time

from llama_index import (
    GPTVectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    download_loader
)

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

#スプレッドシートを取得するための関数
def get_sheet():        
    spreadsheet = gc.open_by_url(spreadsheet_url).sheet1
    import_value = spreadsheet.col_values(2)#B行の要素を取得
    print(import_value)
    return import_value
    #spreadsheet.acell('B'+cell_number).value

#index作成
persist_dir = (os.path.dirname(__file__)+"\\").replace(os.getcwd().replace("C","c")+"\\","")
index_dir = persist_dir+".\\index\\"
if not os.path.exists(index_dir):
    os.mkdir(index_dir)

#ファイルの読み込み
filename="data\\karada.pdf"
root=os.path.dirname(__file__)+"\\"+filename#実行ファイルがあるディレクトリを指定
loader = download_loader("CJKPDFReader")#PDFローダーを準備
#rootを作業ディレクトリの相対パスに変換して読み込み↓　触るな！
docs = loader().load_data(root.replace(os.getcwd().replace("C","c")+"\\",""))

index = GPTVectorStoreIndex.from_documents(docs)#docsからindex作成
index.storage_context.persist(index_dir)#index保存

# load from disk
storage_context = StorageContext.from_defaults(persist_dir=index_dir)
# load index
index = load_index_from_storage(storage_context)


#インデックスから解答を生成する
def print_response(prompt: str, index):
    query_engine = index.as_query_engine()
    return query_engine.query(prompt+"日本語で答えてください。質問に関係ないことは、話さないでください。出力は必ず２文以内にしてください。それが不可能な場合でもできるだけ、少なくなるようにして下さい。")


#UDP通信周りの関数
def UDP(content):
    client.sendto(content.encode('utf-8'),(HOST,PORT))

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
            ans=print_response(new_list[i], index)
            UDP(new_list[i]+"@"+str(ans))
        current_list = new_list
        lastnum = len(current_list)
        time.sleep(5.0)