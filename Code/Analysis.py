import pandas as pd

def quick_analysis(cleaned:pd.DataFrame, metadata:pd.DataFrame):
    #Compute mean NDVI before and after sowing for each crop_type
    results = []
    for crop, group in metadata.groupby("crop_type"):
        parcels =  group['parcel_id'].unique()
        subset = cleaned[(cleaned['parcel_id'].isin(parcels)) & (cleaned['sensor_status'] == "OK")]

        for _,row in group.iterrows():
            sow_date = row['sowing_date']
            parcel_id = row['parcel_id']
            parcel_data = subset[subset['parcel_id'] == parcel_id]

            before = parcel_data[(parcel_data['date'] < sow_date) & (parcel_data['date'] >= sow_date - pd.Timedelta(days=30))]
            after = parcel_data[(parcel_data['date'] > sow_date) & (parcel_data['date'] <= sow_date + pd.Timedelta(days=30))]

            results.append({
                "crop_type": row['crop_type'],
                "parcel_id": parcel_id,
                "mean_ndvi_before": before['ndvi_value'].mean(),
                "mean_ndvi_after": after['ndvi_value'].mean()
            })

    df_results = pd.DataFrame(results)

    summary = df_results.groupby("crop_type").agg({
        "mean_ndvi_before": "mean",
        "mean_ndvi_after": "mean",
        "parcel_id": "count"
    }).reset_index().rename(columns={"parcel_id": "n_parcels"})

    return summary

cleaned = pd.read_csv("output/cleaned_readings.csv")
metadata = pd.read_csv("output/cleaned_metadata.csv")

cleaned['date'] = pd.to_datetime(cleaned['date'])
metadata['sowing_date'] = pd.to_datetime(metadata['sowing_date'])

if __name__ == "__main__":
    summary = quick_analysis(cleaned, metadata)
    print(summary)

