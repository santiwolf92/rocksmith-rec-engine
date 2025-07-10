import streamlit as st
import pandas as pd
import subprocess
from engine import generate_recommendations

st.set_page_config(page_title="Rocksmith Recommender", layout="wide")

st.title("🎸 Rocksmith CDLC Recommender")
st.markdown("Compare your Spotify + Last.fm listening data with your CDLC library.")

# ✅ CDLC Update Button
if st.button("🔄 Update CDLC Library"):
    with st.spinner("Scanning DLC folder and updating library..."):
        try:
            result = subprocess.run(
                ["python", "scripts/update_cdlc_library.py"],
                capture_output=True,
                text=True,
                check=True
            )
            st.success("✅ CDLC library updated successfully.")
            st.text(result.stdout)
        except subprocess.CalledProcessError as e:
            st.error("⚠️ Failed to update CDLC library.")
            st.text(e.stderr)

# === Session State Setup ===
if 'recs' not in st.session_state:
    st.session_state.recs = pd.DataFrame()
if 'offset' not in st.session_state:
    st.session_state.offset = 0
if 'min_scrobbles' not in st.session_state:
    st.session_state.min_scrobbles = 0
if 'max_scrobbles' not in st.session_state:
    st.session_state.max_scrobbles = 500  # default cap

# === Dynamic slider range ===
temp_recs = generate_recommendations(top_n=1, save=False)
true_max = int(temp_recs['Scrobbles'].max() or 0)
slider_cap = min(500, true_max)

# === Sliders ===
min_scrobbles = st.slider("Minimum Scrobbles", 0, slider_cap, st.session_state.min_scrobbles)
max_scrobbles = st.slider("Maximum Scrobbles", 0, slider_cap, st.session_state.max_scrobbles)

# === Generate Recommendations ===
if st.button("🎯 Generate Recommendations"):
    with st.spinner("Crunching data..."):
        st.session_state.offset = 0
        st.session_state.min_scrobbles = min_scrobbles
        st.session_state.max_scrobbles = max_scrobbles

        all_recs = generate_recommendations(top_n=500, save=False)
        filtered = all_recs[
            all_recs['Scrobbles'].fillna(0).between(min_scrobbles, max_scrobbles)
        ].reset_index(drop=True)

        st.session_state.recs = filtered.head(50)
        st.session_state.all_filtered = filtered

# === Load More ===
if not st.session_state.recs.empty and st.button("➕ Load 50 More"):
    st.session_state.offset += 50
    start = st.session_state.offset
    end = start + 50
    new_recs = st.session_state.all_filtered.iloc[start:end]
    st.session_state.recs = pd.concat([st.session_state.recs, new_recs], ignore_index=True)

# === Display Results ===
if not st.session_state.recs.empty:
    st.success(f"Showing {len(st.session_state.recs)} recommendations")
    st.dataframe(
        st.session_state.recs[['Artist Name(s)', 'Track Name', 'Scrobbles']],
        use_container_width=True
    )  # ← This closing parenthesis was missing

    # === Download Button ===
    csv = st.session_state.recs.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv, "recommendations.csv", "text/csv")

