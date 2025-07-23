"""
verify_datasets.py - Verify all required CSV data files are present and valid
Run this before ETL to ensure your dataset folder is properly configured.
"""

import pandas as pd

print("=" * 60)
print("HEALTHCARE COST NAVIGATOR - DATA VERIFICATION")
print("=" * 60)

# 1. TEST HOSPITAL PRICING DATA
print("\n1️⃣ HOSPITAL PRICING DATA (MUP_INP_RY24_P03_V10_DY22_PrvSvc.csv)")
print("   Contains: Medicare inpatient charges by hospital and procedure")
print("-" * 60)

try:
    pricing_df = pd.read_csv('dataset/MUP_INP_RY24_P03_V10_DY22_PrvSvc.csv', encoding='latin-1')
    print(f"✅ Loaded successfully!")
    print(f"   - Total procedure records: {len(pricing_df):,}")
    print(f"   - Unique hospitals: {pricing_df['Rndrng_Prvdr_CCN'].nunique():,}")
    print(f"   - Unique procedures (DRGs): {pricing_df['DRG_Cd'].nunique()}")
    print(f"   - States covered: {', '.join(sorted(pricing_df['Rndrng_Prvdr_State_Abrvtn'].unique()))}")
    
    # Store for cross-checking
    hospital_ids = set(pricing_df['Rndrng_Prvdr_CCN'].astype(str))
    hospital_zips = set(pricing_df['Rndrng_Prvdr_Zip5'].astype(str))
except Exception as e:
    print(f"❌ Error: {e}")
    hospital_ids = set()
    hospital_zips = set()

# 2. TEST CMS RATINGS DATA
print("\n2️⃣ HOSPITAL RATINGS DATA (Hospital_General_Information.csv)")
print("   Contains: Official CMS star ratings (1-5 scale)")
print("-" * 60)

try:
    ratings_df = pd.read_csv('dataset/Hospital_General_Information.csv', encoding='utf-8')
    cms_ids = set(ratings_df['Facility ID'].astype(str))
    
    print(f"✅ Loaded successfully!")
    print(f"   - Total CMS hospitals: {len(ratings_df):,}")
    
    # Show rating distribution
    rating_counts = ratings_df['Hospital overall rating'].value_counts()
    print(f"   - With star ratings: {rating_counts[rating_counts.index != 'Not Available'].sum():,}")
    print(f"   - Without ratings: {rating_counts.get('Not Available', 0):,}")
    
    # Cross-reference with our hospitals
    matches = hospital_ids.intersection(cms_ids)
    print(f"\n   📊 Cross-reference with pricing data:")
    print(f"   - Our hospitals with CMS ratings: {len(matches):,} out of {len(hospital_ids):,} ({len(matches)/len(hospital_ids)*100:.1f}%)")
    print(f"   - Our hospitals needing mock ratings: {len(hospital_ids) - len(matches):,}")
except Exception as e:
    print(f"❌ Error: {e}")

# 3. TEST ZIP CODE DATA
print("\n3️⃣ ZIP CODE COORDINATES (uszips.csv)")
print("   Contains: US ZIP codes with lat/lon for distance calculations")
print("-" * 60)

try:
    # Try different encodings
    for encoding in ['latin-1', 'utf-8', 'cp1252']:
        try:
            zip_df = pd.read_csv('dataset/uszips.csv', encoding=encoding)
            print(f"✅ Loaded successfully with {encoding} encoding!")
            break
        except:
            continue
    
    all_zips = set(zip_df['zip'].astype(str))
    
    print(f"   - Total US ZIP codes: {len(zip_df):,}")
    print(f"   - NY ZIP codes available: {len(zip_df[zip_df['state_id'] == 'NY']):,}")
    
    # Cross-reference with hospital ZIPs
    if hospital_zips:
        geocodable = hospital_zips.intersection(all_zips)
        print(f"\n   📊 Cross-reference with hospital locations:")
        print(f"   - Hospital ZIPs we can geocode: {len(geocodable):,} out of {len(hospital_zips):,} ({len(geocodable)/len(hospital_zips)*100:.1f}%)")
        print(f"   - Hospital ZIPs missing coordinates: {len(hospital_zips) - len(geocodable):,}")
        
        # Show a missing example if any
        missing = hospital_zips - all_zips
        if missing:
            print(f"   - Example missing ZIP: {list(missing)[0]}")
except Exception as e:
    print(f"❌ Error: {e}")

# SUMMARY
print("\n" + "=" * 60)
print("📊 DATA VERIFICATION SUMMARY")
print("=" * 60)
print(f"\n✅ Ready for ETL if all 3 datasets loaded successfully")
print(f"📝 Note: {len(hospital_ids) - len(matches):,} hospitals will receive mock ratings (4-9 scale)")