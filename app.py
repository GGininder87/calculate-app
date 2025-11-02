import streamlit as st
import pandas as pd

# 初始化 Session State 來儲存數據
if 'inventory_totals' not in st.session_state:
    # 初始化：建立一個字典，用來儲存所有商品的累積金額 (0-99)
    st.session_state.inventory_totals = {i: 0.0 for i in range(100)}

def add_transaction(item_number, amount):
    """將交易金額加到指定的商品編號上，並更新狀態。"""
    try:
        # 將金額加到該商品的總額上 (內部仍用浮點數計算，確保數據精準度)
        st.session_state.inventory_totals[item_number] += amount
        
        # 顯示成功或修正的提示
        if amount >= 0:
            st.success(f"紀錄更新成功: 商品 {item_number}, 金額變動 +{amount:.0f}") # 這裡也將顯示格式改為整數
        else:
            st.info(f"紀錄修正成功: 商品 {item_number}, 金額變動 {amount:.0f} (已扣除)") # 這裡也將顯示格式改為整數

    except KeyError:
        st.error(f"商品編號 {item_number} 超出範圍 (0-99)。")
    except TypeError:
        st.error("金額輸入錯誤，請輸入有效的數字。")

def display_totals_table():
    """顯示當前所有商品的總金額表格。"""
    
    data = st.session_state.inventory_totals
    
    # 篩選掉金額為零的項目，只顯示有交易的商品
    has_sales = {k: v for k, v in data.items() if v != 0}
    
    if not has_sales:
        st.info("目前尚無任何交易記錄。")
        return

    # 建立 Pandas DataFrame
    df = pd.DataFrame(
        list(has_sales.items()),
        columns=["商品編號 (Item)", "總收入 (Total AUD/TWD)"]
    )
    df = df.sort_values(by="商品編號 (Item)")
    
    # 格式化金額顯示 (使用 .0f 確保只顯示整數)
    df["總收入 (Total AUD/TWD)"] = df["總收入 (Total AUD/TWD)"].map('${:,.0f}'.format)
    
    st.subheader("📊 當前商品總額清單")
    st.dataframe(df)
    
    # 顯示總和 (使用 .0f 確保只顯示整數)
    total_revenue = sum(data.values())
    st.markdown(f"**💰 所有商品總收入:** **${total_revenue:,.0f}**")


# --- Streamlit 應用程式介面 (UI) ---

st.title("商品金額整合計算器 (Web App)")
st.caption("輸入商品編號 (0-99) 和交易金額，系統會自動加總。")

# 1. 輸入區域 (Input Form)
with st.form("transaction_form", clear_on_submit=True):
    # 商品編號維持整數輸入
    item_number = st.number_input("輸入商品編號 (0 - 99):", min_value=0, max_value=99, step=1, value=0)
    
    # ***關鍵修改處：將 step 設為 1，強制 UI 顯示為整數***
    amount = st.number_input("輸入交易金額 (新增:正數, 修正/刪除:負數):", step=1)
    
    submitted = st.form_submit_button("確認提交 (Submit)")
    
    if submitted:
        if amount == 0:
            st.warning("請輸入非零金額。")
        else:
            add_transaction(int(item_number), amount)

# 2. 顯示結果 (Output)
st.markdown("---") # 替換 st.divider()
display_totals_table()

st.sidebar.markdown("""
### 💡 功能說明
* **新增交易:** 輸入**正數**金額。
* **修正/刪除:** 輸入**負數**金額，即可從總額中扣除。
* **數據儲存:** 數據會儲存在瀏覽器 Session 中，關閉瀏覽器後會重置。如需永久保存，未來可以擴充下載功能。
""")