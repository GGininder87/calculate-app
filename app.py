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
    if not logs: return "0"
    res = []
    for i, v in enumerate(logs):
        prefix = "+" if (i > 0 and v >= 0) else ""
        res.append(f"{prefix}{v:.0f}")
    return " ".join(res)

# --- UI 介面 ---
st.title("🔢 數字金額整合計算器")

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
st.subheader("📊 交易明細")

logs = st.session_state.inventory_logs
if not logs:
    st.info("目前沒有資料")
else:
    for idx in sorted(logs.keys()):
        data = logs[idx]
        if data['up'] or data['down']:
            sum_up = sum(data['up'])
            sum_down = sum(data['down'])
            with st.expander(f"編號: {idx}", expanded=True):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write("**🔝 上:**")
                    st.code(format_log_text(data['up']))
                    st.write(f"小計: ${sum_up:,.0f}")
                with col_b:
                    st.write("**⬇️ 下:**")
                    st.code(format_log_text(data['down']))
                    st.write(f"小計: ${sum_down:,.0f}")

    st.divider()
    t_up = sum(sum(d['up']) for d in logs.values())
    t_down = sum(sum(d['down'])
