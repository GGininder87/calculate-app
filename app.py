這個需求非常合理！這能讓你的帳單或紀錄看起來更整齊。

要達成「先排兩位數（0-99），再排三位數（000-999）」的邏輯，我們需要在顯示前將編號（ID）進行 「長度優先，數值次之」 的排序。

以下是修改後的完整程式碼。我已經加入了排序邏輯，並且保留了你要求的「重複輸入則顯示加總過程（100 + 50 = 150）」功能。

完整修復版程式碼
Python
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
    """將 [100, 50] 轉為 '100 + 50'"""
    if not logs: return "0"
    res = []
    for i, v in enumerate(logs):
        # 第一筆不加符號，之後的正數加 +
        prefix = "+" if (i > 0 and v >= 0) else ""
        res.append(f"{prefix}{v:.0f}")
    return " ".join(res)

# --- UI 介面 ---
st.title("🔢 數字金額整合計算器")

with st.form("my_form", clear_on_submit=True):
    item_id = st.text_input("1. 輸入編號 (如: 24 或 024):").strip()
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
    # --- 排序邏輯 ---
    # 排序規則：先比字串長度 (len)，再比字串內容 (x)
    # 這樣 2 位的 (如 24) 就會排在 3 位的 (如 024) 前面
    sorted_keys = sorted(logs.keys(), key=lambda x: (len(x), x))
    
    for idx in sorted_keys:
        data = logs[idx]
        if data['up'] or data['down']:
            sum_up = sum(data['up'])
            sum_down = sum(data['down'])
            
            with st.expander(f"編號: {idx}", expanded=True):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write("**🔝 上:**")
                    log_up = format_log_text(data['up'])
                    # 顯示格式：100 + 50 = 150
                    st.code(f"{log_up} = {sum_up:,.0f}", language="text")
                with col_b:
                    st.write("**⬇️ 下:**")
                    log_down = format_log_text(data['down'])
                    st.code(f"{log_down} = {sum_down:,.0f}", language="text")

    st.divider()
    t_up = sum(sum(d['up']) for d in logs.values())
    t_down = sum(sum(d['down']) for d in logs.values())
    
    f1, f2 = st.columns(2)
    f1.metric("總金額 (上) 累計", f"${t_up:,.0f}")
    f2.metric("總金額 (下) 累計", f"${t_down:,.0f}")

if st.sidebar.button("重設所有資料"):
    st.session_state.inventory_logs = {}
    st.rerun()

# --- 程式碼完整結束標記 ---
