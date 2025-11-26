import os
from dotenv import load_dotenv
from google import genai

# 1. 載入環境變數
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. 初始化 Client
client = genai.Client(api_key=api_key)

print("🔍 正在查詢你的帳號可用的 Gemini 模型列表...\n")

try:
    # 3. 列出所有模型
    # 我們只列出支援 "generateContent" (生成內容) 的模型
    for model in client.models.list():
        # 簡單過濾一下，只顯示 Gemini 系列
        if "gemini" in model.name:
            print(f"👉 {model.name}")
            # 顯示它是否支援生成內容 (通常都支援，但確認一下也好)
            # print(f"   - ID: {model.name.split('/')[-1]}") 

    print("\n✅ 查詢完成！請從上面選一個名字填入 ai_handler.py")

except Exception as e:
    print(f"❌ 查詢失敗: {e}")