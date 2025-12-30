#!/usr/bin/env python3
"""
Common Misspelling Corrector for EnMS Chatbot
Provides fuzzy matching for common energy management terms
"""

# Common misspellings dictionary
COMMON_MISSPELLINGS = {
    # Energy terms
    "eneregy": "energy",
    "enery": "energy",
    "energey": "energy",
    
    # Anomaly variants
    "anaomaly": "anomaly",
    "anomoly": "anomaly",
    "anamoly": "anomaly",
    "annomaly": "anomaly",
    
    # Efficiency
    "eficiency": "efficiency",
    "efficency": "efficiency",
    "efficiancy": "efficiency",
    
    # Baseline
    "basline": "baseline",
    "baseeline": "baseline",
    "baselne": "baseline",
    
    # Forecast
    "forcast": "forecast",
    "forcaste": "forecast",
    
    # Dashboard
    "dashbord": "dashboard",
    "dashbaord": "dashboard",
    
    # Monitoring
    "monitering": "monitoring",
    "moniterring": "monitoring",
    
    # Equipment
    "equipement": "equipment",
    "equiptment": "equipment",
    
    # Performance
    "performace": "performance",
    "preformance": "performance",
    
    # Consumption
    "consuption": "consumption",
    "consumtion": "consumption",
    
    # Maintenance
    "maintainance": "maintenance",
    "maintenence": "maintenance",
    
    # Analysis
    "analisis": "analysis",
    "analysys": "analysis",
    
    # Temperature
    "temperture": "temperature",
    "temprature": "temperature",
    
    # Environment
    "enviroment": "environment",
    "enviornment": "environment",
}


def correct_misspellings(text: str) -> tuple[str, list]:
    """
    Correct common misspellings in text
    
    Args:
        text: Input text with potential misspellings
        
    Returns:
        tuple: (corrected_text, list_of_corrections_made)
    """
    corrected = text.lower()
    corrections_made = []
    
    for misspell, correct in COMMON_MISSPELLINGS.items():
        if misspell in corrected:
            corrected = corrected.replace(misspell, correct)
            corrections_made.append(f"{misspell} → {correct}")
    
    return corrected, corrections_made


def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate Levenshtein distance between two strings"""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Cost of insertions, deletions, or substitutions
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def find_closest_match(word: str, candidates: list, threshold: int = 2) -> str:
    """
    Find closest matching word from candidates using Levenshtein distance
    
    Args:
        word: Word to match
        candidates: List of candidate words
        threshold: Maximum distance to consider a match (default: 2)
        
    Returns:
        Closest matching word or original word if no match within threshold
    """
    if not candidates:
        return word
    
    min_distance = float('inf')
    closest = word
    
    for candidate in candidates:
        distance = levenshtein_distance(word.lower(), candidate.lower())
        if distance < min_distance:
            min_distance = distance
            closest = candidate
    
    if min_distance <= threshold:
        return closest
    
    return word


if __name__ == "__main__":
    # Test the corrector
    test_phrases = [
        "What is eneregy baseline?",
        "Show me anaomaly detection",
        "What is the eficiency?",
        "How to check monitering?",
        "Explain forcast model",
    ]
    
    print("Testing Misspelling Corrector")
    print("=" * 60)
    
    for phrase in test_phrases:
        corrected, corrections = correct_misspellings(phrase)
        if corrections:
            print(f"Original:  {phrase}")
            print(f"Corrected: {corrected}")
            print(f"Changes:   {', '.join(corrections)}")
            print()
        else:
            print(f"✅ No errors: {phrase}")
            print()
