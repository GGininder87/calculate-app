import streamlit as st

# 1. 頁面配置
st.set_page_config(page_title="數字金額計算器", layout="wide")

# 2. 初始化資料
if 'inventory_logs' not in st.session_state:
    st.session_state.inventory_logs = {}

# 3. 處理提交逻辑
def add_transaction(item_id, up_val, down_val):
    if item_id not in st.session_state.inventory_logs:
        st.session_state.inventory_logs[item_id] = {'up': [], 'down': []}
    try:
        if up_val: st.session_state.inventory_logs[item_id]['up'].append(float(up_val))
        if down_val: st.session_state.inventory_logs[item_id]['down'].append(float(down_val))
        return True
    except ValueError:
        st.error("金額請輸入純數字")
        return False

def format_log_text(logs):
    if not logs: return "0"
    res = []
    for i, v in enumerate(logs):
        prefix = "+" if (i > 0 and v >= 0) else ""
        res.append(f"{prefix}{v:.0f}")
    return "".join(res)

# --- UI 介面 ---
st.title("🔢 快速輸入計算器")

# 【核心修復】使用 placeholder 重新渲染表單
placeholder = st.empty()

with placeholder.container():
    with st.form("input_form", clear_on_submit=True):
        st.markdown("⌨️ **操作：** 編號 → `Tab` → 上 → `Tab` → 下 → `Enter` (提交後自動回位)")
        
        # 在這裡加入在 Streamlit 中隱藏的關鍵屬性
        item_id = st.text_input("1. 輸入編號 (區分 24 與 024):", key="id_input").strip()
        
        c_in1, c_in2 = st.columns(2)
        with c_in1:
            u_val = st.text_input("2. 金額 (上):", key="up_input")
        with c_in2:
            d_val = st.text_input("3. 金額 (下):", key="down_input")
        
        submit = st.form_submit_button("確認提交 (Enter)")
        
        if submit:
            if not item_id:
                st.warning("請輸入編號")
            elif not u_val and not d_val:
                st.warning("請輸入金額")
            else:
                if add_transaction(item_id, u_val, d_val):
                    st.toast(f"✅ 已紀錄: {item_id}", icon='🚀')
                    # 這一行會強迫整個頁面重新整理，並因為 clear_on_submit 讓游標回到第一個 input
                    st.rerun()

st.divider()

# --- 資料統計 ---
logs = st.session_state.inventory_logs
sorted_keys = sorted(logs.keys(), key=lambda x: (len(x), x))

t2_up, t2_down, t3_up, t3_down = 0, 0, 0, 0
for idx, data in logs.items():
    s_up, s_down = sum(data['up']), sum(data['down'])
    if len(idx) <= 2:
        t2_up += s_up; t2_down += s_down
    else:
        t3_up += s_up; t3_down += s_down

c1, c2 = st.columns(2)
with c1: st.info(f"**0~99 統計** | 🔝 上: `${t2_up:,.0f}` | ⬇️ 下: `${t2_down:,.0f}`")
with c2: st.warning(f"**三位數 統計** | 🔝 上: `${t3_up:,.0f}` | ⬇️ 下: `${t3_down:,.0f}`")

st.divider()

# --- 明細顯示 ---
if not logs:
    st.info("目前沒有資料")
else:
    display_cols = st.columns(5)
    for i, idx in enumerate(sorted_keys):
        data = logs[idx]
        s_up, s_down = sum(data['up']), sum(data['down'])
        with display_cols[i % 5]:
            st.markdown(f"**#{idx}**")
            if data['up']: st.caption(f"上:{format_log_text(data['up'])}={s_up:,.0f}")
            if data['down']: st.caption(f"下:{format_log_text(data['down'])}={s_down:,.0f}")
            st.write("---")

if st.sidebar.button("重設所有資料"):
    st.session_state.inventory_logs = {}
    st.rerun()
