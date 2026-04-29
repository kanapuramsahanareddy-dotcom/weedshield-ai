"""
Indian Agricultural Weed Treatment System
Specialized for wheat cultivation with region-specific recommendations
Fully multilingual support: English, Telugu, Hindi
"""

WEED_TREATMENTS = {
    "phalaris_minor": {
        "common_name": {
            "English": "Phalaris Minor / Guli Danda",
            "Telugu (తెలుగు)": "ఫలారిస్ మైనర్ / గులి దండ",
            "Hindi (हिंदी)": "फालेरिस माइनर / गुली डंडा"
        },
        "description": {
            "English": "Most destructive wheat weed in India, causes 25-40% yield loss",
            "Telugu (తెలుగు)": "భారతదేశంలో అత్యంత హానికరమైన గోధుమ కలుపు, 25-40% దిగుబడి నష్టం కలిగిస్తుంది",
            "Hindi (हिंदी)": "भारत में सबसे हानिकारक गेहूँ का खरपतवार, 25-40% उपज हानि करता है"
        },
        "manual": {
            "English": "Hand pull before seeding stage. Use wheel hoe for large fields.",
            "Telugu (తెలుగు)": "విత్తన దశకు ముందే చేతితో పీకండి. పెద్ద పొలాలకు వీల్ హో వాడండి.",
            "Hindi (हिंदी)": "बुआई से पहले हाथ से उखाड़ें। बड़े खेतों के लिए व्हील हो का उपयोग करें।"
        },
        "prevention": {
            "English": "Use certified weed-free seeds. Crop rotation with mustard.",
            "Telugu (తెలుగు)": "ధృవీకరించిన కలుపు రహిత విత్తనాలు వాడండి. ఆవాలుతో పంట మార్పిడి చేయండి.",
            "Hindi (हिंदी)": "प्रमाणित खरपतवार मुक्त बीज उपयोग करें। सरसों के साथ फसल चक्र अपनाएं।"
        },
        "herbicides": [
            {
                "name": "Clodinafop-propargyl 15% WP",
                "name_local": {
                    "English": "Clodinafop-propargyl 15% WP",
                    "Telugu (తెలుగు)": "క్లోడినాఫాప్-ప్రొపార్జిల్ 15% WP",
                    "Hindi (हिंदी)": "क्लोडिनाफॉप-प्रोपार्जिल 15% WP"
                },
                "brand": "Topik",
                "dosage": "160g/acre",
                "timing": {
                    "English": "30-35 days after sowing",
                    "Telugu (తెలుగు)": "విత్తిన 30-35 రోజులకు",
                    "Hindi (हिंदी)": "बुआई के 30-35 दिन बाद"
                }
            },
            {
                "name": "Fenoxaprop-p-ethyl 9.3% EC",
                "name_local": {
                    "English": "Fenoxaprop-p-ethyl 9.3% EC",
                    "Telugu (తెలుగు)": "ఫెనాక్సాప్రాప్-పి-ఇథైల్ 9.3% EC",
                    "Hindi (हिंदी)": "फेनोक्साप्रोप-पी-एथिल 9.3% EC"
                },
                "brand": "Puma Super",
                "dosage": "400ml/acre",
                "timing": {
                    "English": "25-30 days after sowing",
                    "Telugu (తెలుగు)": "విత్తిన 25-30 రోజులకు",
                    "Hindi (हिंदी)": "बुआई के 25-30 दिन बाद"
                }
            },
            {
                "name": "Isoproturon 75% WP",
                "name_local": {
                    "English": "Isoproturon 75% WP",
                    "Telugu (తెలుగు)": "ఐసోప్రొట్యూరాన్ 75% WP",
                    "Hindi (हिंदी)": "आइसोप्रोट्यूरॉन 75% WP"
                },
                "brand": "Arelon",
                "dosage": "1kg/acre",
                "timing": {
                    "English": "30-40 days after sowing",
                    "Telugu (తెలుగు)": "విత్తిన 30-40 రోజులకు",
                    "Hindi (हिंदी)": "बुआई के 30-40 दिन बाद"
                }
            }
        ],
        "cost_per_acre": "Rs. 800-1200",
        "yield_loss_if_untreated": "25-40%"
    },
    "chenopodium": {
        "common_name": {
            "English": "Chenopodium / Bathua",
            "Telugu (తెలుగు)": "చెనోపోడియం / బాతువా",
            "Hindi (हिंदी)": "चेनोपोडियम / बथुआ"
        },
        "description": {
            "English": "Broad leaf weed, competes heavily for nutrients in wheat",
            "Telugu (తెలుగు)": "వెడల్పాటి ఆకు కలుపు, గోధుమలో పోషకాల కోసం తీవ్రంగా పోటీ పడుతుంది",
            "Hindi (हिंदी)": "चौड़ी पत्ती वाला खरपतवार, गेहूँ में पोषक तत्वों के लिए कड़ी प्रतिस्पर्धा करता है"
        },
        "manual": {
            "English": "Remove before flowering to prevent seed spread",
            "Telugu (తెలుగు)": "విత్తనాల వ్యాప్తిని నివారించడానికి పూత దశకు ముందే తొలగించండి",
            "Hindi (हिंदी)": "बीज फैलने से रोकने के लिए फूल आने से पहले हटाएं"
        },
        "prevention": {
            "English": "Deep summer plowing, use clean irrigation water",
            "Telugu (తెలుగు)": "వేసవిలో లోతుగా దున్నండి, శుద్ధమైన నీటిపారుదల నీరు వాడండి",
            "Hindi (हिंदी)": "गहरी गर्मियों की जुताई करें, साफ सिंचाई जल उपयोग करें"
        },
        "herbicides": [
            {
                "name": "Metsulfuron-methyl 20% WP",
                "name_local": {
                    "English": "Metsulfuron-methyl 20% WP",
                    "Telugu (తెలుగు)": "మెట్సల్ఫ్యూరాన్-మిథైల్ 20% WP",
                    "Hindi (हिंदी)": "मेट्सल्फ्यूरॉन-मिथाइल 20% WP"
                },
                "brand": "Algrip",
                "dosage": "8g/acre",
                "timing": {
                    "English": "30-40 days after sowing",
                    "Telugu (తెలుగు)": "విత్తిన 30-40 రోజులకు",
                    "Hindi (हिंदी)": "बुआई के 30-40 दिन बाद"
                }
            },
            {
                "name": "2,4-D Amine Salt 58% SL",
                "name_local": {
                    "English": "2,4-D Amine Salt 58% SL",
                    "Telugu (తెలుగు)": "2,4-డి అమైన్ సాల్ట్ 58% SL",
                    "Hindi (हिंदी)": "2,4-डी अमाइन साल्ट 58% SL"
                },
                "brand": "Fernoxone",
                "dosage": "500ml/acre",
                "timing": {
                    "English": "30-35 days after sowing",
                    "Telugu (తెలుగు)": "విత్తిన 30-35 రోజులకు",
                    "Hindi (हिंदी)": "बुआई के 30-35 दिन बाद"
                }
            },
            {
                "name": "Carfentrazone-ethyl 40% DF",
                "name_local": {
                    "English": "Carfentrazone-ethyl 40% DF",
                    "Telugu (తెలుగు)": "కార్ఫెంట్రాజోన్-ఇథైల్ 40% DF",
                    "Hindi (हिंदी)": "कार्फेंट्राजोन-एथिल 40% DF"
                },
                "brand": "Affinity",
                "dosage": "20g/acre",
                "timing": {
                    "English": "35-40 days after sowing",
                    "Telugu (తెలుగు)": "విత్తిన 35-40 రోజులకు",
                    "Hindi (हिंदी)": "बुआई के 35-40 दिन बाद"
                }
            }
        ],
        "cost_per_acre": "Rs. 400-600",
        "yield_loss_if_untreated": "15-25%"
    },
    "wild_oat": {
        "common_name": {
            "English": "Wild Oat / Jangli Jai",
            "Telugu (తెలుగు)": "అడవి వోట్స్ / జంగ్లీ జై",
            "Hindi (हिंदी)": "जंगली जई / जंगली जाई"
        },
        "description": {
            "English": "Grassy weed resembling wheat, very hard to distinguish manually",
            "Telugu (తెలుగు)": "గోధుమను పోలిన గడ్డి కలుపు, చేతితో గుర్తించడం చాలా కష్టం",
            "Hindi (हिंदी)": "गेहूँ जैसा दिखने वाला घासदार खरपतवार, हाथ से पहचानना बहुत मुश्किल"
        },
        "manual": {
            "English": "Uproot before ear emergence. Burn removed plants.",
            "Telugu (తెలుగు)": "కంకి రాకముందే పీకండి. తీసిన మొక్కలను తగులబెట్టండి.",
            "Hindi (हिंदी)": "बाली निकलने से पहले उखाड़ें। निकाले गए पौधों को जलाएं।"
        },
        "prevention": {
            "English": "Avoid using farm equipment from infested fields without cleaning",
            "Telugu (తెలుగు)": "శుభ్రం చేయకుండా సోకిన పొలాల పరికరాలు వాడవద్దు",
            "Hindi (हिंदी)": "बिना सफाई के संक्रमित खेतों के उपकरण उपयोग न करें"
        },
        "herbicides": [
            {
                "name": "Fenoxaprop-p-ethyl 9.3% EC",
                "name_local": {
                    "English": "Fenoxaprop-p-ethyl 9.3% EC",
                    "Telugu (తెలుగు)": "ఫెనాక్సాప్రాప్-పి-ఇథైల్ 9.3% EC",
                    "Hindi (हिंदी)": "फेनोक्साप्रोप-पी-एथिल 9.3% EC"
                },
                "brand": "Puma Super",
                "dosage": "400ml/acre",
                "timing": {
                    "English": "25-35 days after sowing",
                    "Telugu (తెలుగు)": "విత్తిన 25-35 రోజులకు",
                    "Hindi (हिंदी)": "बुआई के 25-35 दिन बाद"
                }
            },
            {
                "name": "Clodinafop + Metsulfuron",
                "name_local": {
                    "English": "Clodinafop + Metsulfuron",
                    "Telugu (తెలుగు)": "క్లోడినాఫాప్ + మెట్సల్ఫ్యూరాన్",
                    "Hindi (हिंदी)": "क्लोडिनाफॉप + मेट्सल्फ्यूरॉन"
                },
                "brand": "Clodex Plus",
                "dosage": "160g/acre",
                "timing": {
                    "English": "30-35 days after sowing",
                    "Telugu (తెలుగు)": "విత్తిన 30-35 రోజులకు",
                    "Hindi (हिंदी)": "बुआई के 30-35 दिन बाद"
                }
            }
        ],
        "cost_per_acre": "Rs. 600-900",
        "yield_loss_if_untreated": "20-30%"
    },
    "rumex": {
        "common_name": {
            "English": "Rumex / Jangli Palak",
            "Telugu (తెలుగు)": "రూమెక్స్ / జంగ్లీ పాలక్",
            "Hindi (हिंदी)": "रूमेक्स / जंगली पालक"
        },
        "description": {
            "English": "Broad leaf perennial weed with deep roots",
            "Telugu (తెలుగు)": "లోతైన వేళ్ళు గల వెడల్పాటి ఆకు బహువార్షిక కలుపు",
            "Hindi (हिंदी)": "गहरी जड़ों वाला चौड़ी पत्ती का बारहमासी खरपतवार"
        },
        "manual": {
            "English": "Dig out entire root system. Partial removal causes regrowth.",
            "Telugu (తెలుగు)": "మొత్తం వేరు వ్యవస్థను తవ్వి తీయండి. పాక్షిక తొలగింపు మళ్ళీ మొలకెత్తిస్తుంది.",
            "Hindi (हिंदी)": "पूरी जड़ प्रणाली खोदकर निकालें। आंशिक निराई से दोबारा उगता है।"
        },
        "prevention": {
            "English": "Avoid waterlogging, maintain proper field drainage",
            "Telugu (తెలుగు)": "నీరు నిల్వ ఉండకుండా చేయండి, సరైన పొలం నీకాసు నిర్వహించండి",
            "Hindi (हिंदी)": "जलभराव से बचें, उचित खेत जल निकासी बनाए रखें"
        },
        "herbicides": [
            {
                "name": "2,4-D Amine Salt 58% SL",
                "name_local": {
                    "English": "2,4-D Amine Salt 58% SL",
                    "Telugu (తెలుగు)": "2,4-డి అమైన్ సాల్ట్ 58% SL",
                    "Hindi (हिंदी)": "2,4-डी अमाइन साल्ट 58% SL"
                },
                "brand": "Fernoxone",
                "dosage": "600ml/acre",
                "timing": {
                    "English": "35-45 days after sowing",
                    "Telugu (తెలుగు)": "విత్తిన 35-45 రోజులకు",
                    "Hindi (हिंदी)": "बुआई के 35-45 दिन बाद"
                }
            },
            {
                "name": "Metsulfuron-methyl 20% WP",
                "name_local": {
                    "English": "Metsulfuron-methyl 20% WP",
                    "Telugu (తెలుగు)": "మెట్సల్ఫ్యూరాన్-మిథైల్ 20% WP",
                    "Hindi (हिंदी)": "मेट्सल्फ्यूरॉन-मिथाइल 20% WP"
                },
                "brand": "Algrip",
                "dosage": "10g/acre",
                "timing": {
                    "English": "35-40 days after sowing",
                    "Telugu (తెలుగు)": "విత్తిన 35-40 రోజులకు",
                    "Hindi (हिंदी)": "बुआई के 35-40 दिन बाद"
                }
            }
        ],
        "cost_per_acre": "Rs. 500-700",
        "yield_loss_if_untreated": "10-20%"
    },
    "general_weed": {
        "common_name": {
            "English": "General Weed",
            "Telugu (తెలుగు)": "సాధారణ కలుపు మొక్క",
            "Hindi (हिंदी)": "सामान्य खरपतवार"
        },
        "description": {
            "English": "Unidentified weed species detected in wheat field",
            "Telugu (తెలుగు)": "గోధుమ పొలంలో గుర్తించబడని కలుపు జాతి కనుగొనబడింది",
            "Hindi (हिंदी)": "गेहूँ के खेत में अज्ञात खरपतवार प्रजाति पाई गई"
        },
        "manual": {
            "English": "Scout field and identify species before treatment",
            "Telugu (తెలుగు)": "చికిత్సకు ముందు పొలాన్ని పరిశీలించి జాతిని గుర్తించండి",
            "Hindi (हिंदी)": "उपचार से पहले खेत का निरीक्षण करें और प्रजाति की पहचान करें"
        },
        "prevention": {
            "English": "Consult local Krishi Vigyan Kendra (KVK) for identification",
            "Telugu (తెలుగు)": "గుర్తింపు కోసం స్థానిక కృషి విజ్ఞాన కేంద్రం (KVK) సంప్రదించండి",
            "Hindi (हिंदी)": "पहचान के लिए स्थानीय कृषि विज्ञान केंद्र (KVK) से संपर्क करें"
        },
        "herbicides": [
            {
                "name": "Isoproturon 75% WP",
                "name_local": {
                    "English": "Isoproturon 75% WP",
                    "Telugu (తెలుగు)": "ఐసోప్రొట్యూరాన్ 75% WP",
                    "Hindi (हिंदी)": "आइसोप्रोट्यूरॉन 75% WP"
                },
                "brand": "Arelon",
                "dosage": "1kg/acre",
                "timing": {
                    "English": "30-40 days after sowing",
                    "Telugu (తెలుగు)": "విత్తిన 30-40 రోజులకు",
                    "Hindi (हिंदी)": "बुआई के 30-40 दिन बाद"
                }
            },
            {
                "name": "Sulfosulfuron 75% WG",
                "name_local": {
                    "English": "Sulfosulfuron 75% WG",
                    "Telugu (తెలుగు)": "సల్ఫోసల్ఫ్యూరాన్ 75% WG",
                    "Hindi (हिंदी)": "सल्फोसल्फ्यूरॉन 75% WG"
                },
                "brand": "Leader",
                "dosage": "13.5g/acre",
                "timing": {
                    "English": "30-35 days after sowing",
                    "Telugu (తెలుగు)": "విత్తిన 30-35 రోజులకు",
                    "Hindi (हिंदी)": "बुआई के 30-35 दिन बाद"
                }
            }
        ],
        "cost_per_acre": "Rs. 600-1000",
        "yield_loss_if_untreated": "15-35%"
    }
}


