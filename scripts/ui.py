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

        # Ensure Scrobbles column is numeric
        recs['Scrobbles'] = pd.to_numeric(recs['Scrobbles'], errors='coerce').fillna(0).astype(int)

        # Add a range slider for scrobbles
        min_s, max_s = int(recs['Scrobbles'].min()), int(recs['Scrobbles'].max())
        scrobble_range = st.slider("Filter by Scrobbles", min_s, max_s, (min_s, max_s))

        # Filter the DataFrame
        filtered = recs[
            (recs['Scrobbles'] >= scrobble_range[0]) &
            (recs['Scrobbles'] <= scrobble_range[1])
        ]

        # Show results
        st.dataframe(
            filtered[['Artist Name(s)', 'Track Name', 'Scrobbles']].reset_index(drop=True),
            use_container_width=True
        )

        # Download button
        csv = filtered[['Artist Name(s)', 'Track Name', 'Scrobbles']].to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download CSV", csv, "recommendations.csv", "text/csv")


        # Download button
        csv = filtered[["Artist Name(s)", "Track Name", "Scrobbles"]].to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", csv, "recommendations.csv", "text/csv")

