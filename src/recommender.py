import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Compute a weighted score for a song against a user profile."""
        score = 0.0
        reasons = []

        if song.genre == user.favorite_genre:
            score += 2.0
            reasons.append("genre match (+2.0)")

        if song.mood == user.favorite_mood:
            score += 1.5
            reasons.append("mood match (+1.5)")

        energy_sim = 1.0 - abs(song.energy - user.target_energy)
        score += energy_sim
        reasons.append(f"energy similarity (+{energy_sim:.2f})")

        target_acousticness = 0.75 if user.likes_acoustic else 0.15
        acoustic_sim = 1.0 - abs(song.acousticness - target_acousticness)
        score += acoustic_sim * 0.5
        reasons.append(f"acousticness fit (+{acoustic_sim * 0.5:.2f})")

        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by weighted score for the given user profile."""
        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation for why a song was recommended."""
        _, reasons = self._score(user, song)
        return ", ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences, returning (score, reasons)."""
    score = 0.0
    reasons = []

    if song.get("genre") == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song.get("mood") == user_prefs.get("mood"):
        score += 1.5
        reasons.append("mood match (+1.5)")

    target_energy = user_prefs.get("energy", 0.5)
    energy_sim = 1.0 - abs(song["energy"] - target_energy)
    score += energy_sim
    reasons.append(f"energy similarity (+{energy_sim:.2f})")

    if "likes_acoustic" in user_prefs:
        target_acousticness = 0.75 if user_prefs["likes_acoustic"] else 0.15
        acoustic_sim = 1.0 - abs(song["acousticness"] - target_acousticness)
        score += acoustic_sim * 0.5
        reasons.append(f"acousticness fit (+{acoustic_sim * 0.5:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, sort by score descending, and return the top-k as (song, score, explanation)."""
    scored = []
    for song in songs:
        s, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored.append((song, s, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
