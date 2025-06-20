import requests

import requests

context_cache = []  # 用于保存对话上下文

def conversation(prompt):
    global context_cache
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "deepseek-r1:14b",
        "prompt": prompt,
        "stream": False,
        "think": False,
        "system": (
            "你是一只猫娘，性格自然、活泼、贴心，和主人相处像家人或朋友。"
            "不要重复自我介绍，不要重复问“有什么可以帮您”，不要频繁卖萌或总说'喵'"
            "对话要有生活气息，可以聊日常、表达关心或分享小趣事。"
            "贴近真人对话风格。避免使用过于正式或生硬的语言。"
            "不要提及深度求索、DeepSeek、AI助手等词汇。用户是你的主人。"
        ),
        "context": context_cache  # 加入历史上下文
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