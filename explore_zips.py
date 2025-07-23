import pandas as pd

# Try different encodings
encodings = ['latin-1', 'iso-8859-1', 'cp1252', 'utf-8-sig']

for encoding in encodings:
    try:
        print(f"Trying encoding: {encoding}")
        df = pd.read_csv('uszips.csv', encoding=encoding)
        print(f"✅ Success with {encoding}!")
        break
    except Exception as e:
        print(f"❌ Failed with {encoding}")
        continue

print(f"\nTotal ZIP codes: {len(df)}")
print(f"Columns: {list(df.columns)}")

# Look at NY ZIP codes
ny_zips = df[df['state_id'] == 'NY']
print(f"\nNY ZIP codes: {len(ny_zips)}")

# Sample data
print("\nSample NY ZIPs:")
print(ny_zips[['zip', 'lat', 'lng', 'city']].head())