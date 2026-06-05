import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os

csv_path = os.path.join(os.path.dirname(__file__), "data_viz1.csv")
new_df = pd.read_csv(csv_path)

sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0,'overall')

st.title("🏡 Gurugram Real Estate 🏡")
selected_sector = st.selectbox(
    "Select any sector",
    sector_options)

group_df = new_df.groupby('sector')[['bedRoom', 'price_per_sqft', 'super_built_up_area', 'latitude', 'longitude']].mean()
st.header('Sector Price per Sqft Geomap')
fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="bedRoom", size="price_per_sqft",
                        color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                        mapbox_style="open-street-map", width=1200, height=700, hover_name=group_df.index)

if selected_sector != 'overall':
    selected_sector_df = group_df.loc[[selected_sector]]
    fig.add_trace(px.scatter_mapbox(selected_sector_df, lat="latitude", lon="longitude",
                                    color_discrete_sequence=["red"], size_max=15).data[0])

st.plotly_chart(fig, use_container_width=True)


st.header('Area Vs Price')
if selected_sector =='overall':
    property_type = st.selectbox('Select Property Type', ['flat','house'])

    if property_type == 'house':
        fig1 = plt.figure(figsize=(6,3.6))
        sns.scatterplot(data = new_df[new_df['property_type'] == 'house'], x="super_built_up_area", y="price", hue="bedRoom")
        st.pyplot(fig1)
    else:
        fig1 = plt.figure(figsize=(6,3.6))
        sns.scatterplot(data=new_df[new_df['property_type'] == 'flat'], x="super_built_up_area", y="price", hue="bedRoom")
        st.pyplot(fig1)
else:
    property_type = st.selectbox('Select Property Type', ['flat', 'house'])

    if property_type == 'house':
        fig1 = plt.figure(figsize=(6, 3.6))
        sns.scatterplot(data=new_df[(new_df['property_type'] == 'house') & (new_df['sector'] == selected_sector)], x="super_built_up_area", y="price",
                        hue="bedRoom")
        st.pyplot(fig1)
    else:
        fig1 = plt.figure(figsize=(6, 3.6))
        sns.scatterplot(data=new_df[(new_df['property_type'] == 'flat') & (new_df['sector'] == selected_sector)], x="super_built_up_area", y="price",
                        hue="bedRoom")
        st.pyplot(fig1)
st.subheader('Bedroom Availability in Flats and Houses')


def change(a):
    if a > 6:
        return "6+"
    else:
        return a
temdf = new_df.copy()
temdf["bedRoom"] = temdf["bedRoom"].apply(change)


if selected_sector == 'overall':
    fig4 = plt.figure(figsize=(6,4))
    sns.countplot(data=temdf,x='bedRoom',hue='property_type')
    st.pyplot(fig4)

else:

    fig2 =plt.figure(figsize=(6,4))
    sns.countplot(data=temdf[temdf['sector'] == selected_sector],x='bedRoom',hue='property_type')
    st.pyplot(fig2, use_container_width=True)


st.subheader('Side by Side BHK price comparison')
if selected_sector =="overall":
    temdfh = temdf[temdf['property_type'] == 'house']
    fig3 = px.box(temdfh, x='bedRoom', y='price', title='BHK Price Range Houses')
    st.plotly_chart(fig3, use_container_width=True)

    temdfh = temdf[temdf['property_type'] == 'flat']
    fig3 = px.box(temdfh, x='bedRoom', y='price', title='BHK Price Range flats')
    st.plotly_chart(fig3, use_container_width=True)
else:
    temdfh = temdf[temdf['property_type'] == 'house']
    fig3 = px.box(temdfh[temdfh['sector']==selected_sector], x='bedRoom', y='price', title='BHK Price Range Houses')
    st.plotly_chart(fig3, use_container_width=True)

    temdfh = temdf[temdf['property_type'] == 'flat']
    fig3 = px.box(temdfh[temdfh['sector'] == selected_sector], x='bedRoom', y='price', title='BHK Price Range flats')
    st.plotly_chart(fig3, use_container_width=True)


st.subheader('Age possession of house and flats')
if selected_sector == 'overall':
    fig4 = plt.figure(figsize=(6,4))
    sns.countplot(data=temdf,x='agePossession',hue='property_type')
    st.pyplot(fig4)

else:

    fig2 =plt.figure(figsize=(6,4))
    sns.countplot(data=temdf[temdf['sector'] == selected_sector],x='agePossession',hue='property_type')
    st.pyplot(fig2, use_container_width=True)

st.header('Side by Side Distplot for property type')

fig3 = plt.figure(figsize=(10, 4))
sns.histplot(data=new_df[new_df['property_type'] == 'house'],x='price',kde=True,label='house')
sns.histplot(data=new_df[new_df['property_type'] == 'flat'],x='price',kde=True, label='flat')
plt.legend()
st.pyplot(fig3)


