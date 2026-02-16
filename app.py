import streamlit as st

# 初始化 Session State 來儲存數據
if 'inventory_logs' not in st.session_state:
    # 每個商品編號 (0-999) 對應一個字典，分別存放「上」和「下」的清單
    st.session_state.inventory_logs = {i: {'up': [], 'down': []} for i in range(1000)}

def add_transaction(item_number, amount_up, amount_down):
    """將交易金額分別加入「上」和「下」的清單中"""
    if amount_up is not None:
        st.session_state.inventory_logs[item_number]['up'].append(amount_up)
    if amount_down is not None:
        st.session_state.inventory_logs[item_number]['down'].append(amount_down)
    
    st.success(f"✅ 數字 {item_number} 紀錄成功！")

def format_log(logs):
    """將數字列表轉為算式字串"""
    if not logs:
        return "0"
    log_str = ""
    for i, val in enumerate(logs):
        if i == 0:
            log_str += f"{val:.0f}"
        elif val >= 0:
            log_str += f" + {val:.0f}"
        else:
            log_str += f" {val:.0f}"
    return log_str

def display_totals_table():
    """顯示交易明細與總額"""
    display_data = False
    
    st.subheader("📊 交易明細與最終成果")
    
    # 過濾出有資料的編號並顯示
    for item_number, data in st.session_state.inventory_logs.items():
        if data['up'] or data['down']:
            display_data = True
            total_up = sum(data['up'])
            total_down = sum(data['down'])
            
            log_up_str = format_log(data['up'])
            log_down_str = format_log(data['down'])
            
            # 使用卡片式佈局顯示
            with st.expander(f"🔢 編號: {item_number}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**🔝 金額 (上):**")
                    st.code(log_up_str, language="text")
                    st.write(f"小計: `${total_up:,.0f}`")
                with col2:
                    st.markdown(f"**⬇️ 金額 (下):**")
                    st.code(log_down_str, language="text")
                    st.write(f"小計: `${total_down:,.0f}`")

    if not display_data:
        st.info("目前尚無任何交易記錄。")
        return

    # 計算整體總和
    all_up_total = sum(sum(d['up']) for d in st.session_state.inventory_logs.values())
    all_down_total = sum(sum(d['down']) for d in st.session_state.inventory_logs.values())
    
    st.markdown("---")
    st.markdown(f"### 💰 總累積金額回報")
    c1, c2 = st.columns(2)
    c1.metric("總金額 (上) 累計", f"${all_up_total:,.0f}")
    c2.metric("總金額 (下) 累計", f"${all_down_total:,.0f}")

# --- UI 介面 ---
st.set_page_config(page_title="數字金額計算器", layout="wide")
st.title("🔢 數字金額整合計算器")

with st.form("transaction_form", clear_on_submit=True):
    # 數字編號 0-999，預設空白
    item_number = st.number_input("1. 輸入數字編號 (0 - 999):", min_value=0, max_value=999, step=1, value=None)
    
    st.write("2. 輸入交易金額:")
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        amount_up = st.number_input("金額 (上):", step=1, value=None)
    with col_input2:
        amount_down = st.number_input("金額 (下):", step=1, value=None)
    
    submitted = st.form_submit_button("確認提交 (Submit)")
    
    if submitted:
        if item_number is None:
            st.warning("請先輸入『數字編號』再提交。")
        elif amount_up is None and amount_down is None:
            st.warning("請至少填寫一個金額（上或下）。")
        else:
            add_transaction(int(item_number), amount_up, amount_down)

display_totals_table()
