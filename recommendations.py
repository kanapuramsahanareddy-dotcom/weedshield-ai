# Treatment Recommendations Database
# Comprehensive treatment guidance based on weed detection confidence scores

TREATMENTS = {
    "low": {
        "severity": "LOW",
        "confidence_range": "Below 50%",
        "action": "Preventive Monitoring",
        "description": "Low weed presence detected. Scout the field manually every 3-4 days. No immediate spraying needed.",
        "methods": [
            "Manual spot removal is sufficient",
            "Monitor field every 3-4 days",
            "No herbicide needed at this stage"
        ],
        "herbicides": [],
        "urgency": "Within 2 weeks",
        "cost_impact": "Low"
    },
    "medium": {
        "severity": "MEDIUM", 
        "confidence_range": "50% to 75%",
        "action": "Localized Treatment",
        "description": "Moderate weed infestation. Apply treatment within 3-5 days before spreading.",
        "methods": [
            "Apply Clodinafop-propargyl in affected areas only",
            "Spot spray rather than full field treatment",
            "Re-check field after 7 days"
        ],
        "herbicides": ["Clodinafop-propargyl", "Fenoxaprop-p-ethyl"],
        "urgency": "Within 3-5 days",
        "cost_impact": "Medium"
    },
    "high": {
        "severity": "HIGH",
        "confidence_range": "Above 75%",
        "action": "Immediate Treatment Required",
        "description": "Heavy weed infestation detected. Immediate action needed to prevent crop yield loss.",
        "methods": [
            "Apply Isoproturon or Sulfosulfuron across full field",
            "Consult agronomist within 24 hours",
            "Follow up treatment after 10 days"
        ],
        "herbicides": ["Isoproturon", "Sulfosulfuron", "Metribuzin"],
        "urgency": "Within 24 hours",
        "cost_impact": "High"
    }
}


def get_recommendation(confidence_score):
    """
    Get treatment recommendation based on weed detection confidence score.
    
    Args:
        confidence_score (float): Confidence score between 0 and 1
        
    Returns:
        dict: Treatment recommendation with severity, action, methods, herbicides, urgency, and cost impact
    """
    if confidence_score < 0.50:
        return TREATMENTS["low"]
    elif confidence_score < 0.75:
        return TREATMENTS["medium"]
    else:
        return TREATMENTS["high"]
