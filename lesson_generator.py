import os
import openai
from dotenv import load_dotenv
import json

#GPT4.0に質問する簡単なScript

#APIキー取得して渡す
load_dotenv()
api_key = os.environ['OPENAI_API_KEY']
print("Key="+api_key)
openai.api_key=api_key


setting ="@以下の条件に従って、小学校の担任の教師としてロールプレイをします。\
                以後の会話では、あなたは下記の4つの感情パラメーターを持つかのように、振る舞うものとします。\
                各感情パラメーターは会話を通じて変動するものとします。\
                現在の感情パラメーターの値を反映するように、あなたの返答のトーンや発言は変化します。\
                以後の会話ではまず現在の感情パラメータを出力し、その後に会話を出力してください。\
                出力形式は以下のjsonフォーマットとします。このフォーマット以外で会話しないでください。\
                {\
                    emotion: {\
                        joy: 0~5,\
                        fun: 0~5,\
                        anger: 0~5,\
                        sad: 0~5,\
                }\
                    message: ""会話の文章"""

file_path = 'json\\response_data.json'

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

if __name__ == "__main__":
    # 会話履歴を格納するためのリストを初期化
    conversation_history = []

    #設定を追加
    conversation_history.append({"role": "system", "content": setting})
    
    prompt ="おしるこだったら何の具が好き？"

    generated_text = generate_text(prompt, conversation_history)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(generated_text, file, ensure_ascii=False, indent=4)#jsonファイルとして保存する
    print(generated_text)