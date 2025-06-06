# ActiveVoiceCompanion

会主动找你的AI语音陪伴者（猫娘语音助手）

## 功能简介

- 支持自然语言对话，角色为猫娘小助手
- 支持语音合成与播放（微软 Edge TTS）
- 长时间无输入会主动用猫娘语气问候用户
- 支持自定义语音库和语音风格

## 安装依赖
’‘’bash
/usr/local/bin/python3.11 -m venv venv
‘’‘

source venv/bin/activate
pip install -r requirements.txt

## 运行方法

python main.py
或者
python ui_main.py

## 可用命令

- 输入问题进行对话
- `/exit`, `/quit`, `/bye` 退出程序
- `/voice list` 查看可用语音
- `/voice set` 设置新的语音ID
- `/help` 查看帮助

## 注意事项

- 请确保本地有 Ollama 或其他 LLM 服务，并已正确配置 `llm.py` 的接口地址。
- `tmp/` 文件夹用于存放临时音频，已在 `.gitignore` 中忽略。
- 需要联网以使用 Edge TTS 服务。
- 最好是官方下载的python，不然好像tinker会有什么问题

---

如有问题欢迎提 Issue！