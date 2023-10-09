import os
import openai
from dotenv import load_dotenv

from llama_index import (
    GPTVectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

load_dotenv()
api_key = os.environ['OPENAI_API_KEY']
print(api_key)
openai.api_key=api_key

persist_dir = "./LangChainTest/"#indexを作成する現在のディレクトリ
if not os.path.exists(persist_dir):
    os.mkdir(persist_dir)

documents = SimpleDirectoryReader("data").load_data()

index = GPTVectorStoreIndex.from_documents(documents)
index.storage_context.persist(persist_dir)

# load from disk
storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
# load index
index = load_index_from_storage(storage_context)


def print_response(prompt: str, index):
    query_engine = index.as_query_engine()
    print(query_engine.query(prompt))


print_response("禁止になったカードは何ですか？", index)
print_response("環境で最強のデッキは何ですか？", index)
print_response("エスパーミッドレンジは何色のデッキですか？", index)