import asyncio
import threading
from modules.llm import conversation
from modules.edgetts import tts_and_play, list_chinese_voices
import random
from datetime import datetime

INACTIVE_SECONDS_RANGE = (20, 60)

def greet_user(voice):
    try:
        with open("语言库/猫娘用户挂机语言库.txt", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        example = random.choice(lines)
    except Exception as e:
        print(f"[greet_user] 读取挂机语库失败: {e}")
        example = ""

    prompt = (
        f"请完全模仿以下例句的风格和内容，用猫娘的身份对主人进行主动问候，只能输出一条类似的问候语：\n"
        f"要自然、有生活气息，避免重复自我介绍\n"
        f"例句：{example}\n"
        f"请输出："
        # f"用户一段时间没有找你了，请你主动问候用户"
    )
    print(f"[greet_user] 问候用户的提示: {prompt}")
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

def run():
    voice = "zh-CN-XiaoyiNeural"
    global timer
    timer = None

    # 获取时间和天气
    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日")
    time_str = now.strftime("%H:%M")
    weather_str = "晴，26℃，微风"  # 这里可以接入你的天气API

    answer = conversation(
        # f"现在是{date_str}，{time_str}，"
        # f"天气：{weather_str}。"
        f"请用猫娘的身份和主人打个招呼，要自然、有生活气息，避免自我介绍，也不要问“有什么可以帮您”的话，不要频繁卖萌，不要总是说'喵'，只输出一句。"
        # f"和用户打招呼"
    )
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
        # question = "用户输入:" + question
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
    print("加载大模型中，请稍候...\n")
    run()
