import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def plot_spending_pie_chart(df):
    """繪製支出分類圓餅圖"""
    if df.empty:
        return

    # 1. 過濾掉 "Income" (收入)，我們只看支出
    expenses = df[df['Category'] != 'Income']
    
    if expenses.empty:
        st.info("目前沒有支出數據可供分析。")
        return

    # 2. 依照 Category 分組並加總 Amount
    category_sum = expenses.groupby('Category')['Amount'].sum()

    # 3. 設定畫布大小
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # 4. 繪製圓餅圖
    # autopct='%1.1f%%' 代表顯示小數點後一位的百分比
    # startangle=90 代表從 12 點鐘方向開始畫
    # colors 使用 pastel 色系比較柔和專業
    ax.pie(
        category_sum, 
        labels=category_sum.index, 
        autopct='%1.1f%%', 
        startangle=90,
        colors=plt.cm.Pastel1.colors
    )
    
    ax.axis('equal')  # 確保圓餅是圓的
    ax.set_title("支出分佈 (By Category)")

    # 5. 在 Streamlit 顯示圖表
    st.pyplot(fig)

def plot_trend_bar_chart(df):
    """繪製近期交易長條圖"""
    if df.empty:
        return

    # 只取最後 10 筆交易
    recent_df = df.tail(10)

    # 簡單的長條圖
    st.bar_chart(
        data=recent_df,
        x="Date",
        y="Amount",
        color="Category", # 根據分類顯示不同顏色
        use_container_width=True
    )