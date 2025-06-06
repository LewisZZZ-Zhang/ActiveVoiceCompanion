import torch
from TTS.utils.radam import RAdam

torch.serialization.add_safe_globals([RAdam])  # 传入列表，元素为类对象

from TTS.api import TTS

tts = TTS(model_name="tts_models/zh-CN/baker/tacotron2-DDC-GST", progress_bar=False)
print("模型文件路径：", tts.tts_config_path)