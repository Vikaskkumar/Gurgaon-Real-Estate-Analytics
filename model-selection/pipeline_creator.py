import pandas as pd
import numpy as np
import pickle
import os
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
import category_encoders as ce

# ── Load data ──
df = pd.read_csv(r"C:\Users\admin\Desktop\capstone project\model-selection\gurgaon_properties_missing_value_imputation.csv")
print("Data loaded ✅ Shape:", df.shape)

# ── Feature Engineering ──
df['luxury_category'] = df['luxury_score'].apply(
    lambda x: 'Low' if x <= 50 else ('Medium' if x <= 100 else 'High')
)
df['floor_category'] = df['floorNum'].apply(
    lambda x: 'Low Floor' if x <= 3 else ('Mid Floor' if x <= 10 else 'High Floor')
)
df = df.drop(columns=['luxury_score'])
print("Feature engineering done ✅")

# ── Define X and y ──
X = df.drop(columns=['price'])
y = df['price']
y_transformed = np.log1p(y)

print("X shape:", X.shape)
print("X columns:", X.columns.tolist())

# ── Define Preprocessor ──
num_cols = ['bedRoom', 'bathroom', 'built_up_area', 'servant room', 
            'store room', 'floorNum', 'study room', 'pooja room', 'others']

cat_cols = ['property_type', 'balcony', 'furnishing_type', 
            'luxury_category', 'floor_category']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_cols),
        ('cat', OrdinalEncoder(), cat_cols),
        ('cat1', OneHotEncoder(drop='first', sparse_output=False), ['agePossession']),
        ('target_enc', ce.TargetEncoder(), ['sector'])
    ],
    remainder='drop'
)

# ── Define Pipeline ──
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=500, random_state=42))
])

# ── Fit Pipeline ──
print("Training pipeline... ⏳")
pipeline.fit(X, y_transformed)
print("Pipeline trained ✅")

# ── Save pipeline.pkl ──
save_path = r"C:\Users\admin\Desktop\capstone project\price-prediction\pages\pipeline.pkl"
with open(save_path, "wb") as f:
    pickle.dump(pipeline, f)

if os.path.exists(save_path):
    print("pipeline.pkl saved successfully ✅")
    print("Location:", save_path)
else:
    print("❌ File not saved — check the path")

# ── Quick test ──
sample = X.iloc[[0]]
predicted = np.expm1(pipeline.predict(sample))[0]
print(f"\nSample prediction: ₹ {round(predicted, 2)} Lakhs ✅")