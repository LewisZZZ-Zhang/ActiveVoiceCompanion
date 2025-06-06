# ActiveVoiceCompanion

会主动找你的AI语音陪伴者（猫娘语音助手）

## 功能简介

- 支持自然语言对话，角色为猫娘小助手
- 支持语音合成与播放（微软 Edge TTS）
- 长时间无输入会主动用猫娘语气问候用户
- 支持自定义语音库和语音风格

## 安装依赖

1. **克隆项目并进入目录**
    ```bash
    git clone <你的仓库地址>
    cd ActiveVoiceCompanion
    ```

2. **创建并激活虚拟环境**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **安装 Python 依赖**
    ```bash
    pip install -r requirements.txt
    ```

4. **安装 ffmpeg（pydub 需要）**
    ```bash
    brew install ffmpeg
    ```

## 运行方法

```bash
python main.py
```

## 可用命令

- 输入问题进行对话
- `/exit`, `/quit`, `/bye` 退出程序
- `/voice list` 查看可用语音
- `/voice set` 设置新的语音ID
- `/help` 查看帮助

## 目录结构

- `main.py`：主程序入口
- `llm.py`：大模型对话接口
- `edgetts.py`：语音合成与播放
- `语言库/猫娘用户挂机语言库.txt`：挂机问候语库
- `tmp/`：临时音频文件夹（不会上传到GitHub）

## 注意事项

- 请确保本地有 Ollama 或其他 LLM 服务，并已正确配置 `llm.py` 的接口地址。
- `tmp/` 文件夹用于存放临时音频，已在 `.gitignore` 中忽略。
- 需要联网以使用 Edge TTS 服务。

---

如有问题欢迎提 Issue！