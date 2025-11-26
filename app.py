import streamlit as st
import pandas as pd
from ai_handler import ask_ai_to_categorize
from data_manager import load_data, save_transaction

# 1. 設定網頁
st.set_page_config(page_title="SmartLedger AI", page_icon="💰", layout="centered")
st.title("🏡 SmartLedger 家庭智能記帳")

# --- Session State 初始化 ---
# 用來暫存 AI 分析出來的結果，防止按鈕刷新後消失
if 'current_data' not in st.session_state:
    st.session_state['current_data'] = None

# 2. 輸入區塊
st.subheader("📝 新增帳目")
user_input = st.text_input(
    "請輸入消費內容：", 
    placeholder="例如：今晚同 Mary 食日本野用咗 800 蚊",
    key="input_text"
)

# 3. AI 分析按鈕
if st.button("✨ AI 智能分析", type="primary"):
    if not user_input:
        st.warning("⚠️ 請先輸入內容！")
    else:
        with st.spinner("🤖 AI 正在思考分類中..."):
            ai_result = ask_ai_to_categorize(user_input)
            
            if ai_result:
                # 處理 List 情況，取第一筆
                if isinstance(ai_result, list):
                    st.session_state['current_data'] = ai_result[0]
                else:
                    st.session_state['current_data'] = ai_result
            else:
                st.error("AI 分析失敗，請重試。")

# 4. 顯示分析結果與儲存按鈕
# 只有當 session_state 裡面有資料時才顯示這塊
if st.session_state['current_data']:
    data = st.session_state['current_data']
    
    with st.container(border=True):
        st.subheader(f"{data.get('emoji', '📝')} 確認交易明細")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 金額", f"{data.get('amount')} {data.get('currency')}")
        with col2:
            st.metric("🏷️ 分類", f"{data.get('category')} > {data.get('sub_category')}")
        with col3:
            st.metric("👤 付款人", data.get('payer'))
        
        st.text(f"摘要: {data.get('description')}")
        
        # --- 儲存按鈕 ---
        if st.button("✅ 確認並儲存"):
            save_transaction(data)
            st.success("🎉 交易已儲存！")
            
            # 清空暫存，準備下一筆
            st.session_state['current_data'] = None
            # 重新執行網頁以更新下方的表格
            st.rerun()

# 5. 顯示歷史交易紀錄
st.divider()
st.subheader("📊 最近交易紀錄")

# 讀取並顯示 CSV
df = load_data()
if not df.empty:
    # 按照時間倒序排列 (最新的在上面)
    df = df.sort_values(by="Date", ascending=False)
    st.dataframe(df, use_container_width=True)
else:
    st.info("目前還沒有交易紀錄，快輸入第一筆吧！")