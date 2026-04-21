"""
Indian Agricultural Weed Treatment System
Specialized for wheat cultivation with region-specific recommendations
"""

WEED_TREATMENTS = {
    "phalaris_minor": {
        "common_name": "Phalaris Minor / Guli Danda",
        "description": "Most destructive wheat weed in India, causes 25-40% yield loss",
        "herbicides": [
            {"name": "Clodinafop-propargyl 15% WP", "brand": "Topik", "dosage": "160g/acre", "timing": "30-35 DAS"},
            {"name": "Fenoxaprop-p-ethyl 9.3% EC", "brand": "Puma Super", "dosage": "400ml/acre", "timing": "25-30 DAS"},
            {"name": "Isoproturon 75% WP", "brand": "Arelon", "dosage": "1kg/acre", "timing": "30-40 DAS"}
        ],
        "manual": "Hand pull before seeding stage. Use wheel hoe for large fields.",
        "prevention": "Use certified weed-free seeds. Crop rotation with mustard.",
        "cost_per_acre": "Rs. 800-1200",
        "yield_loss_if_untreated": "25-40%"
    },
    "chenopodium": {
        "common_name": "Chenopodium / Bathua",
        "description": "Broad leaf weed, competes heavily for nutrients in wheat",
        "herbicides": [
            {"name": "Metsulfuron-methyl 20% WP", "brand": "Algrip", "dosage": "8g/acre", "timing": "30-40 DAS"},
            {"name": "2,4-D Amine Salt 58% SL", "brand": "Fernoxone", "dosage": "500ml/acre", "timing": "30-35 DAS"},
            {"name": "Carfentrazone-ethyl 40% DF", "brand": "Affinity", "dosage": "20g/acre", "timing": "35-40 DAS"}
        ],
        "manual": "Remove before flowering to prevent seed spread",
        "prevention": "Deep summer plowing, use clean irrigation water",
        "cost_per_acre": "Rs. 400-600",
        "yield_loss_if_untreated": "15-25%"
    },
    "wild_oat": {
        "common_name": "Wild Oat / Jangli Jai",
        "description": "Grassy weed resembling wheat, very hard to distinguish manually",
        "herbicides": [
            {"name": "Fenoxaprop-p-ethyl 9.3% EC", "brand": "Puma Super", "dosage": "400ml/acre", "timing": "25-35 DAS"},
            {"name": "Clodinafop + Metsulfuron (Combo)", "brand": "Clodex Plus", "dosage": "160g/acre", "timing": "30-35 DAS"}
        ],
        "manual": "Uproot before ear emergence. Burn removed plants.",
        "prevention": "Avoid using farm equipment from infested fields without cleaning",
        "cost_per_acre": "Rs. 600-900",
        "yield_loss_if_untreated": "20-30%"
    },
    "rumex": {
        "common_name": "Rumex / Jangli Palak",
        "description": "Broad leaf perennial weed with deep roots",
        "herbicides": [
            {"name": "2,4-D Amine Salt 58% SL", "brand": "Fernoxone", "dosage": "600ml/acre", "timing": "35-45 DAS"},
            {"name": "Metsulfuron-methyl 20% WP", "brand": "Algrip", "dosage": "10g/acre", "timing": "35-40 DAS"}
        ],
        "manual": "Dig out entire root system. Partial removal causes regrowth.",
        "prevention": "Avoid waterlogging, maintain proper field drainage",
        "cost_per_acre": "Rs. 500-700",
        "yield_loss_if_untreated": "10-20%"
    },
    "general_weed": {
        "common_name": "General Weed",
        "description": "Unidentified weed species detected in wheat field",
        "herbicides": [
            {"name": "Isoproturon 75% WP", "brand": "Arelon", "dosage": "1kg/acre", "timing": "30-40 DAS"},
            {"name": "Sulfosulfuron 75% WG", "brand": "Leader", "dosage": "13.5g/acre", "timing": "30-35 DAS"}
        ],
        "manual": "Scout field and identify species before treatment",
        "prevention": "Consult local Krishi Vigyan Kendra (KVK) for identification",
        "cost_per_acre": "Rs. 600-1000",
        "yield_loss_if_untreated": "15-35%"
    }
}


def get_weed_treatment(weed_type, confidence):
    """
    Match weed_type to closest key in WEED_TREATMENTS.
    If no match found, use "general_weed" as fallback.
    """
    # Normalize the input
    weed_key = weed_type.lower().strip()
    
    # Direct match
    if weed_key in WEED_TREATMENTS:
        return WEED_TREATMENTS[weed_key]
    
    # Try fuzzy matching for common variations
    for key in WEED_TREATMENTS.keys():
        if key in weed_key or weed_key in key:
            return WEED_TREATMENTS[key]
    
    # Fallback to general weed
    return WEED_TREATMENTS["general_weed"]


def get_severity(confidence):
    """
    Determine severity level and urgency based on confidence score.
    Returns: (severity_level, color, urgency_message)
    """
    if confidence < 0.50:
        return "LOW", "yellow", "Monitor field every 3-4 days"
    elif confidence < 0.75:
        return "MEDIUM", "orange", "Apply treatment within 3-5 days"
    else:
        return "HIGH", "red", "Immediate treatment required within 24 hours"


def format_recommendation(weed_type, confidence):
    """
    Format complete recommendation for display in UI.
    Returns dictionary with all treatment information.
    """
    treatment = get_weed_treatment(weed_type, confidence)
    severity, color, urgency = get_severity(confidence)
    
    return {
        "weed_name": treatment["common_name"],
        "severity": severity,
        "color": color,
        "urgency": urgency,
        "description": treatment["description"],
        "primary_herbicide": treatment["herbicides"][0],
        "all_herbicides": treatment["herbicides"],
        "manual_control": treatment["manual"],
        "prevention": treatment["prevention"],
        "cost_per_acre": treatment["cost_per_acre"],
        "yield_loss": treatment["yield_loss_if_untreated"]
    }


def get_recommendation(weed_type, confidence=0.8):
    """
    Legacy function for backward compatibility.
    Returns formatted recommendation data compatible with app.py.
    """
    rec = format_recommendation(weed_type, confidence)
    
    # Map to app.py expected format
    return {
        "severity": rec["severity"],
        "confidence_range": f"{confidence*100:.0f}%-{(confidence+0.1)*100:.0f}%" if confidence < 1 else "80%-100%",
        "action": f"Treat with {rec['primary_herbicide']['name']}" if rec.get("primary_herbicide") else "Monitor field",
        "description": rec["description"],
        "methods": [rec["manual_control"], rec["prevention"]],
        "herbicides": [h["name"] for h in rec.get("all_herbicides", [])],
        "urgency": rec["urgency"],
        "cost_impact": rec["cost_per_acre"]
    }
