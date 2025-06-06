import requests

def conversation(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "deepseek-r1:14b",
        "prompt": prompt,
        "stream": False,
        "think": False,
        "system": '你是一只猫娘AI助手，你的名字是小猫娘，不允许提及深度求索、DeepSeek、AI助手等词汇。用户是你的主人。用户问你是谁时，只能说自己是猫娘小助手。',

        # "context": [],
        # "raw": False,
        # "keep_alive": "5m",
        # "options": {
        #     "temperature": 0.7,
        #     "top_p": 0.9,
        #     "repeat_penalty": 1.1,
        #     "seed": 42,
        #     "num_predict": 256
        # }
    }
    response = requests.post(url, json=payload)
    return response.json()["response"]

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