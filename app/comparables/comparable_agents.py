from typing import List, Dict
from math import sqrt


def find_comparables(subject: Dict, candidates: List[Dict], top_n=5) -> List[Dict]:
    def score(p):
        score = 0
        if subject.get("zoning") and p.get("zoning") == subject["zoning"]:
            score += 2
        if subject.get("property_type") and p.get("property_type") == subject["property_type"]:
            score += 2

        # Similarity by size (square feet)
        sf1 = subject.get("square_feet")
        sf2 = p.get("square_feet")
        if sf1 and sf2:
            score += 1 / (1 + abs(sf1 - sf2) / max(sf1, sf2))

        # Similarity by year built
        y1 = subject.get("year_built")
        y2 = p.get("year_built")
        if y1 and y2:
            score += 1 / (1 + abs(y1 - y2))

        return score

    # Compute and attach scores
    for p in candidates:
        p["score"] = score(p)

    sorted_results = sorted(candidates, key=lambda x: x["score"], reverse=True)
    return sorted_results[:top_n]
