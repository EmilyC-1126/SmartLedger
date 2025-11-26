import streamlit as st
import pandas as pd
from ai_handler import ask_ai_to_categorize

# 1. 設定網頁標題與版面
st.set_page_config(page_title="SmartLedger AI", page_icon="💰", layout="centered")

st.title("🏡 SmartLedger 家庭智能記帳")
st.write("輸入一句話，讓 AI 幫你自動分類！")

# 2. 建立輸入區塊
# st.text_input 建立一個文字輸入框
user_input = st.text_input(
    "📝 請輸入消費內容：", 
    placeholder="例如：今晚同 Mary 食日本野用咗 800 蚊",
    help="你可以輸入任何語言，AI 都聽得懂！"
)

# 3. 建立按鈕與觸發邏輯
if st.button("✨ AI 智能分析", type="primary"):
    if not user_input:
        st.warning("⚠️ 請先輸入內容！")
    else:
        # 顯示轉圈圈的載入動畫
        with st.spinner("🤖 AI 正在思考分類中..."):
            # 呼叫我们在 ai_handler.py 寫好的函數
            ai_result = ask_ai_to_categorize(user_input)

        # 4. 顯示結果
        if ai_result:
            # 處理回傳格式：如果 AI 回傳的是 List [{}], 我們取第一個
            if isinstance(ai_result, list):
                data = ai_result[0]
            else:
                data = ai_result

            # 使用 Streamlit 的 container 來美化顯示
            with st.container(border=True):
                st.subheader(f"{data.get('emoji', '📝')} 識別結果")
                
                # 建立三欄排版
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("💰 金額", f"{data.get('amount', 0)} {data.get('currency', 'HKD')}")
                with col2:
                    st.metric("🏷️ 分類", f"{data.get('category')} > {data.get('sub_category')}")
                with col3:
                    st.metric("👤 付款人", data.get('payer', 'Me'))
                
                st.info(f"📋 摘要: {data.get('description')}")
            
            # 暫時顯示原始 JSON (方便除錯，之後會移除)
            with st.expander("查看原始數據 (Debug)"):
                st.json(data)
                
            st.success("🎉 分析成功！(目前僅為預覽，尚未儲存)")
            
        else:
            st.error("❌ AI 分析失敗，請稍後再試。")