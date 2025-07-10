import streamlit as st
import pandas as pd
from engine import generate_recommendations

st.set_page_config(page_title="Rocksmith Recommender", layout="wide")

st.title("🎸 Rocksmith CDLC Recommender")
st.markdown("Compare your Spotify + Last.fm listening data with your CDLC library.")

if st.button("🎯 Generate Recommendations"):
    with st.spinner("Crunching data..."):
        recs = generate_recommendations(save=False)

        # Ensure Scrobbles column is numeric
        recs["Scrobbles"] = pd.to_numeric(recs["Scrobbles"], errors="coerce")

        st.success(f"Found {len(recs)} missing songs!")

        # Compute min/max for slider bounds
        min_val = int(recs["Scrobbles"].min() or 0)
        max_val = int(recs["Scrobbles"].max() or 0)

        # Dual slider to filter scrobbles range
        min_scrobbles, max_scrobbles = st.slider(
            "Filter by Scrobbles",
            min_value=min_val,
            max_value=max_val,
            value=(min_val, max_val),
        )

        # Apply filtering
        filtered = recs[
            recs["Scrobbles"].fillna(0).between(min_scrobbles, max_scrobbles)
        ]

        # Display table
        st.dataframe(
            filtered[["Artist Name(s)", "Track Name", "Scrobbles"]].reset_index(drop=True),
            use_container_width=True
        )

        # Download button
        csv = filtered[["Artist Name(s)", "Track Name", "Scrobbles"]].to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", csv, "recommendations.csv", "text/csv")

