import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Academic Intelligence System", layout="wide")

st.title("⚡ Academic Intelligence System")

# =========================
# LOAD DATA
# =========================
DATA_FILE = "data/students.csv"

if "df" not in st.session_state:
    if os.path.exists(DATA_FILE):
        st.session_state.df = pd.read_csv(DATA_FILE)
    else:
        st.session_state.df = pd.DataFrame(columns=["Nombre", "Puntos"])

df = st.session_state.df

# =========================
# MENU
# =========================
menu = st.sidebar.radio("Menu", [
    "Dashboard",
    "Student Intelligence",
    "Alerts Center",
    "Reports"
])

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.header("Overview")

    col1, col2 = st.columns(2)

    col1.metric("Students", df["Nombre"].nunique())
    col2.metric("Total Points", df["Puntos"].sum())

    st.dataframe(df)

# =========================
# STUDENT INTELLIGENCE
# =========================
elif menu == "Student Intelligence":

    st.header("Student Intelligence")

    students = df["Nombre"].unique()

    col1, col2 = st.columns(2)

    student = col1.selectbox("Select student", students)

    puntos = col2.number_input("Points (+ / -)", step=1)

    if st.button("Apply Points ⚡"):

        idx = df[df["Nombre"] == student].index

        if len(idx) > 0:
            st.session_state.df.loc[idx, "Puntos"] += puntos
        else:
            new_row = pd.DataFrame([[student, puntos]], columns=["Nombre", "Puntos"])
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)

        st.session_state.df.to_csv(DATA_FILE, index=False)

        st.success(f"{puntos} points applied to {student}")

# =========================
# ALERTS CENTER
# =========================
elif menu == "Alerts Center":

    st.header("🚨 Alerts Center")

    for i, row in df.iterrows():
        if row["Puntos"] < 0:
            st.error(f"{row['Nombre']} → Needs attention")

# =========================
# REPORTS
# =========================
elif menu == "Reports":

    st.header("📊 Reports")

    st.dataframe(df)

    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        "report.csv",
        "text/csv"
    )
