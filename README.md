# Music Recommender Simulation

## Project Summary

This project builds a content-based music recommendation system in Python. Given a user "taste profile" (preferred genre, mood, energy level, and acoustic preference), the system scores every song in a CSV catalog and returns the top matches with a plain-language explanation for each pick.

It is a simplified simulation of how real platforms like Spotify or YouTube Music decide what to play next — using math on song attributes instead of a neural network or crowd data.

---

## How The System Works

### Real-world context

Large streaming platforms use two main strategies:

- **Collaborative filtering** — "Users who liked X also liked Y." The system looks at the behavior of thousands of users and finds patterns across them. It does not need to know anything about the songs themselves.
- **Content-based filtering** — "This song has the same energy and mood as the one you just liked." The system compares song attributes directly to the user's known preferences. This is what our simulation uses.

Real apps like Spotify blend both approaches and add deep-learning layers on top. Our version focuses on the content-based side so the logic stays transparent and explainable.

### Features each song uses

| Feature | Type | Description |
|---|---|---|
| `genre` | categorical | Musical genre (pop, lofi, rock, r&b …) |
| `mood` | categorical | Emotional tone (happy, chill, intense …) |
| `energy` | float 0–1 | Perceived intensity and activity level |
| `tempo_bpm` | float | Beats per minute |
| `valence` | float 0–1 | Musical positiveness (happy-sounding vs sad) |
| `danceability` | float 0–1 | How suitable the track is for dancing |
| `acousticness` | float 0–1 | Confidence the track is acoustic |

### What the UserProfile stores

```python
UserProfile(
    favorite_genre="pop",     # preferred genre string
    favorite_mood="happy",    # preferred mood string
    target_energy=0.85,       # ideal energy level 0–1
    likes_acoustic=False,     # prefers acoustic or electronic sound
)
```

The functional API accepts the same data as a plain dictionary so profiles are easy to define inline in `main.py`.

### Algorithm Recipe (scoring one song)

| Rule | Points |
|---|---|
| Genre matches user preference | **+2.0** |
| Mood matches user preference | **+1.5** |
| Energy proximity: `1.0 − |song.energy − target_energy|` | **0 – 1.0** |
| Acousticness fit: `(1.0 − |song.acousticness − target|) × 0.5` | **0 – 0.5** |

Maximum possible score: **5.0**

Genre carries the most weight because genre is the strongest signal of what a listener actually wants. Mood is next. Energy is a continuous similarity score so a song that is 0.01 away from the target energy is barely penalised. Acousticness acts as a tiebreaker and texture preference.

### Ranking Rule

`recommend_songs(user_prefs, songs, k)` calls `score_song` on every track, collects `(song, score, explanation)` tuples, sorts them by score descending using Python's built-in `sorted()`, and returns the top `k`.

```
Input (user prefs dict)
        │
        ▼
┌───────────────────────────────────┐
│  For every song in the catalog:   │
│    score, reasons = score_song()  │
└───────────────────────────────────┘
        │
        ▼
Sort all (song, score) pairs — highest first
        │
        ▼
Return top-k with explanations
```

---

## Getting Started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Mac / Linux
.venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### Run the recommender

```bash
python -m src.main
```

### Run tests

```bash
pytest
```

---

## Terminal Output

Below is the actual output produced by `python -m src.main` across four user profiles.

```
Loaded songs: 22

============================================================
  Profile : High-Energy Pop Fan
============================================================
  #1  Sunrise City — Neon Echo
       Score : 4.96
       Why   : genre match (+2.0) | mood match (+1.5) | energy similarity (+0.97) | acousticness fit (+0.48)

  #2  Gym Hero — Max Pulse
       Score : 3.37
       Why   : genre match (+2.0) | energy similarity (+0.92) | acousticness fit (+0.45)

  #3  Rooftop Lights — Indigo Parade
       Score : 2.81
       Why   : mood match (+1.5) | energy similarity (+0.91) | acousticness fit (+0.40)

  #4  Neon Seoul — K-Glow
       Score : 1.44
       Why   : energy similarity (+0.97) | acousticness fit (+0.47)

  #5  Pulse Wave 99 — Circuit Dreams
       Score : 1.43
       Why   : energy similarity (+0.95) | acousticness fit (+0.48)

============================================================
  Profile : Chill Lofi Studier
============================================================
  #1  Midnight Coding — LoRoom
       Score : 4.94
       Why   : genre match (+2.0) | mood match (+1.5) | energy similarity (+0.96) | acousticness fit (+0.48)

  #2  Library Rain — Paper Lanterns
       Score : 4.92
       Why   : genre match (+2.0) | mood match (+1.5) | energy similarity (+0.97) | acousticness fit (+0.45)

  #3  Focus Flow — LoRoom
       Score : 3.46
       Why   : genre match (+2.0) | energy similarity (+0.98) | acousticness fit (+0.48)

  #4  Spacewalk Thoughts — Orbit Bloom
       Score : 2.81
       Why   : mood match (+1.5) | energy similarity (+0.90) | acousticness fit (+0.41)

  #5  Ipanema Dreams — Bossa Collective
       Score : 1.45
       Why   : energy similarity (+1.00) | acousticness fit (+0.45)

============================================================
  Profile : Deep Metal Head
============================================================
  #1  Iron Fist Rising — Skull Fracture
       Score : 4.96
       Why   : genre match (+2.0) | mood match (+1.5) | energy similarity (+1.00) | acousticness fit (+0.46)

  #2  Bass Drop Berlin — Klub Kurrent
       Score : 1.44
       Why   : energy similarity (+0.99) | acousticness fit (+0.45)

  #3  Storm Runner — Voltline
       Score : 1.42
       Why   : energy similarity (+0.94) | acousticness fit (+0.47)

  #4  Gym Hero — Max Pulse
       Score : 1.41
       Why   : energy similarity (+0.96) | acousticness fit (+0.45)

  #5  Neon Seoul — K-Glow
       Score : 1.38
       Why   : energy similarity (+0.91) | acousticness fit (+0.47)

============================================================
  Profile : Soulful R&B Listener
============================================================
  #1  Golden Hour — Silk Soul
       Score : 4.84
       Why   : genre match (+2.0) | mood match (+1.5) | energy similarity (+1.00) | acousticness fit (+0.34)

  #2  Velvet Static — Mirror Maze
       Score : 1.33
       Why   : energy similarity (+0.97) | acousticness fit (+0.36)

  #3  Open Road Anthem — Dusty Miles
       Score : 1.31
       Why   : energy similarity (+0.90) | acousticness fit (+0.41)

  #4  Crossroads Blues — Harp and Smoke
       Score : 1.31
       Why   : energy similarity (+0.82) | acousticness fit (+0.49)

  #5  Midnight Coding — LoRoom
       Score : 1.25
       Why   : energy similarity (+0.77) | acousticness fit (+0.48)
```

