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

        # Filter by scrobbles
        min_scrobbles = st.slider("Minimum Scrobbles", 0, int(recs['Scrobbles'].max() or 0), 0)
        filtered = recs[recs['Scrobbles'].fillna(0) >= min_scrobbles]

        # Display table
        st.dataframe(
            filtered[['Artist Name(s)', 'Track Name', 'Scrobbles']].reset_index(drop=True),
            use_container_width=True
        )

        # Download button
        csv = filtered[['Artist Name(s)', 'Track Name', 'Scrobbles']].to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download CSV", csv, "recommendations.csv", "text/csv")
