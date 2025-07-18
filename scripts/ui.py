import streamlit as st
import pandas as pd
from engine import generate_recommendations
import subprocess
import os

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
    st.session_state.max_scrobbles = 500
if 'filter_existing' not in st.session_state:
    st.session_state.filter_existing = False

# Fixed scrobble slider cap between 1 and 500
slider_cap = 500

# Sidebar options
with st.sidebar:
    st.header("🔧 Settings")
    min_scrobbles = st.slider("Minimum Scrobbles", 1, slider_cap, st.session_state.min_scrobbles)
    max_scrobbles = st.slider("Maximum Scrobbles", 1, slider_cap, st.session_state.max_scrobbles)
    filter_existing = st.checkbox("✅ Only show songs that exist on CustomsForge", value=st.session_state.filter_existing)

# Progress callback
def streamlit_progress_callback():
    progress_bar = st.progress(0)
    status_text = st.empty()

    def callback(current, total, artist, track):
        pct = current / total
        progress_bar.progress(pct)
        status_text.markdown(f"🔍 Checking `{artist}` — `{track}` ({current}/{total})")

    return callback

# Generate button
if st.button("🎯 Generate Recommendations"):
    with st.spinner("Crunching data..."):
        st.session_state.offset = 0
        st.session_state.min_scrobbles = min_scrobbles
        st.session_state.max_scrobbles = max_scrobbles
        st.session_state.filter_existing = filter_existing

        update_cb = streamlit_progress_callback() if filter_existing else None

        all_recs = generate_recommendations(
            top_n=50,
            save=False,
            min_scrobbles=min_scrobbles,
            max_scrobbles=max_scrobbles,
            filter_existing=filter_existing,
            update_progress=update_cb,
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

    csv = st.session_state.recs.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv, "recommendations.csv", "text/csv")

# Update CDLC Library button
if st.button("🔁 Update CDLC Library"):
    try:
        script_path = os.path.join(os.path.dirname(__file__), "update_cdlc_library.py")
        result = subprocess.run(["python", script_path], check=True, capture_output=True, text=True)
        st.success("✅ CDLC library updated successfully.")
        st.text(result.stdout)
    except subprocess.CalledProcessError as e:
        st.error("❌ Failed to update CDLC library.")
        st.text(e.stderr)