def get_weed_treatment(weed_type, confidence, language="English"):
    """
    Match weed_type to closest key in WEED_TREATMENTS.
    If no match found, use "general_weed" as fallback.
    Returns treatment data in the specified language.
    """
    # Normalize the input
    weed_key = weed_type.lower().strip()
    
    # Direct match
    if weed_key not in WEED_TREATMENTS:
        # Try fuzzy matching for common variations
        found = False
        for key in WEED_TREATMENTS.keys():
            if key in weed_key or weed_key in key:
                weed_key = key
                found = True
                break
        if not found:
            weed_key = "general_weed"
    
    treatment = WEED_TREATMENTS[weed_key]
    lang = language if language in ["English", "Telugu (తెలుగు)", "Hindi (हिंदी)"] else "English"
    
    return {
        "common_name": treatment["common_name"][lang],
        "description": treatment["description"][lang],
        "manual": treatment["manual"][lang],
        "prevention": treatment["prevention"][lang],
        "herbicides": [
            {
                "name": h["name_local"][lang],
                "brand": h["brand"],
                "dosage": h["dosage"],
                "timing": h["timing"][lang]
            }
            for h in treatment["herbicides"]
        ],
        "cost_per_acre": treatment["cost_per_acre"],
        "yield_loss_if_untreated": treatment["yield_loss_if_untreated"]
    }


