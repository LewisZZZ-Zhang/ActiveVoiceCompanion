# git clone https://github.com/SparkAudio/Spark-TTS
# pip install modelscope
# modelscope download --model SparkAudio/Spark-TTS-0.5B


import sys
sys.path.append('/Users/Lewis/MyFiles/funproject/1/Spark-TTS')

from SparkTTS import SparkTTS

model = SparkTTS('./pretrained_models/Spark-TTS-0.5B')
wav = model.inference(text="你好，这是真人级语音合成。", gender="female")