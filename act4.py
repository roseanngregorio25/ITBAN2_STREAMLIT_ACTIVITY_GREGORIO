import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# --------------------------
# Database Configuration
# --------------------------
DB_USER = 'root'
DB_PASSWORD = None  # or your actual password as a string
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'university'

@st.cache_resource
def get_connection():
    if DB_PASSWORD is None:
        connection_url = f"mysql+pymysql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        connection_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(connection_url)

engine = get_connection()

# --------------------------
# Authentication
# --------------------------
st.sidebar.header("🔐 Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

def authenticate(user, pwd):
    return user == "admin" and pwd == "school123"

if authenticate(username, password):
    st.success(f"Welcome, {username} 👋")
    st.title("🏫 School Management Dashboard")

    # --------------------------
    # Table Selector
    # --------------------------
    table = st.selectbox("Select Table", ["faculty", "subjects"])

    # --------------------------
    # Table Viewer with Filter
    # --------------------------
    st.subheader("📄 Table Viewer")
    filter_query = st.text_input("Optional SQL Filter (e.g., department = 'Math')")

    view_query = f"SELECT * FROM {table}"
    if filter_query.strip():
        view_query += f" WHERE {filter_query}"

    with engine.connect() as conn:
        df = pd.read_sql(text(view_query), conn)
    st.dataframe(df)

    # --------------------------
    # Insert New Record
    # --------------------------
    st.subheader(f"➕ Add New Record to `{table}`")
    with st.form(key="insert_form"):
        with engine.connect() as conn:

            if table == "faculty":
                full_name = st.text_input("Full Name")
                department = st.text_input("Department")
                email = st.text_input("Email")
                contact = st.text_input("Contact Number")
                submit = st.form_submit_button("Insert Faculty")
                if submit:
                    conn.execute(text("""
                        INSERT INTO faculty (full_name, department, email, contact)
                        VALUES (:name, :dept, :email, :contact)
                    """), {"name": full_name, "dept": department, "email": email, "contact": contact})
                    conn.commit()
                    st.success("✅ Faculty record inserted!")

            elif table == "subjects":
                subject_name = st.text_input("Subject Name")
                subject_code = st.text_input("Subject Code")
                submit = st.form_submit_button("Insert Subject")
                if submit:
                    conn.execute(text("""
                        INSERT INTO subjects (subject_name, subject_code)
                        VALUES (:name, :code)
                    """), {"name": subject_name, "code": subject_code})
                    conn.commit()
                    st.success("✅ Subject added!")

else:
    st.warning("🔐 Please log in with valid credentials.")
