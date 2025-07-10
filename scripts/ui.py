import streamlit as st
import pandas as pd
from engine import generate_recommendations

st.set_page_config(page_title="Rocksmith Recommender", layout="wide")
st.title("🎸 Rocksmith CDLC Recommender")
st.markdown("Compare your Spotify + Last.fm listening data with your CDLC library.")

# Placeholder to avoid errors before generation
recs = pd.DataFrame()

# Set default slider ranges (you can adjust these)
min_slider_default = 0
max_slider_default = 1000

# Sliders that now affect recommendation generation
min_scrobbles = st.slider("Minimum Scrobbles", min_slider_default, max_slider_default, min_slider_default)
max_scrobbles = st.slider("Maximum Scrobbles", min_slider_default, max_slider_default, max_slider_default)

if st.button("🎯 Generate Recommendations"):
    with st.spinner("Crunching data..."):
        recs = generate_recommendations(min_scrobbles=min_scrobbles, max_scrobbles=max_scrobbles, save=False)
        st.success(f"Found {len(recs)} missing songs!")

        # Display table
        st.dataframe(
            recs[['Artist Name(s)', 'Track Name', 'Scrobbles']].reset_index(drop=True),
            use_container_width=True
        )

        # Download button
        csv = recs[['Artist Name(s)', 'Track Name', 'Scrobbles']].to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download CSV", csv, "recommendations.csv", "text/csv")

