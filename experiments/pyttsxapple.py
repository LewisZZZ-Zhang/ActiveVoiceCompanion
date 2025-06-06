import pyttsx3

def supported_languages():
    engine = pyttsx3.init()
    for voice in engine.getProperty('voices'):
        print(voice.id, voice.name)

def list_chinese_voices():
    engine = pyttsx3.init()
    print("可用中文语音：")
    for voice in engine.getProperty('voices'):
        # 检查 voice.id 或 voice.name 是否包含中文相关关键词
        if ("zh" in voice.id.lower() or
            "chinese" in voice.name.lower() 
            # or
            # "Tingting" in voice.name or
            # "Meijia" in voice.name or
            # "Sinji" in voice.name
            ):
            print(voice.name, end='\n     ---')
            print(voice.id)

def speak(text,id = "com.apple.voice.compact.zh-TW.Meijia"):
    engine = pyttsx3.init()
    for voice in engine.getProperty('voices'):
        if id == voice.id:
            print(f"使用语音: {voice.name} id---{voice.id}")
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    list_chinese_voices()
    # supported_languages()
    speak("你好，我是小爱同学。",id="com.apple.voice.compact.zh-CN.Tingting") 