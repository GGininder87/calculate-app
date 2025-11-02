好的，沒問題！這是一個簡單的文字和格式調整，讓您的 App 標題和輸出更精煉。

✅ 修正：調整標題和移除「商品」文字
我已經根據您的要求對程式碼進行了兩處調整：

標題修改：

將 "📊 商品交易明細與最終結果" 改為 "📊 交易明細與最終成果"。

結果格式修改：

將 f"商品 {item_number}: {log_str} = ${total_amount:,.0f}"

改為 f"{item_number}: {log_str} = ${total_amount:,.0f}"，移除了「商品」兩字。

請您完全替換您 app.py 檔案中的內容，使用下面這段更新後的程式碼。

💻 完整且已修正的 Streamlit 程式碼 (最終版本)
Python

import streamlit as st
import pandas as pd

# 初始化 Session State 來儲存數據 (將總額改為交易清單 Log)
if 'inventory_logs' not in st.session_state:
    # 每個商品編號 (0-99) 對應一個空的交易清單 []
    st.session_state.inventory_logs = {i: [] for i in range(100)}

def add_transaction(item_number, amount):
    """將交易金額加入指定的商品的交易清單 (Log) 中。"""
    try:
        if amount is None:
            st.warning("請輸入交易金額。")
            return
            
        # 將金額直接加入該商品的交易清單
        st.session_state.inventory_logs[item_number].append(amount)
        
        # 顯示成功或修正的提示
        if amount >= 0:
            st.success(f"紀錄新增成功: 數字 {item_number}, 交易金額 +{amount:.0f}")
        else:
            st.info(f"紀錄修正/刪除: 數字 {item_number}, 交易金額 {amount:.0f} (已扣除)")

    except KeyError:
        st.error(f"數字 {item_number} 超出範圍 (0-99)。")
    except TypeError:
        st.error("金額輸入錯誤，請輸入有效的數字。")

def display_totals_table():
    """顯示所有商品的交易明細 Log 和總額。"""
    
    # 建立一個列表來儲存要顯示的數據
    display_data = []
    
    # 遍歷所有商品的交易記錄
    for item_number, logs in st.session_state.inventory_logs.items():
        if not logs:
            continue # 跳過沒有交易記錄的商品
            
        # 1. 計算總金額
        total_amount = sum(logs)
        
        # 2. 格式化交易明細 (將 [50, 50, -25, 100] 轉為 "50 + 50 - 25 + 100")
        log_str = ""
        for i, val in enumerate(logs):
            if i == 0:
                # 第一筆記錄：如果是負數，前面不需要 + 號
                log_str += f"{val:.0f}"
            elif val >= 0:
                # 正數：前面加 + 號
                log_str += f" + {val:.0f}"
            else:
                # 負數：前面加空格和 - 號
                log_str += f" {val:.0f}" # .0f 會自動包含負號
        
        # ***修正點 2：移除「商品」二字，只保留數字***
        full_process_str = f"{item_number}: {log_str} = ${total_amount:,.0f}"
        
        # 儲存到顯示列表中
        display_data.append({
            "交易明細 (Log)": full_process_str
        })

    if not display_data:
        st.info("目前尚無任何交易記錄。")
        return

    # ***修正點 1：更改標題***
    st.subheader("📊 交易明細與最終成果")
    
    # 逐行顯示明細
    for row in display_data:
        st.markdown(f"**{row['交易明細 (Log)']}**")
    
    # 顯示所有商品總和 (這部分保留)
    all_items_total = sum(sum(logs) for logs in st.session_state.inventory_logs.values())
    st.markdown("---")
    st.markdown(f"**💰 所有數字總收入 (所有數字 0-99):** **${all_items_total:,.0f}**")


# --- Streamlit 應用程式介面 (UI) ---

st.title("數字金額整合計算器 (Web App)")
st.caption("輸入數字編號 (0-99) 和交易金額，系統會自動儲存每筆明細。")

# 1. 輸入區域 (Input Form)
with st.form("transaction_form", clear_on_submit=True):
    # 商品編號維持整數輸入 (維持預設 value=0 較穩定)
    item_number = st.number_input("輸入數字編號 (0 - 99):", min_value=0, max_value=99, step=1, value=0)
    
    # 將 value 設為 None，讓輸入框預設為空
    amount = st.number_input("輸入交易金額 (新增:正數, 修正/刪除:負數):", step=1, value=None)
    
    submitted = st.form_submit_button("確認提交 (Submit)")
    
    if submitted:
        # 加入對 None 的檢查
        if amount is None:
            st.warning("請輸入交易金額。")
        elif amount == 0:
            st.warning("請輸入非零金額。")
        else:
            add_transaction(int(item_number), amount)

# 2. 顯示結果 (Output)
st.markdown("---") 
display_totals_table()

st.sidebar.markdown("""
### 💡 功能說明
* **新增交易:** 輸入**正數**金額。
* **修正/刪除:** 輸入**負數**金額，即可從總額中扣除 (該筆記錄也會出現在明細中)。
* **數據儲存:** 數據會在瀏覽器 Session 中，關閉瀏覽器後會重置。
""")
