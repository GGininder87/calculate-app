import streamlit as st

# 1. 初始化 Session State (確保數據在同一節點內不會因刷新而消失)
if 'inventory_logs' not in st.session_state:
    st.session_state.inventory_logs = {}

def add_transaction(item_id, amount_up, amount_down):
    """將交易金額加入指定編號的紀錄中"""
    if item_id not in st.session_state.inventory_logs:
        st.session_state.inventory_logs[item_id] = {'up': [], 'down': []}
    
    if amount_up is not None:
        st.session_state.inventory_logs[item_id]['up'].append(amount_up)
    if amount_down is not None:
        st.session_state.inventory_logs[item_id]['down'].append(amount_down)
    
    st.success(f"✅ 編號 「{item_id}」 紀錄成功！")

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
    st.subheader("📊 交易明細與最終成果")
    
    # 排序編號：確保 24, 024 會分開顯示但排在一起
    sorted_keys = sorted(st.session_state.inventory_logs.keys())
    
    display_data = False
    for item_id in sorted_keys:
        data = st.session_state.inventory_logs[item_id]
        if data['up'] or data['down']:
            display_data = True
            total_up = sum(data['up'])
            total_down = sum(data['down'])
            
            with st.expander(f"🔢 編號: {item_id}", expanded=True):
