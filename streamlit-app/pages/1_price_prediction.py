import numpy as np
import streamlit as st
import pandas as pd
import os
import joblib


st.title("🏠 Gurgaon Property Price Predictor")


BASE_DIR = os.path.dirname(__file__)

data = joblib.load(os.path.join(BASE_DIR, 'df.joblib'))
pipeline = joblib.load(os.path.join(BASE_DIR, 'pipeline.joblib'))

df = pd.DataFrame(data)

st.header("Select your Input")

property_type   = st.selectbox("Property Type", ["flat", "house"])
sector          = st.selectbox("Select Sector", sorted(df['sector'].unique().tolist()))
bedroom         = float(st.selectbox("Number of Bedrooms", sorted(df['bedRoom'].unique().tolist())))
bathroom        = float(st.selectbox("Number of Bathrooms", sorted(df['bathroom'].unique().tolist())))
balcony         = st.selectbox("Number of Balconies", sorted(df['balcony'].unique().tolist()))
property_age    = st.selectbox("Property Age", sorted(df['agePossession'].unique().tolist()))
builtup_area    = float(st.number_input("Built Up Area (sq ft)", min_value=0.0))
servant_room    = float(st.selectbox("Servant Room", [0, 1]))
store_room      = float(st.selectbox("Store Room", [0, 1]))
furnishing_type = st.selectbox("Furnishing Type", sorted(df['furnishing_type'].unique().tolist()))
luxury_category = st.selectbox("Luxury Category", sorted(df['luxury_category'].unique().tolist()))
floor_category  = st.selectbox("Floor Category", sorted(df['floor_category'].unique().tolist()))

# ── Missing fields added ──
floor_num       = float(st.number_input("Floor Number", min_value=0.0, max_value=50.0))
study_room      = float(st.selectbox("Study Room", [0, 1]))
pooja_room      = float(st.selectbox("Pooja Room", [0, 1]))
others          = float(st.selectbox("Others Room", [0, 1]))

if st.button("Predict"):
    input_data = [[property_type, sector, bedroom, bathroom, balcony,
                   property_age, builtup_area, servant_room, store_room,
                   furnishing_type, luxury_category, floor_category,
                   floor_num, study_room, pooja_room, others]]  # 👈 added

    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category',
               'floorNum', 'study room', 'pooja room', 'others']  # 👈 added

    one_df = pd.DataFrame(input_data, columns=columns)
    st.dataframe(one_df)

    price = np.expm1(pipeline.predict(one_df))[0]
    st.success(f"💰 Estimated Price: ₹ {round(price, 2)} Crore")