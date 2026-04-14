"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:
    python -m src.main
"""

import os
from src.recommender import load_songs, recommend_songs

SONGS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")

# --- User Profiles ---
PROFILES = {
    "High-Energy Pop Fan": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "likes_acoustic": False,
    },
    "Chill Lofi Studier": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "likes_acoustic": True,
    },
    "Deep Metal Head": {
        "genre": "metal",
        "mood": "aggressive",
        "energy": 0.97,
        "likes_acoustic": False,
    },
    "Soulful R&B Listener": {
        "genre": "r&b",
        "mood": "warm",
        "energy": 0.65,
        "likes_acoustic": True,
    },
}


def print_recommendations(profile_name: str, recs) -> None:
    """Print a clean formatted block of recommendations for one user profile."""
    print("=" * 60)
    print(f"  Profile : {profile_name}")
    print("=" * 60)
    for rank, (song, score, explanation) in enumerate(recs, start=1):
        print(f"  #{rank}  {song['title']} — {song['artist']}")
        print(f"       Score : {score:.2f}")
        print(f"       Why   : {explanation}")
        print()


def main() -> None:
    songs = load_songs(SONGS_PATH)
    print(f"Loaded songs: {len(songs)}\n")

    for profile_name, user_prefs in PROFILES.items():
        recs = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(profile_name, recs)


if __name__ == "__main__":
    main()
