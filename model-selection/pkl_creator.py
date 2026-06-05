import pandas as pd
import numpy as np
import pickle
import os

# ── Load data ──
df = pd.read_csv(r"C:\Users\admin\Desktop\capstone project\model-selection\gurgaon_properties_missing_value_imputation.csv")
print("Data loaded ✅ Shape:", df.shape)

# ── Create luxury_category from luxury_score ──
def assign_luxury(score):
    if score <= 50:
        return 'Low'
    elif score <= 100:
        return 'Medium'
    else:
        return 'High'

df['luxury_category'] = df['luxury_score'].apply(assign_luxury)
print("luxury_category created ✅")
print(df['luxury_category'].value_counts())

# ── Create floor_category from floorNum ──
def assign_floor(floor):
    if floor <= 3:
        return 'Low Floor'
    elif floor <= 10:
        return 'Mid Floor'
    else:
        return 'High Floor'

df['floor_category'] = df['floorNum'].apply(assign_floor)
print("floor_category created ✅")
print(df['floor_category'].value_counts())

# ── Drop luxury_score (no longer needed) ──
df = df.drop(columns=['luxury_score'])

# ── Verify final columns ──
print("\nFinal columns:", df.columns.tolist())
print("Final shape:", df.shape)

# ── Save df.pkl ──
save_path = r"C:\Users\admin\Desktop\capstone project\price-prediction\pages\df.pkl"
with open(save_path, "wb") as f:
    pickle.dump(df, f)

if os.path.exists(save_path):
    print("\ndf.pkl saved successfully ✅")
    print("Location:", save_path)
else:
    print("❌ File not saved — check the path")