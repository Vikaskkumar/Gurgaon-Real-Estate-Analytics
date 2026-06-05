import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analysis", layout="wide")
st.title("Gurgaon Sector Price Map")

df = pd.read_csv('pages/new.csv')

# ── Geo Map ────────────────────────────────────────────────────────────────────
temp_df = df.groupby('sector').agg(
    avg_price=('price', 'mean'),
    latitude=('latitude', 'first'),
    longitude=('longitude', 'first')
).reset_index().dropna(subset=['latitude', 'longitude'])

fig_map = px.scatter_map(temp_df, lat='latitude', lon='longitude',
                         color='avg_price', size='avg_price',
                         hover_name='sector', zoom=11, height=600,
                         color_continuous_scale='Turbo', size_max=30)
fig_map.update_layout(map_style='open-street-map', margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_map, use_container_width=True)

# ── Word Cloud ─────────────────────────────────────────────────────────────────
st.subheader("Feature Word Cloud")

text = ' '.join(df.columns.str.replace('_', ' ').tolist())
wc = WordCloud(width=1600, height=600, background_color='black',
               colormap='plasma', scale=2).generate(text)

fig_wc, ax = plt.subplots(figsize=(16, 6))
ax.imshow(wc, interpolation='bilinear')
ax.axis('off')
fig_wc.tight_layout(pad=0)
st.pyplot(fig_wc, use_container_width=True)

#-----
st.subheader("Area vs Price")

fig_scatter = px.scatter(df, x='built_up_area', y='price',
                         color='price_per_sqft', size='price',
                         hover_name='sector',
                         color_continuous_scale='blues',
                         height=500)
st.plotly_chart(fig_scatter, use_container_width=True)


#----pie chart

st.subheader("BHK Distribution by Sector")

sector_list = ['All'] + sorted(df['sector'].unique().tolist())
selected = st.selectbox("Select Sector", sector_list)

filtered = df if selected == 'All' else df[df['sector'] == selected]

fig_pie = px.pie(filtered, names='bedRoom', height=500,
                 color_discrete_sequence=px.colors.qualitative.Vivid)
st.plotly_chart(fig_pie, use_container_width=True)


#---bedroom

st.subheader("Price Distribution by Bedroom")

fig_box = px.box(df, x='bedRoom', y='price',
                 color='bedRoom',
                 color_discrete_sequence=px.colors.qualitative.Vivid,
                 height=500)
st.plotly_chart(fig_box, use_container_width=True)


#--------------------
st.subheader("Price Distribution: Flat vs House")

import plotly.figure_factory as ff

flat  = df[df['property_type'] == 'flat']['price'].dropna().tolist()
house = df[df['property_type'] == 'house']['price'].dropna().tolist()

fig_dist = ff.create_distplot([flat, house], ['Flat', 'House'],
                               colors=['#6c63ff', '#f9826c'],
                               show_hist=False, show_rug=False)
fig_dist.update_layout(height=500)
st.plotly_chart(fig_dist, use_container_width=True)