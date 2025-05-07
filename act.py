import streamlit as st

# App title and header
st.title("📱 Welcome to the Streamlit App")
st.header("🔐 User Information Form")

# Input fields
with st.form("user_form"):
    email = st.text_input("📧 Enter your email address")
    pin = st.text_input("🔢 Enter your 4-digit PIN", type="password")
    submitted = st.form_submit_button("Submit")

# Display results after form submission
if submitted:
    st.success("✅ Submission received!")
    st.write("You entered:")
    st.write(f"📧 Email: {email}")
    st.write(f"🔒 PIN: {'*' * len(pin)} (hidden for privacy)")
