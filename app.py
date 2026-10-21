import streamlit as st
import pandas as pd
from datetime import datetime

# ページ基本設定（スマホ向けレイアウト）
st.set_page_config(page_title="FXトレード＆市場記録簿", page_icon="📈", layout="centered")

st.title("📈 FX記録簿 & 市場メモ")

# --- データの初期化（セッション状態） ---
if "trade_data" not in st.session_state:
    st.session_state.trade_data = []

# --- タブの作成 ---
tab1, tab2 = st.tabs(["📝 記録入力", "📊 履歴・集計"])

with tab1:
    st.header("今日の市場環境 & トレード記録")
    
    with st.form("fx_form", clear_on_submit=True):
        date = st.date_input("日付", datetime.now())
        
        st.subheader("🌐 市場環境メモ")
        jp_market = st.text_area("日本市場の状況（日経平均、日銀動向、円相場の背景など）", placeholder="例: 日経平均反落。日銀総裁発言により円高進行。")
        world_market = st.text_area("世界市場の状況（米金利、株価、指標発表など）", placeholder="例: 米CPIが予想上振れ、米長期金利上昇でドル買い。")
        market_mood = st.selectbox("市場の雰囲気", ["リスクオン", "リスクオフ", "レンジ・拮抗", "その他"])
        
        st.subheader("⚔️ トレード詳細")
        pair = st.selectbox("通貨ペア", ["USD/JPY", "EUR/JPY", "GBP/JPY", "EUR/USD", "GBP/USD", "AUD/JPY", "その他"])
        trade_type = st.radio("売買区分", ["買い (Long)", "売り (Short)"], horizontal=True)
        
        col1, col2 = st.columns(2)
        with col1:
            pips = st.number_input("獲得pips", value=0.0, step=0.1)
        with col2:
            pnl = st.number_input("損益（円）", value=0, step=100)
            
        memo = st.text_area("エントリー根拠・反省点メモ", placeholder="例: チャネル下限での反発を狙ってロング。利確が早すぎた。")
        
        submitted = st.form_submit_dict("記録を保存") if hasattr(st, "form_submit_dict") else st.form_submit_button("記録を保存")
        
        if submitted:
            st.session_state.trade_data.append({
                "日付": date.strftime("%Y/%m/%d"),
                "通貨ペア": pair,
                "売買": trade_type,
                "獲得pips": pips,
                "損益（円）": pnl,
                "市場雰囲気": market_mood,
                "日本市場": jp_market,
                "世界市場": world_market,
                "メモ": memo
            })
            st.success("トレード記録を保存しました！")

with tab2:
    st.header("📊 トレード履歴とサマリー")
    
    if st.session_state.trade_data:
        df = pd.DataFrame(st.session_state.trade_data)
        
        # 簡易集計
        total_pnl = df["損益（円）"].sum()
        total_pips = df["獲得pips"].sum()
        win_rate = (df["損益（円）"] > 0).mean() * 100
        
        col1, col2, col3 = st.columns(3)
        col1.metric("合計損益", f"{total_pnl:,} 円")
        col2.metric("合計pips", f"{total_pips:.1f} pips")
        col3.metric("勝率", f"{win_rate:.1f} %")
        
        st.subheader("📋 履歴一覧")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("まだ記録はありません。データを入力をするとここに表示されます。")
