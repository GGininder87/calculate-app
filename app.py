import streamlit as st

# 頁面配置
st.set_page_config(page_title="數字金額計算器", layout="wide")

# 1. 初始化資料
if 'inventory_logs' not in st.session_state:
    st.session_state.inventory_logs = {}

def add_transaction(item_id, up_val, down_val):
    if item_id not in st.session_state.inventory_logs:
        st.session_state.inventory_logs[item_id] = {'up': [], 'down': []}
    if up_val is not None:
        st.session_state.inventory_logs[item_id]['up'].append(up_val)
    if down_val is not None:
        st.session_state.inventory_logs[item_id]['down'].append(down_val)

def format_log_text(logs):
    """將 [100, 50] 轉為 '100+50'"""
    if not logs: return "0"
    res = []
    for i, v in enumerate(logs):
        prefix = "+" if (i > 0 and v >= 0) else ""
        res.append(f"{prefix}{v:.0f}")
    return "".join(res)

# --- UI 介面 ---
st.title("🔢 數字金額整合計算器 (緊湊版)")

with st.form("my_form", clear_on_submit=True):
    item_id = st.text_input("1. 輸入編號 (區分 24 與 024):").strip()
    c_in1, c_in2 = st.columns(2)
    with c_in1:
        u_val = st.number_input("金額 (上):", value=None, step=1)
    with c_in2:
        d_val = st.number_input("金額 (下):", value=None, step=1)
    
    if st.form_submit_button("確認提交"):
        if not item_id:
            st.warning("請輸入編號")
        elif u_val is None and d_val is None:
            st.warning("請輸入金額")
        else:
            add_transaction(item_id, u_val, d_val)
            st.success(f"已記錄: {item_id}")

st.divider()

# --- 資料統計邏輯 ---
logs = st.session_state.inventory_logs
sorted_keys = sorted(logs.keys(), key=lambda x: (len(x), x))

# 分類總計變數
total_2_up, total_2_down = 0, 0   # 0-99 (長度 1~2)
total_3_up, total_3_down = 0, 0   # 三位數 (長度 3 以上)

# 顯示統計數據
st.subheader("💰 分類統計回報")
stat_col1, stat_col2 = st.columns(2)

# 先計算
for idx, data in logs.items():
    s_up = sum(data['up'])
    s_down = sum(data['down'])
    if len(idx) <= 2:
        total_2_up += s_up
        total_2_down += s_down
    else:
        total_3_up += s_up
        total_3_down += s_down

with stat_col1:
    st.info("**【0 ~ 99 統計】**")
    st.write(f"🔝 上累計: **${total_2_up:,.0f}**")
    st.write(f"⬇️ 下累計: **${total_2_down:,.0f}**")

with stat_col2:
    st.warning("**【三位數字 統計】**")
    st.write(f"🔝 上累計: **${total_3_up:,.0f}**")
    st.write(f"⬇️ 下累計: **${total_3_down:,.0f}**")

st.divider()

# --- 緊湊顯示明細 ---
st.subheader("📊 交易明細 (緊湊模式)")

if not logs:
    st.info("目前沒有資料")
else:
    # 為了讓畫面更小，我們不使用 expander，改用多欄位顯示
    # 每行顯示 3 個編號，節省垂直空間
    cols = st.columns(3)
    for i, idx in enumerate(sorted_keys):
        data = logs[idx]
        s_up = sum(data['up'])
        s_down = sum(data['down'])
        
        # 決定放在哪一欄
        with cols[i % 3]:
            # 用 markdown 做出一個緊湊的小方框感覺
            st.markdown(f"**#{idx}**")
            if data['up']:
                st.caption(f"上: {format_log_text(data['up'])} = **{s_up:,.0f}**")
            if data['down']:
                st.caption(f"下: {format_log_text(data['down'])} = **{s_down:,.0f}**")
            st.write("---")

if st.sidebar.button("重設所有資料"):
    st.session_state.inventory_logs = {}
    st.rerun()

# --- 程式碼完整結束標記 ---
