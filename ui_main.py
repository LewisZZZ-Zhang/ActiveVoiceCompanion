import asyncio
import threading
import random
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
from modules.llm import conversation
from modules.edgetts import tts_and_play, list_chinese_voices

INACTIVE_SECONDS_RANGE = (20, 60)

class CatGirlAIUI:
    def __init__(self, root):
        self.root = root
        self.root.title("猫娘AI助手")
        self.voice = "zh-CN-XiaoyiNeural"
        self.timer = None
        self.running = True

        self.text_area = scrolledtext.ScrolledText(root, width=60, height=20, state='disabled')
        self.text_area.pack(padx=10, pady=10)

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(side=tk.LEFT, padx=10, pady=5, expand=True, fill=tk.X)
        self.entry.bind("<Return>", self.on_send)

        self.send_btn = tk.Button(root, text="发送", command=self.on_send)
        self.send_btn.pack(side=tk.LEFT, padx=5)

        self.voice_btn = tk.Button(root, text="语音列表", command=self.show_voices)
        self.voice_btn.pack(side=tk.LEFT, padx=5)

        self.set_voice_btn = tk.Button(root, text="设置语音", command=self.set_voice)
        self.set_voice_btn.pack(side=tk.LEFT, padx=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # 首次问候
        threading.Thread(target=self.first_greet, daemon=True).start()

    def append_text(self, text):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.see(tk.END)
        self.text_area.config(state='disabled')

    def first_greet(self):
        answer = conversation(
            '你是一只猫娘AI助手，你的名字是小猫娘，不要提及深度求索、DeepSeek、AI助手等词汇。用户是你的主人。用户问你是谁时，只能说自己是猫娘小助手。现在和用户打个招呼吧！'
        )
        self.append_text(f"猫娘：{answer}")
        asyncio.run(tts_and_play(answer, self.voice))
        self.start_greet_timer()

    def start_greet_timer(self):
        if self.timer:
            self.timer.cancel()
        wait_time = random.randint(*INACTIVE_SECONDS_RANGE)
        self.timer = threading.Timer(wait_time, self.greet_user)
        self.timer.start()

    def greet_user(self):
        try:
            with open("语言库/猫娘用户挂机语言库.txt", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            example = random.choice(lines)
        except Exception as e:
            example = ""
        prompt = f"用户很久没有输入了，请用可爱的猫娘语气问候用户。模仿: {example}"
        answer = conversation(prompt)
        self.append_text(f"猫娘：{answer}")
        asyncio.run(tts_and_play(answer, self.voice))
        if self.running:
            self.start_greet_timer()

    def on_send(self, event=None):
        question = self.entry.get().strip()
        if not question:
            messagebox.showinfo("提示", "请输入内容")
            return
        self.append_text(f"你：{question}")
        self.entry.delete(0, tk.END)
        if self.timer:
            self.timer.cancel()
        threading.Thread(target=self.handle_question, args=(question,), daemon=True).start()

    def handle_question(self, question):
        if not question.startswith("/"):
            answer = conversation(question)
            self.append_text(f"猫娘：{answer}")
            asyncio.run(tts_and_play(answer, self.voice))
            if self.running:
                self.start_greet_timer()
        else:
            cmd = question.lower()
            if cmd in ["/exit", "/quit", "/bye"]:
                self.append_text("已退出程序。")
                self.on_close()
            elif cmd == "/voice list":
                voices = list_chinese_voices()
                self.append_text("可用语音：\n" + "\n".join(voices) if voices else "未获取到语音列表")
                if self.running:
                    self.start_greet_timer()
            elif cmd == "/voice set":
                new_voice = simpledialog.askstring("设置语音", "请输入新的语音ID（如 zh-CN-XiaoyiNeural）:", parent=self.root)
                if new_voice:
                    self.voice = new_voice
                    self.append_text(f"已设置语音为: {self.voice}")
                if self.running:
                    self.start_greet_timer()
            elif question.strip() == "":
                self.append_text("问题不能为空，请重新输入。")
                if self.running:
                    self.start_greet_timer()
            elif cmd == "/help":
                self.append_text(
                    "可用命令：\n"
                    "1. 输入问题进行对话\n"
                    "2. 输入 /exit, /quit, /bye 退出程序\n"
                    "3. 输入 /voice list 查看可用语音\n"
                    "4. 输入 /voice set 设置新的语音ID\n"
                )
                if self.running:
                    self.start_greet_timer()
            else:
                self.append_text("未知命令，请输入 /help 查看帮助。")
                if self.running:
                    self.start_greet_timer()

    def show_voices(self):
        voices = list_chinese_voices()
        messagebox.showinfo("可用语音", "\n".join(voices) if voices else "未获取到语音列表")

    def set_voice(self):
        new_voice = simpledialog.askstring("设置语音", "请输入新的语音ID（如 zh-CN-XiaoyiNeural）:", parent=self.root)
        if new_voice:
            self.voice = new_voice
            messagebox.showinfo("设置成功", f"已设置语音为: {self.voice}")

    def on_close(self):
        self.running = False
        if self.timer:
            self.timer.cancel()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CatGirlAIUI(root)
    root.mainloop()