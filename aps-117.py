import streamlit as st
import pandas as pd
import numpy as np

def load_data(uploaded_file):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    return None

def apply_interest_rate_shocks(df, shocks):
    results = {}
    for shock in shocks:
        df["Shocked_Rate"] = df["Original_Rate"] + shock
        df["EVE_Impact"] = df["Balance"] * (df["Shocked_Rate"] - df["Original_Rate"])
        results[f"Shock {shock}bps"] = df["EVE_Impact"].sum()
    return results

st.title("APS 117 Interest Rate Risk Reporting")

uploaded_file = st.file_uploader("Upload Balance Sheet Data (CSV)", type=["csv"])

shocks = st.multiselect("Select Interest Rate Shocks (bps)", options=[-200, -100, 0, 100, 200], default=[-100, 0, 100])

data = load_data(uploaded_file)

if data is not None:
    st.write("Uploaded Data:")
    st.dataframe(data.head())
    
    results = apply_interest_rate_shocks(data, shocks)
    st.write("EVE Sensitivity Results:")
    st.write(results)
    
    st.download_button("Download Results", pd.DataFrame.from_dict(results, orient='index').to_csv(), "EVE_Sensitivity.csv", "text/csv")
