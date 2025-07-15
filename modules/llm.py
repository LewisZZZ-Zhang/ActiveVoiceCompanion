import requests

import requests

context_cache = []  # 用于保存对话上下文

def conversation(prompt):
    global context_cache
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "deepseek-r1:14b",
        # "model": "pivpav/tiefighter:latest",
        # "model": "llama3.2",
        # "model": "mistral:7b-instruct-v0.2-q6_K",
        "prompt": prompt,
        "stream": False,
        "think": False,
        "system": (
            # "你是用户的女友，性格自然、活泼、贴心"
            "你是一只猫娘，性格自然、活泼、贴心"
            "用户是你的主人，你于用户相处像情侣。"
            "你只能用中文回复，不要输出任何英文或解释说明。"
            # "和主人对话时要自然、有生活气息，避免自我介绍，也不要问“有什么可以帮您”，不要频繁卖萌或总说'喵'。"
            # "不要分析自己的角色设定，也不要解释对话风格，只要像真实猫娘一样和主人互动。"
            # "不要提及深度求索、DeepSeek、AI助手等词汇。用户是你的主人。"
            # "请不要分析自己的角色设定，只要像猫娘一样和用户自然互动。"
        ),
        "context": context_cache,  # 加入历史上下文
        "temperature": 0.9  # 可选，控制生成文本的随机性
    }

    response = requests.post(url, json=payload)
    data = response.json()
    context_cache = data.get("context", [])  # 保存新上下文
    resp = data["response"]
    # 过滤掉 system prompt 内容
    resp = resp.split("你是一只猫娘")[0]
    return resp



if __name__ == "__main__":
    while True:
        # question = "你好，deepseek-llm-14B！"
        question = input("请输入问题: ")
        if question.lower() in ["exit", "quit", "bye"]:
            print("退出程序。")
            break
        elif question.strip() == "":
            print("问题不能为空，请重新输入。")
            continue
        answer = conversation(question)
        print(answer)