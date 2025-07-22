import pandas as pd

# Read with correct encoding
df = pd.read_csv('MUP_INP_RY24_P03_V10_DY22_PrvSvc.csv', encoding='latin-1')

print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")

# Check unique providers
unique_providers = df['Rndrng_Prvdr_CCN'].nunique()
print(f"\nUnique hospitals: {unique_providers}")

# Check unique DRGs
unique_drgs = df['DRG_Cd'].nunique()
print(f"Unique DRG codes: {unique_drgs}")

# Sample data
print("\nSample provider:")
print(df[['Rndrng_Prvdr_CCN', 'Rndrng_Prvdr_Org_Name', 'Rndrng_Prvdr_City', 'Rndrng_Prvdr_Zip5']].head(2))

print("\nSample procedures:")
print(df[['DRG_Cd', 'DRG_Desc', 'Avg_Submtd_Cvrd_Chrg']].head(2))

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())