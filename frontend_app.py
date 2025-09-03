import streamlit as st
import pandas as pd
from datetime import timedelta

# Title
st.title("🔌 Outages and Complaints Matcher")

# File Uploaders
uploaded_outages = st.file_uploader("Upload Outages CSV File", type=["csv"])
uploaded_complaints = st.file_uploader("Upload Complaints CSV File",
                                       type=["csv"])

# Process the files once both are uploaded
if uploaded_outages and uploaded_complaints:
    outages = pd.read_csv(uploaded_outages)
    complaints = pd.read_csv(uploaded_complaints)

    # Convert date columns to datetime
    outages['time_of_outage'] = pd.to_datetime(outages['time_of_outage'],
                                               infer_datetime_format=True,
                                               errors='coerce')
    complaints['time_of_complaint'] = pd.to_datetime(
        complaints['time_of_complaint'],
        infer_datetime_format=True,
        errors='coerce')

    # Drop rows with invalid dates
    outages = outages.dropna(subset=['time_of_outage'])
    complaints = complaints.dropna(subset=['time_of_complaint'])

    # Merge datasets
    merged_df = outages.merge(complaints,
                              on='site',
                              suffixes=('_outage', '_complaint'))

    # Filter rows within 4 hours
    filtered_df = merged_df[(abs(merged_df['time_of_outage'] -
                                 merged_df['time_of_complaint'])
                             <= timedelta(hours=4))]

    results_df = filtered_df[['site', 'time_of_outage', 'time_of_complaint']]

    # Show the results
    st.success(f"Found {len(results_df)} matching records!")
    st.dataframe(results_df)

    # Provide download button
    csv = results_df.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Download Matched Results CSV",
                       data=csv,
                       file_name="matched_outages_complaints.csv",
                       mime='text/csv')

else:
    st.info("Please upload both Outages and Complaints CSV files to proceed.")
