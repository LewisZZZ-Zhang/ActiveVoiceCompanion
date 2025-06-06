# pip install edge-tts
# pip install playsound
# pip install simpleaudio
# pip install pydub
from pydub import AudioSegment
from pydub.playback import play
import edge_tts
import asyncio

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

async def tts_and_play(text, voice="zh-CN-XiaoyiNeural", file_path="voice/tmp_output.mp3"):
    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save(file_path)
    # print(f"已保存到 {file_path}")
    audio = AudioSegment.from_file(file_path)
    play(audio)

if __name__ == "__main__":
    # list_chinese_voices()
    # test_all_chinese_voices()
    asyncio.run(tts_and_play("你好，你在干什么啊。"))

