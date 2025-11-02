這是一個很好的使用者體驗優化點！

您希望在輸入金額時，輸入框內預設的 0 不要擋住您的輸入，這樣您就不必每次手動刪除它。

在 Streamlit 中，我們可以在 st.number_input 中使用 value=None 或一個空值來實現，讓輸入框一開始是空的。不過，Streamlit 的 st.number_input 對 value 的處理比較嚴格，通常需要一個數字。

✅ 解決方案：設置預設為空值（或在輸入時覆蓋）
我們可以使用 placeholder 參數，但更常見且兼容性更好的方法是將預設值設定為 None，但這可能與舊版 Streamlit 衝突。

針對您目前的程式碼，最穩定且最簡單的修正方式是讓程式碼在讀取數值時，能夠正確處理 None 的情況，並將輸入框的預設值設定為 None。

請您再次完全替換您的 app.py 檔案內容，使用下面這段更新後的程式碼。

💻 完整且已修正的 Streamlit 程式碼 (金額輸入框預設為空)
我將在 add_transaction 函式中加入對輸入值是否為 None 的檢查，並將 st.number_input 的 value 設為 None，讓輸入框預設為空。

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
        # 這裡會接收 None 或數字
        if amount is None:
            st.warning("請輸入交易金額。")
            return
            
        # 將金額直接加入該商品的交易清單
        st.session_state.inventory_logs[item_number].append(amount)
        
        # 顯示成功或修正的提示
        if amount >= 0:
            st.success(f"紀錄新增成功: 商品 {item_number}, 交易金額 +{amount:.0f}")
        else:
            st.info(f"紀錄修正/刪除: 商品 {item_number}, 交易金額 {amount:.0f} (已扣除)")

    except KeyError:
        st.error(f"商品編號 {item_number} 超出範圍 (0-99)。")
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
        
        # 儲存到顯示列表中
        display_data.append({
            "商品編號": item_number,
            "交易明細 (Log)": log_str,
            "最終總額": total_amount
        })

    if not display_data:
        st.info("目前尚無任何交易記錄。")
        return

    # 建立 Pandas DataFrame
    df = pd.DataFrame(display_data)
    df = df.sort_values(by="商品編號")
    
    # 格式化金額顯示
    df["最終總額"] = df["最終總額"].map('${:,.0f}'.format)
    
    st.subheader("📊 商品交易明細與總額")
    st.dataframe(df) 
    
    # 顯示所有商品總和
    all_items_total = sum(sum(logs) for logs in st.session_state.inventory_logs.values())
    st.markdown(f"**💰 所有商品總收入:** **${all_items_total:,.0f}**")


# --- Streamlit 應用程式介面 (UI) ---

st.title("商品金額整合計算器 (Web App)")
st.caption("輸入商品編號 (0-99) 和交易金額，系統會自動儲存每筆明細。")

# 1. 輸入區域 (Input Form)
with st.form("transaction_form", clear_on_submit=True):
    # 商品編號維持整數輸入 (維持預設 value=0 較穩定)
    item_number = st.number_input("輸入商品編號 (0 - 99):", min_value=0, max_value=99, step=1, value=0)
    
    # ***關鍵修改處：將 value 設為 None***
    # 這樣輸入框在載入時就是空的，但可能會在舊版 Streamlit 產生警告。
    # 如果出現錯誤，請將 value=None 移除，使用預設值 0。
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
