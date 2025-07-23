import pandas as pd

# Load both datasets
cms_ratings = pd.read_csv('Hospital_General_Information.csv', encoding='utf-8')
procedures_data = pd.read_csv('MUP_INP_RY24_P03_V10_DY22_PrvSvc.csv', encoding='latin-1')

# Get unique provider IDs from our data
our_provider_ids = procedures_data['Rndrng_Prvdr_CCN'].unique()
print(f"Our unique provider IDs: {len(our_provider_ids)}")

# Convert Facility ID to string for comparison (remove leading zeros)
cms_ratings['Facility ID'] = cms_ratings['Facility ID'].astype(str)
our_provider_ids = [str(id) for id in our_provider_ids]

# Check overlap
matching_ids = set(our_provider_ids).intersection(set(cms_ratings['Facility ID']))
print(f"Matching provider IDs: {len(matching_ids)}")

# Check NY matches specifically
ny_cms = cms_ratings[cms_ratings['State'] == 'NY']
ny_matches = set(our_provider_ids).intersection(set(ny_cms['Facility ID']))
print(f"Matching NY providers: {len(ny_matches)}")

# Show sample matches
if matching_ids:
    sample_id = list(matching_ids)[0]
    print(f"\nSample match - Provider ID: {sample_id}")
    print("CMS data:")
    print(cms_ratings[cms_ratings['Facility ID'] == sample_id][['Facility Name', 'Hospital overall rating']].iloc[0])
    print("\nOur data:")
    print(procedures_data[procedures_data['Rndrng_Prvdr_CCN'] == int(sample_id)][['Rndrng_Prvdr_Org_Name']].iloc[0])