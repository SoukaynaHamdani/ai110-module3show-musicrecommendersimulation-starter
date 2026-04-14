# Model Card: VibeFinder 1.0

## 1. Model Name

**VibeFinder 1.0**

A content-based music recommender simulation built for the CodePath AI110 course.

---

## 2. Intended Use

VibeFinder 1.0 is designed to suggest songs from a small catalog that match a user's stated preferences for genre, mood, energy level, and acoustic texture.

- **Who it is for**: Classroom exploration and learning. It is meant to demonstrate how a simple scoring algorithm can turn user preferences into a ranked list of recommendations.
- **What it predicts**: The top-k songs most likely to match a user profile, based on song attributes stored in a CSV file.
- **What it is NOT for**: Real production use, personalisation at scale, or any commercial music discovery product. It makes no claims about what any real user would enjoy.

---

## 3. How the Model Works

Every song in the catalog is given a score based on how closely it matches the user's preferences. The scoring works like a point system:

- If the song's genre matches what the user prefers, it earns **2 points**. Genre is worth the most because it is the strongest single signal of musical taste.
- If the song's mood matches, it earns **1.5 points**. Mood is the emotional texture of the song — happy, chill, intense, etc.
- The song then earns up to **1 point** based on how close its energy level is to the user's target. A song that exactly matches the target energy gets 1.0; a song that is very far away gets close to 0.
- If the user has a preference for acoustic or electronic sound, the song earns up to **0.5 points** based on how acoustic it is.

Once every song has a score, the list is sorted from highest to lowest and the top results are returned, along with a short explanation of what contributed to each score.

The maximum possible score is **5.0**. A song that perfectly matches on genre, mood, energy, and acousticness would score 5.0.

---

## 4. Data

| Property | Detail |
|---|---|
| Total songs | 22 |
| Source | Manually created synthetic catalog |
| Original songs | 10 (starter dataset) |
| Added songs | 12 (expanded for diversity) |

**Genres represented**: pop, lofi, rock, ambient, jazz, synthwave, indie pop, r&b, edm, classical, hip-hop, country, metal, bossa nova, indie folk, k-pop, blues, indie

**Moods represented**: happy, chill, intense, relaxed, focused, moody, warm, euphoric, melancholic, confident, nostalgic, aggressive, energetic

**Genre distribution** (songs per genre):
- pop: 2, lofi: 3, rock: 1, ambient: 1, jazz: 1, synthwave: 2, indie pop: 1, r&b: 1, edm: 1, classical: 1, hip-hop: 1, country: 1, metal: 1, bossa nova: 1, indie folk: 1, k-pop: 1, blues: 1, indie: 1

**Limitations of the data**:
- All data is synthetic — no real audio was processed.
- Attribute values were assigned manually and do not come from audio analysis tools like Spotify's API.
- Pop and lofi are slightly over-represented compared to the rest of the catalog.
- Whose taste this reflects is unclear because all songs were created for demonstration purposes.

---

## 5. Strengths

- **Transparent**: Every recommendation comes with a plain-English explanation of exactly which attributes matched and by how much. There are no hidden layers.
- **Fast**: Scoring 22 songs takes milliseconds. The algorithm is O(n) and easily scales to larger catalogs.
- **Works well for strong-preference users**: If a user has a clear genre and mood preference and the catalog has songs matching that, the top results are consistently intuitive. The Lofi Studier and High-Energy Pop Fan profiles both produced rankings that felt exactly right.
- **Interpretable for teaching**: The weighted-point system is easy to reason about, modify, and explain — ideal for understanding the basic mechanics of content-based filtering.

---

## 6. Limitations and Bias

**Filter bubble on genre**: Because genre is worth 2.0 out of a maximum 5.0, songs from the preferred genre dominate the top results. Songs from adjacent genres (e.g., "indie pop" vs "pop") receive zero genre credit even if they are stylistically very close. Over time, a system like this would reinforce the user's existing taste rather than broadening it.

**Exact string matching**: Genre and mood are compared as exact strings. "chill" and "relaxed" are treated as completely different moods. This means a user who wants something "relaxed" will never get credit for songs labelled "chill" even though the distinction is tiny.

**Catalog imbalance**: With only one song each for metal, classical, blues, k-pop, and bossa nova, users who prefer those genres get one good match and then fall back to generic energy similarity for spots #2–5. The pop/lofi over-representation means those users are served better.

