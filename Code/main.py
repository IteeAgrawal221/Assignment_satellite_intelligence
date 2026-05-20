import pandas as pd

def load_data(metadata_path:str, reading_path:str):
    # Load parcel reading and metadata CSVs
    metadata = pd.read_csv(metadata_path)
    readings = pd.read_csv(reading_path)
    return metadata, readings

def clean_data(readings:pd.DataFrame, valid_values:set):
    # --- Date cleaning --- Convert to datetime (handles mixed formats)
    readings['date'] = pd.to_datetime(readings['date'], errors='coerce', dayfirst=True)
    # Format back to DD-MM-YYYY string
    readings['date'] = readings['date'].dt.strftime("%d-%m-%Y")

    # Keep only NDVI values within [-1, 1]
    readings = readings[(readings['ndvi_value'] > -1) & (readings['ndvi_value'] < 1)]

    # --- Sensor status cleaning ---
    readings['sensor_status'] = (
        readings['sensor_status']
        .astype(str)      # convert to string
        .str.strip()      # remove leading/trailing spaces
        .str.upper()      # normalize case
    )

    readings['sensor_status'] = readings['sensor_status'].replace({
        'ERROR': 'Error',
        'OK': 'OK',
        'NA': 'NA',
        'NAN': 'NA'
    })

    # Handle blanks and fill NaN
    readings['sensor_status'] = readings['sensor_status'].replace(['', 'NONE'], 'NA')
    readings['sensor_status'] = readings['sensor_status'].fillna('NA')

    #Drop rows with missng parcel_id
    readings =  readings.dropna(subset=['parcel_id'])
    
    #Keep only parcel_ids that exist in metadata
    readings = readings[readings['parcel_id'].isin(valid_values)]
    return readings  

def join_data(readings:pd.DataFrame, metdata:pd.DataFrame):
    #Merge clean readings with metadata
    cleaned = readings.merge(metadata, on="parcel_id",how="left")
    return cleaned

def save_cleaned_data(cleaned:pd.DataFrame, output_path:str):
    #Save cleaned dataset
    cleaned.to_csv(output_path, index=False)

if __name__ == "__main__":
    metadata, readings = load_data("input/parcel_metadata.csv", "input/parcel_readings.csv")
    valid_values = set(metadata['parcel_id'])
    readings = clean_data(readings, valid_values)

    cleaned = join_data(readings, metadata)
    print(cleaned)

    save_cleaned_data(cleaned, "output/cleaned_parcel_timeseries.csv")
    save_cleaned_data(readings, "output/cleaned_readings.csv")           # cleaned readings only
    save_cleaned_data(metadata, "output/cleaned_metadata.csv")           # metadata only
 