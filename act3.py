import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")
st.title("🦠 COVID-19 Data Dashboard")

# Sidebar for country selection
st.sidebar.title("🌍 Country Selector")
country = st.sidebar.selectbox("Choose a country", ["USA", "Philippines", "India", "Brazil", "Germany"])

# Fetch historical data
url = f"https://disease.sh/v3/covid-19/historical/{country}?lastdays=30"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    if "timeline" in data:
        timeline = data["timeline"]
        df = pd.DataFrame({
            "Date": pd.to_datetime(list(timeline["cases"].keys())),
            "Cases": list(timeline["cases"].values()),
            "Deaths": list(timeline["deaths"].values()),
            "Recovered": list(timeline["recovered"].values()),
        })

        # Compute daily differences
        df["New Cases"] = df["Cases"].diff().fillna(0)
        df["New Deaths"] = df["Deaths"].diff().fillna(0)
        df["New Recovered"] = df["Recovered"].diff().fillna(0)

        st.subheader(f"📊 Daily Statistics for {country}")

        col1, col2, col3 = st.columns(3)
        col1.metric("New Cases (Latest)", int(df['New Cases'].iloc[-1]))
        col2.metric("New Deaths (Latest)", int(df['New Deaths'].iloc[-1]))
        col3.metric("New Recovered (Latest)", int(df['New Recovered'].iloc[-1]))

        st.line_chart(df.set_index("Date")[["New Cases", "New Deaths", "New Recovered"]])

        st.subheader("📌 Proportion of Total")
        totals = {
            "Cases": df["Cases"].iloc[-1],
            "Deaths": df["Deaths"].iloc[-1],
            "Recovered": df["Recovered"].iloc[-1],
        }
        fig, ax = plt.subplots()
        ax.pie(totals.values(), labels=totals.keys(), autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

        # Toggle for raw data
        if st.sidebar.checkbox("Show Raw Data"):
            st.subheader("🗃 Raw Data Table")
            st.dataframe(df)
    else:
        st.error("⚠️ Timeline data not found for this country.")
else:
    st.error(f"❌ API error: {response.status_code}")
