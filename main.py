import pandas as pd
from datetime import timedelta

outages = pd.read_csv('outages.csv')
complaints = pd.read_csv('complaints.csv')

outages['time_of_outage'] = pd.to_datetime(outages['time_of_outage'],
                                           infer_datetime_format=True,
                                           errors='coerce')
complaints['time_of_complaint'] = pd.to_datetime(
    complaints['time_of_complaint'],
    infer_datetime_format=True,
    errors='coerce')

outages = outages.dropna(subset=['time_of_outage'])
complaints = complaints.dropna(subset=['time_of_complaint'])

merged_df = outages.merge(complaints,
                          on='site',
                          suffixes=('_outage', '_complaint'))

filtered_df = merged_df[(abs(merged_df['time_of_outage'] -
                             merged_df['time_of_complaint'])
                         <= timedelta(hours=4))]

results_df = filtered_df[['site', 'time_of_outage', 'time_of_complaint']]

# Print and save the results
print(results_df)
results_df.to_csv('matched_outages_complaints.csv', index=False)
