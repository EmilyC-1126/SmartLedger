import plotly.express as px
import streamlit as st
import pandas as pd

def plot_spending_pie_chart(df):
    """繪製支出分類圓餅圖 (使用 Plotly)"""
    if df.empty:
        return

    # 1. 篩選：只看支出 (Category 不等於 Income)
    # 我們不把 Income 放進圓餅圖，以免比例失衡
    expenses = df[df['Category'] != 'Income']
    
    if expenses.empty:
        st.info("目前只有收入記錄，還沒有支出數據，所以圓餅圖暫時空白。")
        return

    # 2. 畫圖 (Plotly 自動處理中文)
    fig = px.pie(
        expenses, 
        values='Amount', 
        names='Category',
        title='💸 支出分佈 (按主分類)',
        hole=0.4, # 變成甜甜圈圖，比較型
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # 設定滑鼠懸停顯示格式
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    # 3. 顯示
    st.plotly_chart(fig, use_container_width=True)

def plot_trend_bar_chart(df):
    """繪製近期交易長條圖 (使用 Plotly)"""
    if df.empty:
        return

    # 為了讓圖表不至於太擠，我們只取最近 20 筆
    recent_df = df.tail(20)

    # 畫長條圖
    fig = px.bar(
        recent_df, 
        x='Date', 
        y='Amount',
        color='Category', # 不同分類不同顏色
        title='📅 近期交易趨勢 (包含收入與支出)',
        labels={'Amount': '金額', 'Date': '日期', 'Category': '分類'},
        text_auto=True # 自動在柱子上顯示數字
    )
    
    # 讓 X 軸日期顯示得簡潔點
    fig.update_layout(xaxis_title=None)

    st.plotly_chart(fig, use_container_width=True)

def plot_summary_metrics(df):
    """額外功能：顯示總收入與總支出的數字卡片"""
    if df.empty:
        return
        
    # 計算總收入
    total_income = df[df['Category'] == 'Income']['Amount'].sum()
    
    # 計算總支出
    total_expense = df[df['Category'] != 'Income']['Amount'].sum()
    
    # 計算結餘
    balance = total_income - total_expense
    
    # 顯示漂亮的三欄指標
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 總收入", f"${total_income:,.0f}", delta_color="normal")
    col2.metric("💸 總支出", f"${total_expense:,.0f}", delta_color="inverse")
    col3.metric("pig_nose 結餘", f"${balance:,.0f}")