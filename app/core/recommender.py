"""
Vehicle Recommendation Engine

Logic:
- Parse user intent to extract needs (family, towing, fuel-efficient, sport, etc.)
- Score each vehicle against extracted attributes
- Return top 2 with detailed reasoning

This is rule-based attribute matching, not LLM guessing —
ensures factual, explainable recommendations.
"""

from typing import List, Dict, Tuple
from app.data.vehicles import VEHICLES


# Intent keyword → attribute mapping
INTENT_MAP = {
    # Family / passengers
    "family": {"seating_capacity": 5, "tags": ["family", "suv", "safety"]},
    "kids": {"seating_capacity": 5, "tags": ["family", "suv"]},
    "7 seat": {"seating_capacity": 7, "tags": ["7-seat"]},
    "seven seat": {"seating_capacity": 7, "tags": ["7-seat"]},
    "passengers": {"seating_capacity": 5},
    "road trip": {"tags": ["suv", "comfort", "family"]},

    # Towing / hauling
    "tow": {"tags": ["towing", "truck"]},
    "towing": {"tags": ["towing", "truck"]},
    "haul": {"tags": ["hauling", "truck"]},
    "truck": {"tags": ["truck", "pickup"]},
    "pickup": {"tags": ["truck", "pickup"]},
    "cargo": {"tags": ["truck", "cargo"]},
    "work": {"tags": ["truck", "work"]},

    # Performance / sport
    "sport": {"tags": ["sport", "performance"]},
    "fast": {"tags": ["performance", "sport"]},
    "performance": {"tags": ["performance", "sport"]},
    "v8": {"tags": ["v8", "performance"]},
    "manual": {"tags": ["manual", "sport"]},

    # Fuel efficiency / eco
    "fuel": {"tags": ["fuel-efficient", "eco"]},
    "efficient": {"tags": ["fuel-efficient", "eco"]},
    "mpg": {"tags": ["fuel-efficient", "eco"]},
    "hybrid": {"tags": ["hybrid", "phev", "eco"]},
    "electric": {"tags": ["phev", "hybrid"]},
    "commut": {"tags": ["fuel-efficient", "compact", "eco"]},
    "city": {"tags": ["compact", "fuel-efficient"]},

    # SUV / crossover
    "suv": {"tags": ["suv", "crossover"]},
    "crossover": {"tags": ["crossover", "suv"]},
    "off-road": {"tags": ["offroad", "4wd"]},
    "off road": {"tags": ["offroad", "4wd"]},
    "adventure": {"tags": ["offroad", "4wd", "truck"]},
}

# Vehicle → tags mapping for scoring
VEHICLE_TAGS = {
    "ford f-150": ["truck", "pickup", "towing", "hauling", "work", "4wd", "offroad", "cargo", "family"],
    "ford mustang": ["sport", "performance", "v8", "manual", "coupe", "fast"],
    "ford explorer": ["suv", "family", "7-seat", "comfort", "3-row", "towing", "4wd"],
    "ford escape": ["suv", "crossover", "compact", "fuel-efficient", "eco", "hybrid", "phev", "city", "commuter"],
    "ford ranger": ["truck", "pickup", "towing", "4wd", "offroad", "midsize", "adventure", "work"],
}


def _extract_tags(query: str) -> Tuple[List[str], int]:
    """Extract semantic tags and minimum seating from natural language query."""
    query_lower = query.lower()
    tags = []
    min_seating = 0

    for keyword, attributes in INTENT_MAP.items():
        if keyword in query_lower:
            tags.extend(attributes.get("tags", []))
            if "seating_capacity" in attributes:
                min_seating = max(min_seating, attributes["seating_capacity"])

    return list(set(tags)), min_seating


def _score_vehicle(vehicle: Dict, tags: List[str], min_seating: int) -> Tuple[float, List[str]]:
    """Score a vehicle against extracted requirements. Returns (score, reasons)."""
    model_name = vehicle["model"].lower()
    vehicle_tags = VEHICLE_TAGS.get(model_name, [])
    reasons = []
    score = 0.0

    # Tag matching (each matched tag = +1)
    matched_tags = set(tags) & set(vehicle_tags)
    score += len(matched_tags) * 1.0
    if matched_tags:
        reasons.append(f"Matches your needs: {', '.join(sorted(matched_tags))}")

    # Seating requirement
    if min_seating > 0:
        if vehicle["seating_capacity"] >= min_seating:
            score += 2.0
            reasons.append(f"Has {vehicle['seating_capacity']} seats (you need {min_seating}+)")
        else:
            score -= 3.0  # Hard penalize if seating not met
            reasons.append(f"Only {vehicle['seating_capacity']} seats — does not meet requirement")

    # Bonus: if no tags matched but query mentions SUV and vehicle is SUV category
    if not matched_tags and "suv" in vehicle.get("category", ""):
        if "suv" in tags or "crossover" in tags:
            score += 0.5

    return score, reasons


def recommend_vehicles(query: str) -> Dict:
    """
    Match user query to top 2 best-fit Ford vehicles.
    
    Algorithm:
    1. Extract intent tags from natural language
    2. Score each vehicle against those tags
    3. Apply hard constraints (seating, etc.)
    4. Return top 2 with scoring rationale
    """
    tags, min_seating = _extract_tags(query)

    scored = []
    for vehicle in VEHICLES:
        score, reasons = _score_vehicle(vehicle, tags, min_seating)
        scored.append({
            "vehicle": vehicle,
            "score": score,
            "reasons": reasons
        })

    # Sort by score descending
    scored.sort(key=lambda x: x["score"], reverse=True)
    top2 = scored[:2]

    recommendations = []
    for rank, item in enumerate(top2, 1):
        v = item["vehicle"]
        recommendations.append({
            "rank": rank,
            "model": v["model"],
            "year": v["year"],
            "category": v["category"],
            "match_score": round(item["score"], 2),
            "why_recommended": item["reasons"] if item["reasons"] else [
                "General capability match based on Ford lineup position"
            ],
            "key_specs": {
                "engine": v["engine"],
                "seating": v["seating_capacity"],
                "towing": v["towing_capacity"],
                "fuel_economy": v["fuel_economy"],
                "price_range": v["price_range"],
                "drivetrain": v["drivetrain"]
            },
            "best_for": v["use_case"],
            "top_features": v["pros"]
        })

    return {
        "query": query,
        "detected_needs": tags,
        "min_seating_required": min_seating if min_seating > 0 else "not specified",
        "recommendations": recommendations,
        "logic_explanation": (
            "Attribute matching: query parsed for intent keywords (family, towing, sport, eco, etc.), "
            "mapped to vehicle capability tags, scored by overlap count with hard constraints "
            "applied for seating requirements. Top 2 highest-scoring vehicles returned."
        )
    }
