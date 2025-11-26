import os
from dotenv import load_dotenv
from google import genai

# 1. 載入環境變數
# 這行程式碼會去讀取你剛剛建立的 .env 檔案
load_dotenv()

# 2. 安全地獲取 API Key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # 如果找不到 Key，程式會在這裡停止並報錯
    raise ValueError("❌ 找不到 API Key！請檢查 .env 檔案是否設定正確。")

print("✅ API Key 讀取成功！準備連線...")

# 3. 初始化 Gemini 客戶端
# 使用最新的 google-genai SDK
client = genai.Client(api_key=api_key)

try:
    # 4. 簡單測試呼叫：請 AI 講一句關於記帳的話
    print("正在呼叫 Gemini AI，請稍等...")
    
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents="你好，請用一句簡短的話形容「記帳」對家庭的重要性。"
    )
    
    print("\n🤖 Gemini 回應：")
    print(response.text)
    print("\n🎉 恭喜！環境設定成功，我們可以開始寫 App 了！")

except Exception as e:
    print(f"\n❌ 連線發生錯誤: {e}")