def get_severity(confidence, language="English"):
    """
    Determine severity level and urgency based on confidence score.
    Returns: (severity_level, text_color, bg_color, urgency_message)
    """
    SEVERITY_TEXT = {
        "English": {
            "LOW": ("LOW", "#558b2f", "#f1f8e9", "Monitor field every 3-4 days"),
            "MEDIUM": ("MEDIUM", "#e65100", "#fff3e0", "Apply treatment within 3-5 days"),
            "HIGH": ("HIGH", "#c62828", "#ffebee", "Immediate treatment within 24 hours")
        },
        "Telugu (తెలుగు)": {
            "LOW": ("తక్కువ", "#558b2f", "#f1f8e9", "ప్రతి 3-4 రోజులకు పొలాన్ని పర్యవేక్షించండి"),
            "MEDIUM": ("మధ్యస్థం", "#e65100", "#fff3e0", "3-5 రోజుల్లో చికిత్స చేయండి"),
            "HIGH": ("అధిక", "#c62828", "#ffebee", "24 గంటల్లో వెంటనే చికిత్స అవసరం")
        },
        "Hindi (हिंदी)": {
            "LOW": ("कम", "#558b2f", "#f1f8e9", "हर 3-4 दिन में खेत की निगरानी करें"),
            "MEDIUM": ("मध्यम", "#e65100", "#fff3e0", "3-5 दिनों में उपचार करें"),
            "HIGH": ("उच्च", "#c62828", "#ffebee", "24 घंटे में तुरंत उपचार करें")
        }
    }
    lang_data = SEVERITY_TEXT.get(language, SEVERITY_TEXT["English"])
    if confidence < 0.50:
        return lang_data["LOW"]
    elif confidence < 0.75:
        return lang_data["MEDIUM"]
    else:
        return lang_data["HIGH"]


