import torch
from TTS.utils.radam import RAdam
import collections

torch.serialization.add_safe_globals([RAdam, collections.defaultdict, dict])  # 允许反序列化RAdam、defaultdict和dict

from TTS.api import TTS
tts = TTS(model_name="tts_models/zh-CN/baker/tacotron2-DDC-GST", progress_bar=True)
tts.tts_to_file(text="你好，有什么我可以帮你的？", file_path="output.wav")