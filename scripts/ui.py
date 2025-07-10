import streamlit as st
import pandas as pd
from engine import generate_recommendations
import subprocess

st.set_page_config(page_title="Rocksmith Recommender", layout="wide")

st.title("🎸 Rocksmith CDLC Recommender")
st.markdown("Compare your Spotify + Last.fm listening data with your CDLC library.")

# Initialize session state
if 'recs' not in st.session_state:
    st.session_state.recs = pd.DataFrame()
if 'offset' not in st.session_state:
    st.session_state.offset = 0
if 'min_scrobbles' not in st.session_state:
    st.session_state.min_scrobbles = 0
if 'max_scrobbles' not in st.session_state:
    st.session_state.max_scrobbles = 500  # default cap

# Determine dynamic max based on real data, with 500 as upper cap
temp_recs = generate_recommendations(top_n=1, save=False)
true_max = int(temp_recs['Scrobbles'].max() or 0)
slider_cap = min(500, true_max)

# Sliders for generation filters
min_scrobbles = st.slider("Minimum Scrobbles", 0, slider_cap, st.session_state.min_scrobbles)
max_scrobbles = st.slider("Maximum Scrobbles", 0, slider_cap, st.session_state.max_scrobbles)

# Checkbox for filtering existing CDLC
filter_existing = st.checkbox("Only show songs available on CustomsForge")

# Generate button
if st.button("🎯 Generate Recommendations"):
    with st.spinner("Crunching data..."):
        st.session_state.offset = 0
        st.session_state.min_scrobbles = min_scrobbles
        st.session_state.max_scrobbles = max_scrobbles

        all_recs = generate_recommendations(
            top_n=500,
            save=False,
            min_scrobbles=min_scrobbles,
            max_scrobbles=max_scrobbles,
            filter_existing=filter_existing
        )
        filtered = all_recs.reset_index(drop=True)

        st.session_state.recs = filtered.head(50)
        st.session_state.all_filtered = filtered

# Load More button
if not st.session_state.recs.empty and st.button("➕ Load 50 More"):
    st.session_state.offset += 50
    start = st.session_state.offset
    end = start + 50
    new_recs = st.session_state.all_filtered.iloc[start:end]
    st.session_state.recs = pd.concat([st.session_state.recs, new_recs], ignore_index=True)

# Display recommendations
if not st.session_state.recs.empty:
    st.success(f"Showing {len(st.session_state.recs)} recommendations")
    st.dataframe(
        st.session_state.recs[['Artist Name(s)', 'Track Name', 'Scrobbles']],
        use_container_width=True
    )

    # Download button
    csv = st.session_state.recs.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv, "recommendations.csv", "text/csv")

# Update CDLC library button
if st.button("🔄 Update CDLC Library"):
    with st.spinner("Updating CDLC library..."):
        result = subprocess.run(["python", "scripts/update_cdlc_library.py"], capture_output=True, text=True)
        if result.returncode == 0:
            st.success("CDLC library updated successfully.")
        else:
            st.error("❌ Failed to update CDLC library.")
            st.code(result.stderr)

