import streamlit as st

# 頁面配置
st.set_page_config(page_title="數字金額計算器", layout="wide")

# 1. 初始化資料
if 'inventory_logs' not in st.session_state:
    st.session_state.inventory_logs = {}

def add_transaction(item_id, up_val, down_val):
    if item_id not in st.session_state.inventory_logs:
        st.session_state.inventory_logs[item_id] = {'up': [], 'down': []}
    
    # 轉換文字為數字
    try:
        if up_val: st.session_state.inventory_logs[item_id]['up'].append(float(up_val))
        if down_val: st.session_state.inventory_logs[item_id]['down'].append(float(down_val))
    except ValueError:
        st.error("請確保輸入的是有效數字")

def format_log_text(logs):
    if not logs: return "0"
    res = []
    for i, v in enumerate(logs):
        prefix = "+" if (i > 0 and v >= 0) else ""
        res.append(f"{prefix}{v:.0f}")
    return "".join(res)

# --- UI 介面 ---
st.title("🔢 數字金額整合計算器 (快速輸入版)")

# 使用 st.container 配合鍵盤操作優化
with st.form("my_form", clear_on_submit=True):
    st.write("💡 提示：輸入完按 **Tab** 切換下一格，最後按 **Enter** 提交")
    
    # 全部改用 text_input，這樣就不會有你圖片中那個討厭的按鈕了
    item_id = st.text_input("1. 輸入編號 (如: 24 或 024):", key="id_input").strip()
    
    c_in1, c_in2 = st.columns(2)
    with c_in1:
        u_val = st.text_input("金額 (上):", key="up_input")
    with c_in2:
        d_val = st.text_input("金額 (下):", key="down_input")
    
    submit = st.form_submit_button("確認提交 (或按 Enter)")
    
    if submit:
        if not item_id:
            st.warning("請輸入編號")
        elif not u_val and not d_val:
            st.warning("請輸入金額")
        else:
            add_transaction(item_id, u_val, d_val)
            st.success(f"已記錄: {item_id}")

st.divider()

# --- 資料統計與明細 (保持不變) ---
logs = st.session_state.inventory_logs
sorted_keys = sorted(logs.keys(), key=lambda x: (len(x), x))

total_2_up, total_2_down = 0, 0
total_3_up, total_3_down = 0, 0

for idx, data in logs.items():
    s_up, s_down = sum(data['up']), sum(data['down'])
    if len(idx) <= 2:
        total_2_up += s_up; total_2_down += s_down
    else:
        total_3_up += s_up; total_3_down += s_down

stat_col1, stat_col2 = st.columns(2)
with stat_col1:
    st.info("**【0 ~ 99 統計】**")
    st.write(f"🔝 上: **${total_2_up:,.0f}** | ⬇️ 下: **${total_2_down:,.0f}**")
with stat_col2:
    st.warning("**【三位數字 統計】**")
    st.write(f"🔝 上: **${total_3_up:,.0f}** | ⬇️ 下: **${total_3_down:,.0f}**")

st.divider()
st.subheader("📊 交易明細 (緊湊模式)")

if not logs:
    st.info("目前沒有資料")
else:
    cols = st.columns(4) # 改成4欄讓畫面更扁
    for i, idx in enumerate(sorted_keys):
        data = logs[idx]
        s_up, s_down = sum(data['up']), sum(data['down'])
        with cols[i % 4]:
            st.markdown(f"**#{idx}**")
            if data['up']: st.caption(f"上:{format_log_text(data['up'])}={s_up:,.0f}")
            if data['down']: st.caption(f"下:{format_log_text(data['down'])}={s_down:,.0f}")
            st.write("---")

if st.sidebar.button("重設所有資料"):
    st.session_state.inventory_logs = {}
    st.rerun()
