# pip install edge-tts
# pip install playsound
# pip install simpleaudio
# pip install pydub
from pydub import AudioSegment
from pydub.playback import play
import edge_tts
import asyncio
import os

# xiaoxiao，xiaoyi好听，xiaoyi更幼一点
# yunxia有点像罗小黑这种，也算猫吧

def list_chinese_voices():
    voices = asyncio.run(edge_tts.list_voices())
    for v in voices:
        if v["Locale"].startswith("zh-"):
            print(f'{v["ShortName"]}: {v["Gender"]}')

def test_all_chinese_voices():
    voices = asyncio.run(edge_tts.list_voices())
    for v in voices:
        if v["Locale"].startswith("zh-"):
            print(f'Testing voice: {v["ShortName"]}')
            communicate = edge_tts.Communicate("你好，我是你的助手。", voice=v["ShortName"])
            asyncio.run(communicate.save(f'voice/output_{v["ShortName"]}.mp3'))
            print(f'Saved output to voice/output_{v["ShortName"]}.mp3')

# ...existing code...
async def tts_and_play(text, voice="zh-CN-XiaoyiNeural", file_path="tmp/tmp_output.mp3"):
    # 自动创建 tmp 文件夹
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save(file_path)
    audio = AudioSegment.from_file(file_path)
    play(audio)
# ...existing code...

if __name__ == "__main__":
    # list_chinese_voices()
    # test_all_chinese_voices()
    asyncio.run(tts_and_play("你在干嘛啊啊啊！去main里面跑代码啊！"))

