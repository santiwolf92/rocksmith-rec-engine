import streamlit as st
import pandas as pd
from engine import generate_recommendations

st.set_page_config(page_title="Rocksmith Recommender", layout="wide")

st.title("🎸 Rocksmith CDLC Recommender")
st.markdown("Compare your Spotify + Last.fm listening data with your CDLC library.")

if st.button("🎯 Generate Recommendations"):
    with st.spinner("Crunching data..."):
        recs = generate_recommendations(save=False)
        st.success(f"Found {len(recs)} missing songs!")

        # Determine slider range
        max_possible = int(recs['Scrobbles'].max() or 100)
        min_possible = int(recs['Scrobbles'].min() or 0)

        # Dual sliders: min and max scrobbles
        min_scrobbles, max_scrobbles = st.slider(
            "Scrobble Range", min_possible, max_possible, (min_possible, max_possible)
        )

        # Filter by range
        filtered = recs[
            recs['Scrobbles'].fillna(0).between(min_scrobbles, max_scrobbles)
        ]

        # Display table
        st.dataframe(
            filtered[['Artist Name(s)', 'Track Name', 'Scrobbles']].reset_index(drop=True),
            use_container_width=True
        )

        # Download button
        csv = filtered[['Artist Name(s)', 'Track Name', 'Scrobbles']].to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download CSV", csv, "recommendations.csv", "text/csv")

