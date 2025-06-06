import asyncio
import threading
from llm import conversation
from edgetts import tts_and_play, list_chinese_voices
import random

INACTIVE_SECONDS_RANGE = (20, 60)

def greet_user(voice):
    try:
        with open("语言库/猫娘用户挂机语言库.txt", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        example = random.choice(lines)
    except Exception as e:
        print(f"[greet_user] 读取挂机语库失败: {e}")
        example = ""

    prompt = (f"用户很久没有输入了，请用可爱的猫娘语气问候用户。模仿: {example}")
    answer = conversation(prompt)
    print("[greet_user] 问候用户")
    print(answer)
    asyncio.run(tts_and_play(answer, voice))
    wait_time = random.randint(*INACTIVE_SECONDS_RANGE)
    print(f"[greet_user] 下次问候将在 {wait_time} 秒后进行。")
    global timer
    timer = threading.Timer(wait_time, greet_user, args=(voice,))
    print(f"[greet_user] 设置新的timer: {timer}")
    timer.start()

def main():
    voice = "zh-CN-XiaoyiNeural"
    global timer
    timer = None

    answer = conversation('你是一只猫娘AI助手，你的名字是小猫娘，不允许提及深度求索、DeepSeek、AI助手等词汇。用户是你的主人。用户问你是谁时，只能说自己是猫娘小助手。'+"现在和用户打个招呼吧！")
    print(answer)
    asyncio.run(tts_and_play(answer, voice))

    while True:
        # 启动/重置定时器
        if timer:
            print("[main] 取消已有timer")
            timer.cancel()
        wait_time = random.randint(*INACTIVE_SECONDS_RANGE)
        print(f"[main] 设置新的timer，{wait_time}秒后问候")
        timer = threading.Timer(wait_time, greet_user, args=(voice,))
        print(f"[main] 新timer对象: {timer}")
        timer.start()

        question = input("请输入问题: \n")
        print("[main] 用户输入，取消timer")
        timer.cancel()  # 用户输入后取消定时器
        if not question.startswith("/"):
            print("[main] 正常问题，继续处理")
            answer = conversation(question)
            print(answer)
            asyncio.run(tts_and_play(answer, voice))
        else:
            if question.lower() in ["/exit", "/quit", "/bye"]:
                print("退出程序。")
                break
            elif question.lower() == "/voice list":
                list_chinese_voices()
                continue
            elif question.lower() == "/voice set":
                voice = input("请输入新的语音ID（例如 zh-CN-XiaoyiNeural）: ")
                print(f"已设置语音为: {voice}")
                continue
            elif question.strip() == "":
                print("问题不能为空，请重新输入。")
                continue
            elif question.lower() == "/help":
                print("可用命令：\n"
                    "1. 输入问题进行对话\n"
                    "2. 输入 /exit, /quit, /bye 退出程序\n"
                    "3. 输入 /voice list 查看可用语音\n"
                    "4. 输入 /voice set 设置新的语音ID\n"
                )
                continue


if __name__ == "__main__":
    print("欢迎使用猫娘AI助手！\n")
    main()
