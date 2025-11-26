import streamlit as st
import pandas as pd
from ai_handler import ask_ai_to_categorize
from data_manager import load_data, save_transaction
# 記得要 import 圖表功能
from charts import plot_spending_pie_chart, plot_trend_bar_chart

# 1. 設定網頁
st.set_page_config(page_title="SmartLedger AI", page_icon="💰", layout="centered")
st.title("🏡 SmartLedger 家庭智能記帳")

# --- Session State 初始化 ---
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
                if isinstance(ai_result, list):
                    st.session_state['current_data'] = ai_result[0]
                else:
                    st.session_state['current_data'] = ai_result
            else:
                st.error("AI 分析失敗，請重試。")

# 4. 顯示分析結果與儲存按鈕
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
            with st.spinner("正在寫入 Google Sheets..."):
                save_transaction(data)
            
            st.success("🎉 交易已儲存！")
            st.session_state['current_data'] = None
            
            # 強制刷新頁面，讓下方的表格和圖表即時更新
            st.rerun()

# 5. 顯示歷史交易紀錄與圖表
st.divider()

# 每次都重新讀取最新數據
df = load_data()

if not df.empty:
    tab1, tab2 = st.tabs(["📊 財務報表", "📈 數據分析"])
    
    with tab1:
        st.subheader("最近交易紀錄")
        df_display = df.sort_values(by="Date", ascending=False)
        st.dataframe(df_display, use_container_width=True)

    with tab2:
        st.subheader("財務視覺化分析")
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("### 支出佔比")
            plot_spending_pie_chart(df)
            
        with col_right:
            st.markdown("### 近期趨勢")
            plot_trend_bar_chart(df)

else:
    st.info("目前還沒有交易紀錄，快輸入第一筆吧！")