---

## Experiments You Tried

### Experiment 1 — Weight shift: doubling energy importance

Changed `energy_sim` contribution from `1.0 × energy_sim` to `2.0 × energy_sim` and halved genre weight to `1.0`.

Result: Songs with near-perfect energy proximity climbed the list even if they had no genre or mood match. "Ipanema Dreams" (bossa nova, energy 0.38) ranked #1 for the Lofi Studier profile above both lofi songs because the pure proximity beat everything. The output felt less intuitive — a jazz bossa nova song is not what a lofi fan expects even if the energy is identical.

Takeaway: genre is a stronger filter than raw energy in practice. Doubling energy made the system too agnostic about style.

### Experiment 2 — Feature removal: commenting out the mood check

Removed the `+1.5` mood bonus entirely. Ran all four profiles.

Result: The rankings for the Pop Fan barely changed (Sunrise City still #1 because genre already gave it 2.0 + near-perfect energy). But the Lofi Studier lost a key differentiator between "Midnight Coding" (chill) and "Focus Flow" (focused) — they became almost tied. The mood check is important for distinguishing songs within the same genre.

### Experiment 3 — Adversarial profile (conflicting preferences)

Tested profile: `energy: 0.9, mood: "sad"` (intense energy but sad mood).

No song in the catalog has an "sad" mood, so the mood bonus never fired. The system defaulted to a pure energy race: Iron Fist Rising, Bass Drop Berlin, Gym Hero. Technically correct but unsatisfying — a "sad but energetic" listener might want something that doesn't exist in this small catalog.

---

## Limitations and Risks

- **Filter bubble on genre**: Genre is worth 2.0 out of 5.0 maximum points, so songs from the user's preferred genre always dominate. A great track from a nearby genre (e.g., "indie pop" instead of "pop") gets no genre credit at all.
- **Small catalog**: 22 songs cannot represent the diversity of human musical taste. For niche genres like metal or bossa nova there is only one song each, so those profiles have weak competition for spots #2–5.
- **Exact string matching**: Genre and mood are matched as exact strings. "indie pop" never matches "pop", and "chill" never matches "relaxed" even though both describe a low-intensity feel.
- **No listening history**: The system treats every user as brand new. It cannot learn that this specific user actually prefers jazz even though they said "pop."
- **No lyrics or language**: Emotional content in lyrics is completely ignored. A hard-rock track with heartbreaking words scores the same as one with aggressive lyrics if the audio attributes are the same.

---

## Reflection

Building this system revealed how much simplification goes into a "recommendation." Real platforms like Spotify process hundreds of audio features extracted from the actual audio signal, billions of listening events, and social graphs — yet the core idea is the same: turn preferences into a number, rank, return top results.

The most surprising moment was the adversarial experiment. A user asking for "sad but high-energy" music had their mood preference completely ignored because no matching song existed in the catalog. In a real app with millions of songs, this gap would shrink — but the fundamental brittleness of exact-string genre/mood matching would still cause problems at the edges of taste.

AI bias can appear even in a 22-song catalog. Because 5 of the 22 songs are pop or indie pop, any user with "pop" as a genre preference gets disproportionately good coverage while a metal fan gets only one real match and then a fallback to generic high-energy songs. This mirrors real-world problems where under-represented genres (regional music, niche subcultures) get fewer recommendations even when user demand exists.

See [model_card.md](model_card.md) for the full evaluation, bias analysis, and future work.