**No personalisation over time**: The system does not track what the user has already heard, skipped, or loved. It gives identical results every time for the same profile, which would feel repetitive in a real app.

**No diversity enforcement**: The same artist or the same genre can occupy all five top spots. A real recommender would inject variety to prevent the list from feeling like a single-artist playlist.

**Cold-start is the only mode**: Every user is treated as brand new. There is no mechanism to incorporate listening history even if it were available.

---

## 7. Evaluation

Four distinct user profiles were tested:

| Profile | Expected top result | Actual top result | Match? |
|---|---|---|---|
| High-Energy Pop Fan | A pop/happy/high-energy song | Sunrise City (pop, happy, 0.82 energy) | Yes |
| Chill Lofi Studier | A lofi/chill/low-energy song | Midnight Coding (lofi, chill, 0.42 energy) | Yes |
| Deep Metal Head | A metal/aggressive/high-energy song | Iron Fist Rising (metal, aggressive, 0.97 energy) | Yes |
| Soulful R&B Listener | An r&b/warm song | Golden Hour (r&b, warm, 0.65 energy) | Yes |

**What was surprising**:

1. For the Metal Head profile, spots #2–5 were filled by EDM, rock, and pop tracks — not because they were musically similar to metal, but purely because they had high energy. The genre score dominated #1, but after that the system had no real understanding of the metal aesthetic.

2. The adversarial profile (`energy: 0.9, mood: "sad"`) never awarded a mood bonus to any song because "sad" does not appear in the catalog. The system silently fell back to an energy-only ranking, which could mislead a user into thinking their mood preference was being respected.

3. When the weight experiment doubled energy importance, "Ipanema Dreams" (bossa nova, 0.38 energy) ranked #1 for the Lofi Studier — perfectly matching on energy but completely wrong on genre and mood. This showed how sensitive the results are to weight choices.

**Tests run**:
```
pytest tests/test_recommender.py
2 passed in 0.05s
```
- `test_recommend_returns_songs_sorted_by_score` — verifies the pop/happy song ranks above a lofi/chill song for a pop/happy user profile.
- `test_explain_recommendation_returns_non_empty_string` — verifies that `explain_recommendation` always returns a non-empty string.

---

## 8. Future Work

1. **Fuzzy genre and mood matching**: Instead of exact string comparison, build a similarity map so that "chill" and "relaxed" share partial credit, and "indie pop" gets some points when the preference is "pop." This alone would dramatically improve the diversity of results.

2. **Listening history and feedback loop**: Track which songs the user played all the way through vs skipped. Update their profile weights accordingly — if they always skip high-energy pop, reduce that weight over time. This turns the static system into an adaptive one.

3. **Diversity penalty**: After scoring, apply a rule that penalises a song if its artist or genre already appears in the current top-k list. This prevents the recommender from suggesting five songs by the same artist and forces more variety.

4. **Audio feature extraction**: Replace manually assigned attribute values with features computed from real audio (using a library like `librosa`). This would make the energy, acousticness, and valence values objective rather than hand-written.

5. **Larger and more balanced catalog**: Increase the dataset to at least 200–500 songs with equal representation across genres so that users outside pop/lofi receive equally competitive recommendation pools.

---

## 9. Personal Reflection

Building VibeFinder 1.0 made the abstract concept of "content-based filtering" very concrete. Before this project, I thought of recommendation systems as mysterious black boxes. Implementing the scoring function revealed that at their core, they are just carefully weighted math — a formalised version of "does this song match what you told me you like?"

The biggest surprise was how quickly a small bias in the weights or the dataset creates a visible skew in the output. The catalog has three lofi songs and one metal song. That structural imbalance shows up immediately in the quality of recommendations for different profile types. It is a small-scale version of the same problem that real platforms face: genres with fewer catalogue entries get systematically worse coverage, which can affect entire communities of listeners.

Using AI tools (Claude) to generate the expanded song catalog was useful for producing varied data quickly, but I had to critically review each generated song to make sure the attribute values were internally consistent (a "classical/melancholic/low-energy" track should not have danceability 0.9, for example). The AI was a fast drafting tool, not a substitute for domain judgement.

The part that still feels like it requires the most human judgement is the weight assignment. There is no formula for deciding whether genre should be worth 2.0 or 3.0 points relative to mood. That decision encodes a cultural assumption about how music taste works — and different communities would legitimately make different choices.
