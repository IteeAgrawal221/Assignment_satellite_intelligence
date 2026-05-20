# Assignment_satellite_intelligence
Data Engineer Assignment – Satellite Intelligence  - Carnot Technologies

	1. Data Quality Audit
			§ NDVI value out-of-range :- 
				□ Issue: NDVI should be between -1 and 1. Values like 1.832, 1.817, 1.743, 1.665, -1.677, -1.163, -1.492, -1.024 are invalid.
				□ Frequency: ~40+ occurrences across parcels.
				□ Impact: Critical — invalid NDVI breaks vegetation analysis and trend modelling.
				□ Solution :- drop and strictly before ingestion.
				
			§ Sensor_status inconsistency:-
				□ Issue: Sensor status values are inconsistent (OK, ok, Error, error, NaN, blank, NA).
				□ Frequency: Hundreds of entries show inconsistent casing or non-standard flags.
				□ Impact: High — makes filtering unreliable and can misclassify sensor health.
				□ Solution :- Fixed the values in consistent format.
				
			§ Date format inconsistency:-
				□ Issue: Multiple formats used (20-Jan-2026, 19-Mar-2026).
				□ Frequency: Widespread — almost every parcel has mixed formats.
				□ Impact: Medium — parsing errors in pipelines, time-series misalignment.
				□ Solution :- convert all dates  to DD-MM-YYYY format 
				
			§ Parcel_id missing:
				□ Issue: In the readings dataset, parcel IDs like PARCEL_098, PARCEL_099 appear, but they are missing in metadata. Conversely, metadata has PARCEL_050, PARCEL_051, PARCEL_052 which do not appear in readings.
				□ Frequency: Multiple mismatches (at least 5–7 IDs).
				□ Impact: Critical — breaks relational joins between datasets, leading to orphan records.
				□ Solution :-  Enforce referential integrity between metadata and readings (every parcel_id must exist in both).
		
	2. Clean Pipeline
	Approach
		• Load both CSVs with Pandas.
		• Apply cleaning rules:
			○ Drop invalid NDVI.
			○ Normalize sensor_status.
			○ Standardize dates.
			○ Exclude parcel_id mismatches.
		• Join metadata + readings on parcel_id.
		• Save output as cleaned_parcel_timeseries.csv.
	
	3. Data Analysis
		This summary shows that NDVI values generally increase after sowing across all crops. Soybean and wheat start with relatively low vegetation health before sowing but improve noticeably afterward, while sugarcane shows the highest overall NDVI and the largest sample size, suggesting stronger and more consistent crop growth.
		
	4. Production Readiness Reflection
	If scaled 100×:
		1. Switch to Spark for distributed processing.
		2. Add schema validation.
		3. Store cleaned data in Parquet for efficiency.
	Monitoring
		• NDVI out-of-range counts.
		• Sensor status distribution.
		• Missing data rates.
		• Join mismatches.
	Likely Silent Break
		• Date parsing — new formats creeping in.
		• Sensor status drift — new unexpected values.
Parcel ID mismatches — new parcels not in metadata.
