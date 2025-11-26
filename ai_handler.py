import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. 載入環境變數
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. 初始化 Client
client = genai.Client(api_key=api_key)

def ask_ai_to_categorize(user_input):
    """
    將使用者的自然語言輸入，轉換為結構化的 JSON 記帳資料
    """
    
    # 設定 Prompt (提示詞)：教 AI 點樣做野
    prompt = f"""
    你是一位專業的家庭會計師。請分析以下的使用者輸入，並將其轉換為 JSON 格式。
    
    使用者輸入: "{user_input}"
    
    請遵循以下規則：
    1. 提取金額 (amount) 和貨幣 (currency, 預設為 HKD)。
    2. 根據內容判斷 category (主分類) 和 sub_category (子分類)。
       - 建議的主分類: Food, Transport, Housing, Shopping, Utilities, Entertainment, Health, Income.
       - 如果是收入，category 請設為 "Income"。
    3. 提取 description (具體項目摘要)。
    4. 提取 payer (付款人)，如果沒提到，預設為 "Me"。
    5. 推薦一個適合該分類的 emoji 圖案。
    6. 不要輸出任何 Markdown 標記，只輸出純 JSON。
    
    JSON 輸出格式範例:
    {{
        "amount": 100.5,
        "currency": "HKD",
        "category": "Food",
        "sub_category": "Groceries",
        "description": "買菜",
        "payer": "Me",
        "emoji": "🥦"
    }}
    """

    try:
        # 3. 呼叫 Gemini
        # response_mime_type="application/json" 係關鍵！強迫 AI 嘔 JSON 比我地
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite-001",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        # 4. 將回傳的文字轉成 Python 字典 (Dictionary)
        result = json.loads(response.text)
        return result

    except Exception as e:
        print(f"AI 分析錯誤: {e}")
        return None

# 簡單測試區塊 (只有直接執行這個檔案時才會跑)
if __name__ == "__main__":
    test_input = "琴日同Mary去迪士尼玩買飛用左1200蚊"
    print(f"測試輸入: {test_input}")
    print("AI 正在思考中...")
    
    data = ask_ai_to_categorize(test_input)
    
    if data:
        print("\n✅ AI 成功解析：")
        print(json.dumps(data, indent=4, ensure_ascii=False))
    else:
        print("❌ 測試失敗")