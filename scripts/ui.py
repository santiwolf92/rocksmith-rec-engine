import streamlit as st
import pandas as pd
from engine import generate_recommendations

st.set_page_config(page_title="Rocksmith Recommender", layout="wide")

st.title("🎸 Rocksmith CDLC Recommender")
st.markdown("Compare your Spotify + Last.fm listening data with your CDLC library.")

# Session state to persist data
if "recs" not in st.session_state:
    st.session_state.recs = None

# Generate button
if st.button("🎯 Generate Recommendations"):
    with st.spinner("Crunching data..."):
        recs = generate_recommendations(save=False)
        recs['Scrobbles'] = pd.to_numeric(recs['Scrobbles'], errors='coerce').fillna(0).astype(int)
        st.session_state.recs = recs
        st.success(f"Found {len(recs)} missing songs!")

# If we already have recommendations
if st.session_state.recs is not None:
    recs = st.session_state.recs

    # Slider for min/max scrobbles
    min_s, max_s = recs['Scrobbles'].min(), recs['Scrobbles'].max()
    min_val, max_val = st.slider("🎚️ Filter by Scrobbles", min_value=int(min_s), max_value=int(max_s), value=(int(min_s), int(max_s)))

    # Apply filter
    filtered = recs[(recs['Scrobbles'] >= min_val) & (recs['Scrobbles'] <= max_val)]

    # Display table
    st.dataframe(filtered[['Artist Name(s)', 'Track Name', 'Scrobbles']].reset_index(drop=True), use_container_width=True)

    # CSV download
    csv = filtered[['Artist Name(s)', 'Track Name', 'Scrobbles']].to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv, "recommendations.csv", "text/csv")

