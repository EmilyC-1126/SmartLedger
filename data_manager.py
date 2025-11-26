import pandas as pd
import os
from datetime import datetime

CSV_FILE = "ledger_data.csv"

def load_data():
    """讀取現有的記帳數據，如果檔案不存在則建立一個空的"""
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        # 定義 Excel 表格的欄位名稱
        columns = ["Date", "Amount", "Currency", "Category", "Sub_Category", "Description", "Payer"]
        return pd.DataFrame(columns=columns)

def save_transaction(data):
    """將單筆交易存入 CSV 檔案"""
    
    # 1. 準備要寫入的一行資料
    new_row = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Amount": data.get("amount"),
        "Currency": data.get("currency"),
        "Category": data.get("category"),
        "Sub_Category": data.get("sub_category"),
        "Description": data.get("description"),
        "Payer": data.get("payer")
    }
    
    # 2. 載入舊資料
    df = load_data()
    
    # 3. 加入新資料 (使用 concat 代替 append，因為 append 在新版 pandas 已被移除)
    new_df = pd.DataFrame([new_row])
    df = pd.concat([df, new_df], ignore_index=True)
    
    # 4. 存回檔案 (index=False 代表不要儲存 0,1,2... 那些行號)
    df.to_csv(CSV_FILE, index=False)
    
    return True