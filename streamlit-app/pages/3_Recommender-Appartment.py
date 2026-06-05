import streamlit as st
import pickle
import os

st.set_page_config(page_title="Find Apartments", layout="wide")

file_path = os.path.join(os.path.dirname(__file__), 'location_distance.pkl')
with open(file_path, 'rb') as f:
    location_df = pickle.load(f)

st.markdown("""
<style>
.hero {
    background: #185FA5;
    border-radius: 14px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.5rem;
}
.hero h1 { color: #E6F1FB; font-size: 1.6rem; margin-bottom: 4px; }
.hero p  { color: #85B7EB; font-size: 0.9rem; }

.prop-card {
    border-radius: 12px;
    border: 1px solid #e0e0e0;
    overflow: hidden;
    margin-bottom: 1rem;
    display: flex;
}
.accent-bar { width: 7px; flex-shrink: 0; }
.card-body  { padding: 1rem 1.25rem; flex: 1; }
.card-name  { font-size: 1.05rem; font-weight: 600; color: #e8e8e8; }
.card-sub   { font-size: 0.83rem; color: #666; margin: 4px 0 10px; }

.dist-pill {
    display: inline-block;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.75rem;
    font-weight: 500;
    margin-bottom: 8px;
}
.tag {
    display: inline-block;
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.75rem;
    font-weight: 500;
    margin: 2px 3px 2px 0;
}
.sim-card {
    background: #f8f9fa;
    border: 1px solid #e8e8e8;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 6px;
}
.sim-name { font-size: 0.85rem; font-weight: 600; }
.sim-dist { font-size: 0.78rem; color: #888; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🏙️ Find your next home</h1>
  <p>Discover apartments and properties near any location</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2.5, 1, 0.8])
with col1:
    selected_location = st.selectbox("📍 Location", sorted(location_df.columns.to_list()))
with col2:
    radius = st.number_input("Radius (km)", min_value=1, max_value=100, value=5)
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    search = st.button("🔍 Search", use_container_width=True)

PALETTES = [
    {"accent": "#1D9E75", "dist_bg": "#E1F5EE", "dist_text": "#085041",
     "tag_bg": "#9FE1CB",  "tag_text": "#04342C"},
    {"accent": "#534AB7", "dist_bg": "#EEEDFE", "dist_text": "#26215C",
     "tag_bg": "#CECBF6",  "tag_text": "#26215C"},
    {"accent": "#D85A30", "dist_bg": "#FAECE7", "dist_text": "#4A1B0C",
     "tag_bg": "#F5C4B3",  "tag_text": "#4A1B0C"},
]

if search:
    result_ser = (
        location_df[location_df[selected_location] < radius * 1000][selected_location]
        .sort_values()
    )
    if result_ser.empty:
        st.warning(f"No properties found within {radius} km of **{selected_location}**.")
        st.stop()

    st.markdown(f"**{len(result_ser)} properties** found within **{radius} km** of {selected_location}")
    st.markdown("")

    for idx, (name, dist_m) in enumerate(result_ser.items()):
        pal = PALETTES[idx % len(PALETTES)]
        dist_km = round(dist_m / 1000, 1)

        similar = (
            location_df[location_df[selected_location] < radius * 1000][selected_location]
            .sort_values()
            .drop(index=name, errors="ignore")
        )
        similar = similar[abs(similar - dist_m) < 3000]

        st.markdown(f"""
        <div class="prop-card">
          <div class="accent-bar" style="background:{pal['accent']}"></div>
          <div class="card-body">
            <div style="display:flex;justify-content:space-between;align-items:center">
              <span class="card-name">🏢 {name}</span>
              <span class="dist-pill" style="background:{pal['dist_bg']};color:{pal['dist_text']}">{dist_km} km away</span>
            </div>
            <div class="card-sub">📍 {dist_km} km from {selected_location} &nbsp;·&nbsp; Residential</div>
            <span class="tag" style="background:{pal['tag_bg']};color:{pal['tag_text']}">Apartment</span>
            <span class="tag" style="background:{pal['tag_bg']};color:{pal['tag_text']}">{len(similar)} nearby</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if not similar.empty:
            with st.expander(f"View {len(similar)} similar properties near {name}"):
                cols = st.columns(min(len(similar), 3))
                for j, (sim_name, sim_dist) in enumerate(similar.items()):
                    sp = PALETTES[j % len(PALETTES)]
                    with cols[j % 3]:
                        st.markdown(f"""
                        <div class="sim-card">
                          <div class="sim-name" style="color:{sp['accent']}">{sim_name}</div>
                          <div class="sim-dist">📍 {round(sim_dist/1000,1)} km away</div>
                        </div>
                        """, unsafe_allow_html=True)