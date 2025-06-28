import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_analysis(df):
    st.subheader("📊 分析結果")

    st.write("原始資料：")
    st.dataframe(df)

    st.subheader("統計資訊")
    st.write(df['score'].describe())
    st.metric("平均分數", f"{df['score'].mean():.2f}")
    st.metric("最高分", df['score'].max())
    st.metric("最低分", df['score'].min())

    st.subheader("高分學生（≥ 80）")
    st.dataframe(df[df['score'] >= 80])

    st.subheader("最高分學生")
    st.write(df.loc[df['score'].idxmax()])

    df['passed'] = np.where(df['score'] >= 60, 'Yes', 'No')
    df_sorted = df.sort_values(by='score', ascending=False)

    st.subheader("排序後資料")
    st.dataframe(df_sorted)

    csv = df_sorted.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ 下載 CSV", csv, "student_scores.csv", "text/csv")

    st.subheader("分數長條圖")
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(df_sorted['name'], df_sorted['score'], color='skyblue')
    ax.set_title('學生分數分佈圖')
    ax.set_ylabel('分數')
    ax.set_ylim(0, df_sorted['score'].max() * 1.1)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height, int(height),
                ha='center', va='bottom')
    st.pyplot(fig)

def main():
    st.title("🧪 Streamlit Pandas 分析介面")

    option = st.radio("選擇資料來源：", ["使用預設資料", "上傳 CSV 檔", "手動輸入資料"])

    if option == "使用預設資料":
        data = {
            'name': ['Jammy', 'John', 'Alice', 'Peter', 'Kate'],
            'score': [66, 76, 86, 58, 92]
        }
        df = pd.DataFrame(data)
        run_analysis(df)

    elif option == "上傳 CSV 檔":
        uploaded_file = st.file_uploader("請上傳包含 name 和 score 欄位的檔案 (CSV 或 XLSX)", type=["csv", "xlsx"])
        if uploaded_file:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("不支援的檔案格式")

        if 'name' in df.columns and 'score' in df.columns:
            run_analysis(df)
        else:
            st.error("請確保檔案中包含 'name' 和 'score' 欄位。")

    elif option == "手動輸入資料":
        st.info("請逐筆輸入學生資料後按下新增，再按分析。")
        if "records" not in st.session_state:
            st.session_state.records = []

        with st.form(key="input_form"):
            name = st.text_input("學生姓名")
            score = st.number_input("分數", min_value=0, max_value=100, step=1)
            submitted = st.form_submit_button("新增")
            if submitted and name:
                st.session_state.records.append({"name": name, "score": score})

        if st.session_state.records:
            df = pd.DataFrame(st.session_state.records)
            st.write("目前輸入的資料：")
            st.dataframe(df)
            if st.button("開始分析"):
                run_analysis(df)

if __name__ == "__main__":
    main()
