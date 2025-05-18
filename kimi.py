from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

# 初始化 Flask 应用
app = Flask(__name__)

# 开启跨域支持
CORS(app)

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key="请在这里填写你的OpenAI API密钥",
    base_url="https://api.moonshot.cn/v1",
)


@app.route('/kimichat', methods=['POST'])
def chat():
    # 获取用户请求的消息
    user_message = request.json.get('message', '')

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        # 请求 OpenAI API 进行对话生成
        completion = client.chat.completions.create(
            model="moonshot-v1-128k",
            messages=[
                {
                    "role": "system",
                    "content": "你是kimi，在这个话题中,你会尽可能回复与柑橘种植相关的内容,避免回复与柑橘种植无关的内容"
                },
                {
                    "role": "user",
                    "content": user_message
                },
            ],
            temperature=0.3,
        )

        # 返回生成的回复
        answer = completion.choices[0].message
        return answer.content

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # 运行 Flask 应用
    app.run(host='0.0.0.0', port=5000)
