import llm

# 启用思考模式（相当于 /set think）
response = llm.chat(
    model="deepseek-r1:7b",
    messages=[{"role": "user", "content": "Why is the sky blue?"}],
    options={"think": True}  # 关键参数
)
print(response["message"]["content"])

# 禁用思考模式（相当于 /set nothink）
response = llm.chat(
    model="deepseek-r1:7b",
    messages=[{"role": "user", "content": "Calculate 10 + 20"}],
    options={"think": False}  # 直接输出结果
)
print(response["message"]["content"])