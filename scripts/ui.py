import streamlit as st
import pandas as pd
from engine import generate_recommendations

st.set_page_config(page_title="Rocksmith Recommender", layout="wide")
st.title("🎸 Rocksmith CDLC Recommender")
st.markdown("Compare your Spotify + Last.fm listening data with your CDLC library.")

# User input sliders BEFORE recommendation generation
st.markdown("### Filter by Scrobbles Before Generating:")
min_scrobbles = st.slider("Minimum Scrobbles", 0, 1000, 0)
max_scrobbles = st.slider("Maximum Scrobbles", min_scrobbles + 1, 1000, 1000)

if st.button("🎯 Generate Recommendations"):
    with st.spinner("Crunching data..."):
        recs = generate_recommendations(
            save=False,
            min_scrobbles=min_scrobbles,
            max_scrobbles=max_scrobbles
        )
        st.success(f"Found {len(recs)} matching songs!")

        if recs.empty:
            st.warning("No recommendations matched your filters.")
        else:
            st.dataframe(
                recs[['Artist Name(s)', 'Track Name', 'Scrobbles']].reset_index(drop=True),
                use_container_width=True
            )
            csv = recs[['Artist Name(s)', 'Track Name', 'Scrobbles']].to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download CSV", csv, "recommendations.csv", "text/csv")

