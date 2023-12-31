import os
import openai
from dotenv import load_dotenv

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

#index作成
persist_dir = (os.path.dirname(__file__)+"\\").replace(os.getcwd().replace("C","c")+"\\","")
index_dir = persist_dir+".\\index\\"
if not os.path.exists(index_dir):
    os.mkdir(index_dir)

#ファイルの読み込み
filename="data\\testpdf.pdf"
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


def print_response(prompt: str, index):
    query_engine = index.as_query_engine()
    print(query_engine.query(prompt))


print_response("大学入学試験が厳しいのはどの国ですか？", index)