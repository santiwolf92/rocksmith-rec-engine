# 🎸 Rocksmith Recommendation Engine

This project cross-references your **Rocksmith CDLC library** with your **listening history** from **Spotify** and **Last.fm** to generate **personalized song recommendations** — making sure you’re learning the music you love.

---

## 📁 Project Structure

- `data/`
  - `cdlc_library.csv` – Your existing Rocksmith CDLCs
  - `spotify_liked.csv` – Liked songs from Spotify
  - `spotify_top.csv` – Top songs by year (2018–2024)
  - `lastfm_artists.csv` – Most-played artists from Last.fm
  - `playlists/`
    - `1000_de_aspen.csv`
    - `hay_algo_ahi_musica.csv`
  - `recommendations/`
    - `recommendations.csv`
- `scripts/`
  - `analyze.py` *(coming soon)*
- `.gitignore`
- `README.md` – This file
---

## 📊 Data Sources

- **CDLC Library**: Extracted from Rocksmith `.psarc` filenames
- **Spotify Liked Songs**: Full export with metadata like energy, danceability, etc.
- **Spotify Top Songs**: From Spotify Wrapped (2018–2024) with `Top Year` column
- **Last.fm Artists**: Ranked scrobbles showing your most listened-to artists
- **Playlists**: Taste-influencing but not definitive listening history

---

## 🚀 Goals

- Identify **CDLCs you’re missing** from your favorite artists
- Recommend **new songs** based on genre/mood/vibe
- Highlight **gaps** between your listening and learning
- Generate **custom song packs** based on themes like:
  - “Your 2000s Alt Rock Phase”
  - “Most Played, Not Yet Played”
  - “Hidden Gems You’d Actually Shred”

---

## 🛠️ How It Works (Soon)

Scripts in `/scripts` will:
- Parse and normalize data
- Find artist/song overlaps and gaps
- Rank suggestions by relevance and uniqueness
- Output ready-to-import Rocksmith recommendations

---

## 🔮 Coming Soon

- Auto-refresh from Spotify + Last.fm exports
- Interactive CLI or notebook
- Genre and era insights

---

Built for passion, by and for someone who *really* loves music.