def format_recommendation(weed_type, confidence, language="English"):
    """
    Format complete recommendation for display in UI.
    Returns dictionary with all treatment information in specified language.
    """
    treatment = get_weed_treatment(weed_type, confidence, language)
    severity_text, color, bg_color, urgency = get_severity(confidence, language)
    
    ACTION_TEMPLATE = {
        "English": f"Treat with {treatment['herbicides'][0]['name']}",
        "Telugu (తెలుగు)": f"{treatment['herbicides'][0]['name']} తో చికిత్స చేయండి",
        "Hindi (हिंदी)": f"{treatment['herbicides'][0]['name']} से उपचार करें"
    }
    action = ACTION_TEMPLATE.get(language, ACTION_TEMPLATE["English"])
    
    return {
        "weed_name": treatment["common_name"],
        "severity": severity_text,
        "color": color,
        "bg_color": bg_color,
        "urgency": urgency,
        "action": action,
        "description": treatment["description"],
        "primary_herbicide": treatment["herbicides"][0],
        "all_herbicides": treatment["herbicides"],
        "manual_control": treatment["manual"],
        "prevention": treatment["prevention"],
        "cost_per_acre": treatment["cost_per_acre"],
        "yield_loss": treatment["yield_loss_if_untreated"]
    }


def get_recommendation(weed_type, confidence=0.8, language="English"):
    """
    Legacy function for backward compatibility.
    Returns formatted recommendation data compatible with app.py.
    """
    rec = format_recommendation(weed_type, confidence, language)
    
    # Map to app.py expected format
    return {
        "severity": rec["severity"],
        "color": rec["color"],
        "bg_color": rec["bg_color"],
        "confidence_range": f"{confidence*100:.0f}%-{(confidence+0.1)*100:.0f}%" if confidence < 1 else "80%-100%",
        "action": rec["action"],
        "description": rec["description"],
        "manual_control": rec["manual_control"],
        "prevention": rec["prevention"],
        "methods": [rec["manual_control"], rec["prevention"]],
        "herbicides": [h["name"] for h in rec.get("all_herbicides", [])],
        "all_herbicides": rec["all_herbicides"],
        "urgency": rec["urgency"],
        "cost_impact": rec["cost_per_acre"],
        "yield_loss": rec["yield_loss"]
    }
