import streamlit as st

# 初始化 Session State
if 'inventory_logs' not in st.session_state:
    # 改用空字典，因為編號現在是「文字」，我們動態增加 key
    st.session_state.inventory_logs = {}

def add_transaction(item_id, amount_up, amount_down):
    """將交易金額加入指定編號（文字型態）的紀錄中"""
    # 如果這個編號還沒出現過，先初始化它
    if item_id not in st.session_state.inventory_logs:
        st.session_state.inventory_logs[item_id] = {'up': [], 'down': []}
    
    if amount_up is not None:
        st.session_state.inventory_logs[item_id]['up'].append(amount_up)
    if amount_down is not None:
        st.session_state.inventory_logs[item_id]['down'].append(amount_down)
    
    st.success(f"✅ 編號 「{item_id}」 紀錄成功！")

def format_log(logs):
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
    st.subheader("📊 交易明細與最終成果")
    
    # 將 key 排序後顯示（讓 024 跟 24 放在一起方便查看，但分開計算）
    sorted_keys = sorted(st.session_state.inventory_logs.keys())
    
    display_data = False
    for item_id in sorted_keys:
        data = st.session_state.inventory_logs[item_id]
        if data['up'] or data['down']:
            display_data = True
            total_up = sum(data['up'])
            total_down = sum(data['down'])
            
            with st.expander(f"🔢 編號: {item_id}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**🔝 金額 (上):**")
                    st.code(format_log(data['up']), language="text")
                    st.write(f"小計: `${total_up:,.0f}`")
                with col2:
                    st.markdown(f"**⬇️ 金額 (下):**")
                    st.code(format_log(data['down']), language="text")
                    st.write(f"小計: `${total_down:,.0f}`")

    if not display_data:
        st.info("目前尚無任何交易記錄。")
        return

    # 總計
    all_up_total = sum(sum(d['
