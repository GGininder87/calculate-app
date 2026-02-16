import streamlit as st

# 設定頁面資訊 (必須放在第一行)
st.set_page_config(page_title="數字金額計算器", layout="wide")

# 1. 初始化資料結構
if 'inventory_logs' not in st.session_state:
    st.session_state.inventory_logs = {}

# 2. 處理新增資料
def add_transaction(item_id, up_val, down_val):
    if item_id not in st.session_state.inventory_logs:
        st.session_state.inventory_logs[item_id] = {'up': [], 'down': []}
    
    if up_val is not None:
        st.session_state.inventory_logs[item_id]['up'].append(up_val)
    if down_val is not None:
        st.session_state.inventory_logs[item_id]['down'].append(down_val)

# 3. 格式化顯示文字
def format_log_text(logs):
    if not logs:
        return "0"
    items = []
    for i, v in enumerate(logs):
        if i == 0:
            items.append(f"{v:.0f}")
        else:
            prefix = "+" if v >= 0 else ""
            items.append(f"{prefix}{v:.0f}")
    return " ".join(items)

# --- UI 介面 ---
st.title("🔢 數字金額整合計算器")

# 輸入表單
with st.form("my_form", clear_on_submit=True):
    # 使用 text_input 區分 "24" 與 "024"
    item_id = st.text_input("1. 輸入編號 (例如: 24 或 024):").strip()
    
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        u_val = st.number_input("金額 (上):", value=None, step=1)
    with col_in2:
        d_val = st.number_input("金額 (下):", value=None, step=1)
    
    submit = st.form_submit_button("確認提交")
    
    if submit:
        if not item_id:
            st.warning("請輸入編號")
        elif u_val is None and d_val is None:
            st.warning("請輸入金額")
        else:
            add_transaction(item_id, u_val, d_val)
            st.success(f"已記錄編號: {item_id}")

st.divider()

# 4. 顯示結果
st.subheader("📊 交易明細")

logs = st.session_state.inventory_logs

if not logs:
    st.info("目前沒有資料")
else:
    # 排序編號
    for idx in sorted(logs.keys()):
        data = logs[idx]
        if data['up'] or data['down']:
            # 計算總額
            sum_up = sum(data['up'])
            sum_down = sum(data['down'])
            
            # 顯示卡片
            with st.expander(f"編號: {idx}", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.write("**🔝 上:**")
                    st.code(format_log_text(data['up']))
                    st.write(f"小計: ${sum_up:,.0f}")
                with c2:
                    st.write("**⬇️ 下:**")
                    st.code(format_log_text(data['down']))
                    st.write(f"小計: ${sum_down:,.0f}")

    # 總累積回報
    st.divider()
    total_all_up = sum(sum(d['up']) for d in logs.values())
    total_all_down = sum(sum(d['down']) for d in logs.values())
    
    final_c1, final_c2 = st.columns(2)
    final_c1.metric("總金額 (上)
