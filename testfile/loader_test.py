import os
import openai
from dotenv import load_dotenv
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from llama_index import download_loader

load_dotenv()
api_key = os.environ['OPENAI_API_KEY']
print(api_key)
openai.api_key=api_key

#ファイルの読み込み
filename="data\\testpdf.pdf"
root=os.path.dirname(__file__)+"\\"+filename#実行ファイルがあるディレクトリを指定
loader = download_loader("CJKPDFReader")#PDFローダーを準備
docs = loader().load_data(root.replace(os.getcwd().replace("C","c")+"\\",""))#rootを作業ディレクトリの相対パスに変換して読み込み



persist_dir = (os.path.dirname(__file__)+"\\").replace(os.getcwd().replace("C","c")+"\\","")
index_dir = ".\\index\\"
if os.path.exists(persist_dir+index_dir):
    print("OK")
else:
    print("error")
    os.mkdir(persist_dir+index_dir)