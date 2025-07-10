import streamlit as st
import pandas as pd
from engine import generate_recommendations

st.set_page_config(page_title="Rocksmith Recommender", layout="wide")

st.title("🎸 Rocksmith CDLC Recommender")
st.markdown("Compare your Spotify + Last.fm listening data with your CDLC library.")

# Run recommendation generation only once
if "recs" not in st.session_state:
    if st.button("🎯 Generate Recommendations"):
        with st.spinner("Crunching data..."):
            recs = generate_recommendations(save=False)
            recs['Scrobbles'] = pd.to_numeric(recs['Scrobbles'], errors='coerce').fillna(0).astype(int)
            st.session_state.recs = recs
else:
    recs = st.session_state.recs

    st.success(f"Found {len(recs)} missing songs!")

    # Set min/max range
    min_val = int(recs['Scrobbles'].min())
    max_val = int(recs['Scrobbles'].max())

    # Dual slider for range
    scrobble_range = st.slider("Filter by Scrobbles", min_val, max_val, (min_val, max_val))
    min_scrobbles, max_scrobbles = scrobble_range

    # Filter
    filtered = recs[
        recs['Scrobbles'].between(min_scrobbles, max_scrobbles)
    ]

    # Display table
    st.dataframe(
        filtered[['Artist Name(s)', 'Track Name', 'Scrobbles']].reset_index(drop=True),
        use_container_width=True
    )

    # Download button
    csv = filtered[['Artist Name(s)', 'Track Name', 'Scrobbles']].to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv, "recommendations.csv", "text/csv")
