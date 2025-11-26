import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import streamlit as st

COLUMNS = ["Date", "Amount", "Currency", "Category", "Sub_Category", "Description", "Payer"]

def get_connection():
    return st.connection("gsheets", type=GSheetsConnection)

def load_data():
    """讀取數據：現在會使用預設快取，速度會變很快"""
    conn = get_connection()
    try:
        # 修改 1: 移除 ttl=0，使用預設快取 (Streamlit 預設 cache 10分鐘)
        df = conn.read()
        
        if df.empty or len(df.columns) == 0:
            return pd.DataFrame(columns=COLUMNS)
        
        for col in COLUMNS:
            if col not in df.columns:
                df[col] = ""
                
        df = df.dropna(how="all")
        
        if 'Amount' in df.columns:
            # 確保金額格式正確
            df['Amount'] = df['Amount'].astype(str).str.replace(',', '')
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)
            
        return df
        
    except Exception as e:
        print(f"讀取錯誤: {e}")
        return pd.DataFrame(columns=COLUMNS)

def save_transaction(data):
    """存入數據：只有在存檔時才會有等待時間"""
    
    new_row = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Amount": data.get("amount"),
        "Currency": data.get("currency"),
        "Category": data.get("category"),
        "Sub_Category": data.get("sub_category"),
        "Description": data.get("description"),
        "Payer": data.get("payer")
    }
    
    conn = get_connection()
    
    # 這裡我們需要讀最新的數據來做 Append，所以這裡單獨加 ttl=0 比較保險
    # 但為了簡單，直接讀 cache 也可以，因為我們會 overwrite update
    existing_data = load_data()
    
    new_df = pd.DataFrame([new_row])
    updated_df = pd.concat([existing_data, new_df], ignore_index=True)
    
    # 寫入 Google Sheets (這一步最花時間，是正常的)
    conn.update(data=updated_df)
    
    # 修改 2: 關鍵！寫入成功後，立刻清除快取
    # 這樣下一次 load_data() 執行時，因為沒有快取了，就會被迫去 Google 拿最新的
    st.cache_data.clear()
    
    return True