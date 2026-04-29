import io
import streamlit as st
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from recommendations import format_recommendation


# Translations Dictionary
TRANSLATIONS = {
    "English": {
        "title": "WeedShield AI",
        "subtitle": "Weed Detection and Prevention in Wheat Crop Using AI",
        "upload": "Upload Farm Image",
        "detect_btn": "Detect",
        "weed_detected": "⚠️ WEED DETECTED",
        "no_weed": "✅ NO WEED FOUND",
        "confidence": "Confidence",
        "treatment": "Treatment Recommendations",
        "severity": "Severity Level",
        "action": "Action",
        "urgency": "Urgency",
        "methods": "Recommended Methods",
        "herbicides": "Recommended Herbicides",
        "history": "Detection History",
        "no_history": "No detections yet",
        "clear_history": "Clear History",
        "how_to_use": "How to use",
        "step1": "📸 Take or upload a photo of your wheat field",
        "step2": "🔍 Click Detect to analyze for weeds",
        "step3": "📋 Get instant treatment recommendations",
        "download_pdf": "📥 Download Detection Report (PDF)",
        "learn_title": "Learn — Weeds in Wheat Crops",
        "tab1": "Weeds in Wheat Crops",
        "tab2": "Impact on Agriculture",
        "tab3": "Prevention Methods",
        "what_are_weeds": "What are weeds in wheat fields",
        "weeds_desc": "Weeds are non-crop plants that grow within crop stands and compete for resources. Common examples in wheat fields:",
        "weed1": "Phalaris minor (Little seed canary grass)",
        "weed2": "Avena fatua (Wild oats)",
        "weed3": "Other broadleaf and grassy weeds",
        "how_affect": "How weeds affect wheat yield:",
        "affect1": "Compete for light, water and nutrients",
        "affect2": "Reduce grain yield and quality",
        "affect3": "Increase production costs",
        "how_identify": "How to identify weeds vs wheat",
        "identify_desc": "Identify by leaf shape, growth habit and tiller structure; automated detection uses visual features learned by the model.",
        "why_early": "Why early detection is important",
        "early_desc": "Early detection enables targeted treatment, reduces herbicide use and limits yield loss.",
        "impact_title": "Impact on Agriculture",
        "impact1": "Typical crop loss from severe weed infestation: 10-30% (varies by species and timing)",
        "impact2": "Economic impact: reduced marketable yield, increased input costs, and labor",
        "farmer_challenges": "Farmer challenges include timely identification, selective application of control measures, and labor limitations.",
        "prevention_title": "Prevention Methods",
        "prev1": "Manual removal where feasible",
        "prev2": "Herbicide programs (selective and rotational use)",
        "prev3": "Cultural practices (crop rotation, competitive cultivars)",
        "ai_benefits": "AI detection benefits: fast field-scale scouting, early warning, and data-driven interventions to reduce costs and environmental impact.",
        "nav_home": "🏠 Home",
        "nav_detect": "🔍 Detect",
        "nav_learn": "📚 Learn",
        "model_ready": "✓ Model ready",
        "hero_title": "Protect Your Wheat Crop",
        "hero_subtitle": "Early detection, precise treatment, better yields",
        "quick_overview": "Quick Overview",
        "scans_today": "Scans Today",
        "weeds_found": "Weeds Found",
        "accuracy": "Accuracy",
        "how_to_use_title": "How to Use WeedShield AI",
        "step1_title": "Take Photo",
        "step1_desc": "Capture a clear image of your wheat field showing weeds or suspicious areas",
        "step2_title": "Run Detection",
        "step2_desc": "Upload the image and click Run Detection for instant AI analysis",
        "step3_title": "Get Results",
        "step3_desc": "Receive personalized treatment recommendations based on detection results",
        "season_badge": "Season: Rabi 2025",
        "latest_detection": "Latest Detection",
        "no_detections": "No detections yet",
        "field_clear": "Field Clear",
        "detection_stats": "Detection Stats",
        "wheat_label": "Wheat",
        "weeds_label": "Weeds",
        "avg_confidence": "Avg Confidence",
        "image_preview": "Image Preview",
        "upload_field_image": "📸 Upload Field Image",
        "individual_detections": "📋 Individual Detections",
        "detection_results": "Detection Results",
        "treatment_recommendations": "Treatment Recommendations",
        "weeds_found_title": "⚠️ WEEDS FOUND",
        "clear_title": "✅ CLEAR",
        "no_weeds_detected": "No weeds detected",
        "run_detection_btn": "🔍 Run Detection",
        "detect_weeds_title": "🔍 Detect Weeds",
        "learn_about_weeds": "📚 Learn About Weeds",
        "model_not_loaded": "Model not loaded",
        "cannot_run_detection": "Cannot run detection",
        "running_detection": "Running detection...",
        "detection_completed_success": "✓ Detection completed successfully",
        "detection_completed": "✓ Detection completed",
        "home_title": "🏠 Home",
        "language_label": "Language",
        "upload_btn": "Upload",
        "upload_hint": "High-resolution field images give better results",
        "upload_hint_text": "Take a clear photo of your wheat field and upload below",
        "detect_weeds": "🔍 Detect Weeds",
        "home": "Home",
        "detect": "Detect",
        "learn": "Learn"
    },
    "Telugu (తెలుగు)": {
        "title": "వీడ్‌షీల్డ్ AI",
        "subtitle": "AI ఉపయోగించి గోధుమ పంటలో కలుపు మొక్కల గుర్తింపు మరియు నివారణ",
        "upload": "వ్యవసాయ చిత్రాన్ని అప్‌లోడ్ చేయండి",
        "detect_btn": "గుర్తించు",
        "weed_detected": "⚠️ కలుపు మొక్క గుర్తించబడింది",
        "no_weed": "✅ కలుపు మొక్కలు లేవు",
        "confidence": "నమ్మకం స్కోర్",
        "treatment": "చికిత్స సిఫార్సులు",
        "severity": "తీవ్రత స్థాయి",
        "action": "చర్య",
        "urgency": "అత్యవసరత",
        "methods": "సిఫార్సు చేయబడిన పద్ధతులు",
        "herbicides": "సిఫార్సు చేయబడిన కలుపు మందులు",
        "history": "గుర్తింపు చరిత్ర",
        "no_history": "ఇంకా గుర్తింపులు లేవు",
        "clear_history": "చరిత్ర తొలగించు",
        "how_to_use": "ఎలా ఉపయోగించాలి",
        "step1": "📸 మీ గోధుమ పొలం ఫోటో తీయండి లేదా అప్‌లోడ్ చేయండి",
        "step2": "🔍 కలుపు మొక్కలను విశ్లేషించడానికి గుర్తించు నొక్కండి",
        "step3": "📋 తక్షణ చికిత్స సిఫార్సులు పొందండి",
        "download_pdf": "📥 నివేదికను డౌన్‌లోడ్ చేయండి",
        "learn_title": "నేర్చుకోండి — గోధుమ పంటలో కలుపు మొక్కలు",
        "tab1": "గోధుమ పంటలో కలుపు మొక్కలు",
        "tab2": "వ్యవసాయంపై ప్రభావం",
        "tab3": "నివారణ పద్ధతులు",
        "what_are_weeds": "గోధుమ పొలాలలో కలుపు మొక్కలు ఏమిటి",
        "weeds_desc": "కలుపు మొక్కలు పంట లేని మొక్కలు, ఇవి పంట మొక్కలతో పోటీ పడతాయి. గోధుమ పొలాలలో సాధారణ ఉదాహరణలు:",
        "weed1": "ఫలారిస్ మైనర్ (చిన్న గింజ కానరీ గడ్డి)",
        "weed2": "అవెనా ఫాటువా (అడవి వోట్స్)",
        "weed3": "ఇతర వెడల్పు ఆకు మరియు గడ్డి కలుపు మొక్కలు",
        "how_affect": "కలుపు మొక్కలు గోధుమ దిగుబడిని ఎలా ప్రభావితం చేస్తాయి:",
        "affect1": "కాంతి, నీరు మరియు పోషకాల కోసం పోటీ",
        "affect2": "ధాన్యం దిగుబడి మరియు నాణ్యతను తగ్గిస్తుంది",
        "affect3": "ఉత్పత్తి ఖర్చులు పెరుగుతాయి",
        "how_identify": "కలుపు మొక్కలు మరియు గోధుమను ఎలా గుర్తించాలి",
        "identify_desc": "ఆకు ఆకారం, పెరుగుదల అలవాటు మరియు టిల్లర్ నిర్మాణం ద్వారా గుర్తించండి.",
        "why_early": "ముందస్తు గుర్తింపు ఎందుకు ముఖ్యమైనది",
        "early_desc": "ముందస్తు గుర్తింపు లక్ష్య చికిత్సను అనుమతిస్తుంది, కలుపు మందుల వాడకాన్ని తగ్గిస్తుంది.",
        "impact_title": "వ్యవసాయంపై ప్రభావం",
        "impact1": "తీవ్రమైన కలుపు దాడి వల్ల సాధారణ పంట నష్టం: 10-30%",
        "impact2": "ఆర్థిక ప్రభావం: తగ్గిన దిగుబడి, పెరిగిన ఖర్చులు",
        "farmer_challenges": "రైతుల సవాళ్లలో సకాలంలో గుర్తింపు మరియు శ్రమ పరిమితులు ఉన్నాయి.",
        "prevention_title": "నివారణ పద్ధతులు",
        "prev1": "సాధ్యమైనచోట చేతితో తొలగింపు",
        "prev2": "కలుపు మందు కార్యక్రమాలు",
        "prev3": "సాంస్కృతిక పద్ధతులు (పంట మార్పిడి)",
        "ai_benefits": "AI గుర్తింపు ప్రయోజనాలు: వేగవంతమైన పొలం పర్యవేక్షణ మరియు ముందస్తు హెచ్చరిక.",
        "nav_home": "🏠 హోమ్",
        "nav_detect": "🔍 గుర్తించు",
        "nav_learn": "📚 నేర్చుకోండి",
        "model_ready": "✓ సిద్ధంగా ఉంది",
        "hero_title": "మీ గోధుమ పంటను రక్షించండి",
        "hero_subtitle": "ముందస్తు గుర్తింపు, ఖచ్చితమైన చికిత్స, మెరుగైన దిగుబడి",
        "quick_overview": "శీఘ్ర అవలోకనం",
        "scans_today": "నేటి స్కాన్లు",
        "weeds_found": "కలుపు మొక్కలు",
        "accuracy": "ఖచ్చితత్వం",
        "how_to_use_title": "WeedShield AI ఎలా వాడాలి",
        "step1_title": "ఫోటో తీయండి",
        "step1_desc": "మీ గోధుమ పొలం యొక్క స్పష్టమైన చిత్రాన్ని తీయండి",
        "step2_title": "గుర్తింపు నడపండి",
        "step2_desc": "చిత్రాన్ని అప్లోడ్ చేసి గుర్తింపు నడపండి",
        "step3_title": "ఫలితాలు పొందండి",
        "step3_desc": "చికిత్స సిఫార్సులు అందుకోండి",
        "season_badge": "సీజన్: రబీ 2025",
        "latest_detection": "తాజా గుర్తింపు",
        "no_detections": "ఇంకా గుర్తింపులు లేవు",
        "field_clear": "ఖాళీ ఫీల్డ్",
        "detection_stats": "గుర్తింపు గణాంకాలు",
        "wheat_label": "గోధుమ",
        "weeds_label": "కలుపు",
        "avg_confidence": "సగటు నమ్మకం",
        "image_preview": "ఇమేజ్ ప్రివ్యూ",
        "upload_field_image": "📸 ఫీల్డ్ చిత్రం అప్‌లోడ్ చేయండి",
        "individual_detections": "📋 వ్యక్తిగత గుర్తింపులు",
        "detection_results": "గుర్తింపు ఫలితాలు",
        "treatment_recommendations": "చికిత్స సిఫార్సులు",
        "weeds_found_title": "⚠️ కలుపు మిळెను",
        "clear_title": "✅ ఖాళీ",
        "no_weeds_detected": "కలుపు మొక్కలు గుర్తించబడలేదు",
        "run_detection_btn": "🔍 గుర్తింపు చలాయించండి",
        "detect_weeds_title": "🔍 కలుపు గుర్తించండి",
        "learn_about_weeds": "📚 నేర్చుకోండి",
        "model_not_loaded": "మోడల్ లోడ్ చేయబడలేదు",
        "cannot_run_detection": "గుర్తింపు చలాయించలేము",
        "running_detection": "గుర్తింపు నడుస్తోంది...",
        "detection_completed_success": "✓ గుర్తింపు విజయవంతమైనది",
        "detection_completed": "✓ గుర్తింపు పూర్తైనది",
        "home_title": "🏠 హోమ్",
        "language_label": "భాష",
        "upload_btn": "అప్‌లోడ్ చేయండి",
        "upload_hint": "అధిక-రిజల్యూషన్ ఫీల్డ్ ఇమేజ్‌లు మెరుగైన ఫలితాలను ఇస్తాయి",
        "upload_hint_text": "మీ గోధుమ పొలం యొక్క స్పష్టమైన ఫోటో తీసి దిగువన అప్లోడ్ చేయండి",
        "detect_weeds": "🔍 కలుపు గుర్తించండి",
        "home": "హోమ్",
        "detect": "గుర్తించు",
        "learn": "నేర్చుకోండి"
    },
    "Hindi (हिंदी)": {
        "title": "वीडशील्ड AI",
        "subtitle": "AI का उपयोग करके गेहूं की फसल में खरपतवार की पहचान और रोकथाम",
        "upload": "खेत की तस्वीर अपलोड करें",
        "detect_btn": "पहचानें",
        "weed_detected": "⚠️ खरपतवार मिला",
        "no_weed": "✅ कोई खरपतवार नहीं",
        "confidence": "विश्वास स्कोर",
        "treatment": "उपचार की सिफारिशें",
        "severity": "गंभीरता स्तर",
        "action": "कार्रवाई",
        "urgency": "तत्कालता",
        "methods": "अनुशंसित तरीके",
        "herbicides": "अनुशंसित खरपतवारनाशी",
        "history": "पहचान इतिहास",
        "no_history": "अभी तक कोई पहचान नहीं",
        "clear_history": "इतिहास साफ करें",
        "how_to_use": "कैसे उपयोग करें",
        "step1": "📸 अपने गेहूं के खेत की फोटो लें या अपलोड करें",
        "step2": "🔍 खरपतवार का विश्लेषण करने के लिए पहचानें दबाएं",
        "step3": "📋 तुरंत उपचार की सिफारिशें प्राप्त करें",
        "download_pdf": "📥 रिपोर्ट डाउनलोड करें",
        "learn_title": "सीखें — गेहूं की फसल में खरपतवार",
        "tab1": "गेहूं में खरपतवार",
        "tab2": "कृषि पर प्रभाव",
        "tab3": "रोकथाम के तरीके",
        "what_are_weeds": "गेहूं के खेतों में खरपतवार क्या हैं",
        "weeds_desc": "खरपतवार गैर-फसल पौधे हैं जो फसल के साथ प्रतिस्पर्धा करते हैं। गेहूं के खेतों में सामान्य उदाहरण:",
        "weed1": "फालारिस माइनर (छोटे बीज वाली कैनरी घास)",
        "weed2": "एवेना फातुआ (जंगली जई)",
        "weed3": "अन्य चौड़ी पत्ती और घास वाले खरपतवार",
        "how_affect": "खरपतवार गेहूं की उपज को कैसे प्रभावित करते हैं:",
        "affect1": "प्रकाश, पानी और पोषक तत्वों के लिए प्रतिस्पर्धा",
        "affect2": "अनाज की उपज और गुणवत्ता कम करता है",
        "affect3": "उत्पादन लागत बढ़ाता है",
        "how_identify": "खरपतवार और गेहूं की पहचान कैसे करें",
        "identify_desc": "पत्ती के आकार, वृद्धि की आदत से पहचानें।",
        "why_early": "जल्दी पहचान क्यों जरूरी है",
        "early_desc": "जल्दी पहचान से लक्षित उपचार संभव होता है।",
        "impact_title": "कृषि पर प्रभाव",
        "impact1": "गंभीर खरपतवार से फसल नुकसान: 10-30%",
        "impact2": "आर्थिक प्रभाव: कम उपज, बढ़ी हुई लागत",
        "farmer_challenges": "किसानों की चुनौतियों में समय पर पहचान और श्रम सीमाएं शामिल हैं।",
        "prevention_title": "रोकथाम के तरीके",
        "prev1": "जहां संभव हो हाथ से निराई",
        "prev2": "खरपतवारनाशी कार्यक्रम",
        "prev3": "सांस्कृतिक तरीके (फसल चक्र)",
        "ai_benefits": "AI पहचान के फायदे: तेज़ खेत निगरानी और प्रारंभिक चेतावनी।",
        "nav_home": "🏠 होम",
        "nav_detect": "🔍 पहचानें",
        "nav_learn": "📚 सीखें",
        "model_ready": "✓ तैयार है",
        "hero_title": "अपनी गेहूं की फसल बचाएं",
        "hero_subtitle": "जल्दी पहचान, सटीक उपचार, बेहतर उपज",
        "quick_overview": "त्वरित अवलोकन",
        "scans_today": "आज के स्कैन",
        "weeds_found": "खरपतवार मिले",
        "accuracy": "सटीकता",
        "how_to_use_title": "WeedShield AI कैसे उपयोग करें",
        "step1_title": "फोटो लें",
        "step1_desc": "अपने गेहूं के खेत की स्पष्ट तस्वीर लें",
        "step2_title": "जांच करें",
        "step2_desc": "छवि अपलोड करें और जांच चलाएं",
        "step3_title": "परिणाम पाएं",
        "step3_desc": "उपचार की सिफारिशें प्राप्त करें",
        "season_badge": "मौसम: रबी 2025",
        "latest_detection": "नवीनतम जांच",
        "no_detections": "अभी तक कोई जांच नहीं",
        "field_clear": "खेत स्पष्ट",
        "detection_stats": "जांच आंकड़े",
        "wheat_label": "गेहूं",
        "weeds_label": "खरपतवार",
        "avg_confidence": "औसत आत्मविश्वास",
        "image_preview": "छवि पूर्वावलोकन",
        "upload_field_image": "📸 खेत की छवि अपलोड करें",
        "individual_detections": "📋 व्यक्तिगत जांच",
        "detection_results": "जांच परिणाम",
        "treatment_recommendations": "उपचार की सिफारिशें",
        "weeds_found_title": "⚠️ खरपतवार मिले",
        "clear_title": "✅ स्पष्ट",
        "no_weeds_detected": "कोई खरपतवार पहचाना नहीं गया",
        "run_detection_btn": "🔍 जांच चलाएं",
        "detect_weeds_title": "🔍 खरपतवार पहचानें",
        "learn_about_weeds": "📚 सीखें",
        "model_not_loaded": "मॉडल लोड नहीं हुआ",
        "cannot_run_detection": "जांच नहीं चला सकते",
        "running_detection": "जांच चल रही है...",
        "detection_completed_success": "✓ जांच सफलतापूर्वक पूरी हुई",
        "detection_completed": "✓ जांच पूरी हुई",
        "home_title": "🏠 होम",
        "language_label": "भाषा",
        "upload_btn": "अपलोड करें",
        "upload_hint": "उच्च-रिज़ॉल्यूशन खेत की तस्वीरें बेहतर परिणाम देती हैं",
        "upload_hint_text": "अपने गेहूँ के खेत की स्पष्ट फोटो लें और नीचे अपलोड करें",
        "detect_weeds": "🔍 खरपतवार पहचानें",
        "home": "होम",
        "detect": "पहचानें",
        "learn": "सीखें"
    }
}


st.set_page_config(page_title="WeedShield AI — Professional Weed Detector", layout="wide")


# Redesigned UI with modern styling
page_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

* { font-family: 'Poppins', sans-serif; }

/* MAIN CONTAINER - Light off-white background */
[data-testid="stAppViewContainer"] {
    background-color: #f7f5f0 !important;
}

/* SIDEBAR - Dark forest green */
[data-testid="stSidebar"] {
    background-color: #1a2e1a !important;
}

[data-testid="stSidebar"] * {
    color: #d4e8d4 !important;
}

/* Sidebar specific elements */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #d4e8d4 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #a8d5a8 !important;
    font-weight: 700 !important;
}

/* MAIN CONTENT - Light background */
.main [data-testid="stAppViewContainer"] > section {
    background-color: #f7f5f0 !important;
}

/* TEXT COLORS */
h1, h2, h3 {
    color: #2a4d2a !important;
    font-weight: 700 !important;
}

p, li, span, div {
    color: #3d3d3d !important;
}

/* BUTTONS - Green accent */
.stButton > button {
    background: linear-gradient(135deg, #2d6a2d 0%, #3d8a3d 100%) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 12px 24px !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 2px 8px rgba(45, 106, 45, 0.3) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #3d8a3d 0%, #4da84d 100%) !important;
    box-shadow: 0 4px 16px rgba(45, 106, 45, 0.5) !important;
    transform: translateY(-2px) !important;
}

/* HERO BANNER */
.hero-banner {
    background: linear-gradient(135deg, #2a4d2a 0%, #3d6a3d 100%) !important;
    padding: 40px 30px !important;
    border-radius: 12px !important;
    margin-bottom: 30px !important;
    text-align: center !important;
    box-shadow: 0 4px 15px rgba(42, 77, 42, 0.2) !important;
}

.hero-banner h1 {
    color: #ffffff !important;
    font-size: 32px !important;
    margin-bottom: 8px !important;
}

.hero-banner p {
    color: #e8f5e9 !important;
    font-size: 18px !important;
    margin: 0 !important;
}

/* STAT CARDS */
.stat-card {
    background-color: #ffffff !important;
    border: 2px solid #e0e0e0 !important;
    border-radius: 12px !important;
    padding: 24px !important;
    text-align: center !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
}

.stat-card:hover {
    border-color: #2d6a2d !important;
    box-shadow: 0 4px 16px rgba(45, 106, 45, 0.1) !important;
    transform: translateY(-4px) !important;
}

.stat-card .stat-number {
    color: #2d6a2d !important;
    font-size: 36px !important;
    font-weight: 700 !important;
    margin: 12px 0 !important;
}

.stat-card .stat-label {
    color: #666666 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}

/* STEP CARDS */
.step-card {
    background-color: #ffffff !important;
    border: 1px solid #e8e8e8 !important;
    border-radius: 10px !important;
    padding: 20px !important;
    text-align: center !important;
    transition: all 0.3s ease !important;
}

.step-card:hover {
    box-shadow: 0 4px 12px rgba(45, 106, 45, 0.15) !important;
    border-color: #a8d5a8 !important;
}

.step-number {
    display: inline-block !important;
    background: #2d6a2d !important;
    color: white !important;
    width: 40px !important;
    height: 40px !important;
    line-height: 40px !important;
    border-radius: 50% !important;
    font-weight: 700 !important;
    font-size: 18px !important;
    margin-bottom: 12px !important;
}

.step-card h3 {
    margin-top: 12px !important;
    margin-bottom: 8px !important;
    font-size: 16px !important;
}

.step-card p {
    font-size: 13px !important;
    min-height: 60px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* UPLOAD ZONE */
[data-testid="stFileUploader"] {
    background-color: #ffffff !important;
    border: 2px dashed #2d6a2d !important;
    border-radius: 12px !important;
    padding: 30px !important;
    transition: all 0.3s ease !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: #3d8a3d !important;
    background-color: #f0f7f0 !important;
}

/* WHITE CARDS */
.white-card {
    background-color: #ffffff !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 12px !important;
    padding: 24px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
}

/* TABS */
.stTabs [data-baseweb="tab"] {
    color: #666666 !important;
    font-weight: 600 !important;
    border-bottom: 3px solid transparent !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #2d6a2d !important;
    border-bottom: 3px solid #2d6a2d !important;
}

/* EXPANDER */
.streamlit-expanderHeader {
    background: #f5f5f5 !important;
    border-radius: 8px !important;
    color: #2d6a2d !important;
    font-weight: 600 !important;
}

/* PAGE TITLE WITH BADGE */
.page-header {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    margin-bottom: 24px !important;
    padding: 0 !important;
}

.page-title {
    color: #2a4d2a !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}

.season-badge {
    background: #2d6a2d !important;
    color: white !important;
    padding: 8px 16px !important;
    border-radius: 20px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

/* STATUS PILL */
.status-pill {
    display: inline-block !important;
    background: #4da84d !important;
    color: white !important;
    padding: 8px 16px !important;
    border-radius: 20px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}

/* SUCCESS/ERROR BOXES */
[data-testid="stSuccess"] {
    background: #e8f5e9 !important;
    border: 1px solid #81c784 !important;
    border-radius: 8px !important;
}

/* MOBILE RESPONSIVE */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem 0.5rem !important;
    }
    h1 { font-size: 22px !important; }
    h2 { font-size: 18px !important; }
    h3 { font-size: 16px !important; }
    p, li { font-size: 14px !important; }
    .hero-banner h1 { font-size: 24px !important; }
    .stat-card .stat-number { font-size: 28px !important; }
}

/* DOWNLOAD BUTTON */
[data-testid="stDownloadButton"] > button {
    background: #1565c0 !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    transition: all 0.25s ease !important;
}

[data-testid="stDownloadButton"] > button:hover {
    background: #1976d2 !important;
    transform: translateY(-2px) !important;
}

/* SELECTOR */
[data-testid="stSelectbox"] > div {
    background: #ffffff !important;
    border: 1px solid #d0d0d0 !important;
    border-radius: 8px !important;
}

</style>
"""

st.markdown(page_css, unsafe_allow_html=True)


# Class configuration
CLASS_MAP = {0: 'Weed', 1: 'Wheat'}
CLASS_COLORS = {0: (255, 0, 0), 1: (0, 200, 0)}  # Red for Weed, Green for Wheat (RGB)



def calculate_severity(weed_count, weed_confidences):
    if weed_count == 0:
        return ('Low', 0.0, '🟢')

    avg_conf = np.mean(weed_confidences) if weed_confidences else 0.0

    if weed_count >= 5:
        return ('High', avg_conf, '🔴')
    elif weed_count == 1:
        if avg_conf >= 0.35:
            return ('Medium', avg_conf, '🟡')
        else:
            return ('Low', avg_conf, '🟢')
    elif weed_count <= 4:
        return ('Medium', avg_conf, '🟡')
    else:
        return ('High', avg_conf, '🔴')


def draw_detections_on_image(img_pil, boxes):
    img = img_pil.copy()
    draw = ImageDraw.Draw(img)
    
    weed_count = 0
    wheat_count = 0
    
    if boxes is not None and len(boxes) > 0:
        try:
            font = ImageFont.truetype("arial.ttf", 16)
            small_font = ImageFont.truetype("arial.ttf", 12)
        except:
            font = ImageFont.load_default()
            small_font = font
        
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            
            if cls == 0:
                weed_count += 1
            elif cls == 1:
                wheat_count += 1
            
            color = CLASS_COLORS.get(cls, (255, 255, 255))
            class_name = CLASS_MAP.get(cls, f'Class {cls}')
            
            box_width = 3
            for i in range(box_width):
                draw.rectangle(
                    [(x1-i, y1-i), (x2+i, y2+i)],
                    outline=color,
                    width=1
                )
            
            label_text = f'{class_name} {conf:.1%}'
            
            text_bbox = draw.textbbox((0, 0), label_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            label_x = x1
            label_y = max(0, y1 - text_height - 12)
            bg_box = [label_x - 2, label_y - 2, label_x + text_width + 8, label_y + text_height + 8]
            draw.rectangle(bg_box, fill=color)
            
            draw.text((label_x + 4, label_y + 2), label_text, font=font, fill=(255, 255, 255))
    
    return img, weed_count, wheat_count


def generate_pdf_report(img_annotated, weed_count, wheat_count, severity_level, severity_icon,
                       treatment_info, boxes, upload_name, detection_time, image_size, duration):
    from io import BytesIO

    pdf_bytes = BytesIO()
    c = canvas.Canvas(pdf_bytes, pagesize=letter)
    width, height = letter

    def wrap_text(text, max_width, font_size=10):
        from reportlab.pdfbase.ttfonts import TTFont
        c.setFont("Helvetica", font_size)
        words = text.split(' ')
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            line_str = ' '.join(current_line)
            if c.stringWidth(line_str, "Helvetica", font_size) > max_width:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        return lines

    y_pos = height - 40

    c.setFont("Helvetica-Bold", 24)
    c.drawString(30, y_pos, "WeedShield AI")
    c.setFont("Helvetica", 12)
    c.drawString(30, y_pos - 20, "Weed Detection Report")
    y_pos -= 50

    c.setFont("Helvetica-Bold", 11)
    c.drawString(30, y_pos, "Report Information")
    y_pos -= 15

    c.setFont("Helvetica", 10)
    c.drawString(40, y_pos, f"Image: {upload_name}")
    y_pos -= 12
    y_pos -= 12
    c.drawString(40, y_pos, f"Processing Duration: {duration:.3f}s")
    y_pos -= 12
    y_pos -= 12
    y_pos -= 25

    c.setFont("Helvetica-Bold", 11)
    c.drawString(30, y_pos, "Detection Summary")
    y_pos -= 15

    c.setFont("Helvetica", 10)
    c.drawString(40, y_pos, f"Weeds Detected: {weed_count}")
    y_pos -= 12
    c.drawString(40, y_pos, f"Wheat Plants: {wheat_count}")
    y_pos -= 12

    c.setFont("Helvetica-Bold", 12)
    severity_text = f"Severity Level: {severity_icon} {severity_level}"
    c.drawString(40, y_pos, severity_text)
    y_pos -= 25

    c.setFont("Helvetica-Bold", 11)
    c.drawString(30, y_pos, "Treatment Recommendations")
    y_pos -= 15

    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y_pos, f"Weed: {treatment_info.get('weed_name', 'General Weed')}")
    y_pos -= 12

    c.setFont("Helvetica", 9)
    detail_lines = wrap_text(treatment_info.get('description', 'N/A'), 500, 9)
    for line in detail_lines:
        c.drawString(40, y_pos, line)
        y_pos -= 11

    y_pos -= 5
    c.setFont("Helvetica-Bold", 9)
    c.drawString(40, y_pos, "Recommended Methods:")
    y_pos -= 10

    c.setFont("Helvetica", 9)
    for method in treatment_info.get('methods', []):
        c.drawString(50, y_pos, f"• {method}")
        y_pos -= 10
    
    if treatment_info.get('all_herbicides'):
        y_pos -= 5
        c.setFont("Helvetica-Bold", 9)
        c.drawString(40, y_pos, "Recommended Herbicides:")
        y_pos -= 10
        
        c.setFont("Helvetica", 9)
        for herbicide in treatment_info.get('all_herbicides', []):
            c.drawString(50, y_pos, f"• {herbicide}")
            y_pos -= 10
    
    y_pos -= 5
    c.setFont("Helvetica", 9)
    c.drawString(40, y_pos, f"Urgency: {treatment_info.get('urgency', 'N/A')}")
    y_pos -= 12
    c.drawString(40, y_pos, f"Cost Impact: {treatment_info.get('cost_impact', 'N/A')}")
    y_pos -= 25

    if boxes is not None and len(boxes) > 0:
        y_pos -= 10
        c.setFont("Helvetica-Bold", 11)
        c.drawString(30, y_pos, "Individual Detections")
        y_pos -= 15

        c.setFont("Helvetica", 9)
        for i, box in enumerate(boxes):
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            class_name = CLASS_MAP.get(cls, f'Class {cls}')
            det_text = f"{i+1}. {class_name} - {conf:.1%} confidence"
            c.drawString(40, y_pos, det_text)
            y_pos -= 10

            if y_pos < 50:
                c.showPage()
                y_pos = height - 40

    c.setFont("Helvetica", 8)
    c.drawString(30, 20, "Generated by WeedShield AI | YOLOv8 Detection Engine | Model: best.pt")

    c.save()
    pdf_bytes.seek(0)
    return pdf_bytes.getvalue()


# Model path and load
MODEL_PATH = "best.pt"

# Language selector at top of sidebar
language_options = ["English", "Telugu (తెలుగు)", "Hindi (हिंदी)"]
language = st.sidebar.selectbox(
    "Language",
    language_options,
    label_visibility="collapsed"
)
t = TRANSLATIONS[language]

try:
    with st.spinner('Loading model (YOLOv8)...'):
        model = YOLO(MODEL_PATH)
except Exception as e:
    st.sidebar.error(f"Failed to load model: {e}")
    model = None


# SIDEBAR HEADER - Logo area
st.sidebar.markdown("""
<div style="text-align: center; padding: 20px 0; border-bottom: 1px solid #3a5a3a; margin-bottom: 20px;">
    <h1 style="font-size: 28px; margin: 0 0 8px 0;">🌾</h1>
    <h2 style="font-size: 20px; margin: 0; color: #a8d5a8;">WeedShield AI</h2>
    <p style="font-size: 12px; color: #8ac48a; margin: 4px 0 0 0;">Wheat Weed Detection</p>
</div>
""", unsafe_allow_html=True)

# NAVIGATION
st.sidebar.markdown("<h3 style='color: #8ac48a; font-size: 12px; text-transform: uppercase; margin-top: 0; margin-bottom: 12px;'>Navigation</h3>", unsafe_allow_html=True)

nav_options = [
    ("🏠 Home", t.get("nav_home", "Home")),
    ("🔍 Detect", t.get("nav_detect", "Detect")),
    ("📚 Learn", t.get("nav_learn", "Learn"))
]

# Store current page in session state
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 0

menu_index = st.sidebar.radio(
    "Navigation",
    range(len(nav_options)),
    format_func=lambda x: nav_options[x][0],
    label_visibility="collapsed"
)
st.session_state['current_page'] = menu_index
menu = nav_options[menu_index][1]

st.sidebar.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

# Model status pill in sidebar
st.sidebar.markdown(f"""
<div style="background: #4da84d; color: white; padding: 8px 16px; border-radius: 20px; font-size: 11px; font-weight: 600; text-align: center;">
    ✓ {t.get('model_ready', 'Model ready')}
</div>
""", unsafe_allow_html=True)


# Session state initialization
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'last_upload' not in st.session_state:
    st.session_state['last_upload'] = None


def add_history(entry):
    st.session_state['history'].insert(0, entry)
    st.session_state['history'] = st.session_state['history'][:100]


# Remove the sidebar history rendering - now handled by session state only


### HOME ###
if t.get("nav_home","Home") in menu or menu == 'Home':
    # Page header with title and badge
    col_title, col_badge = st.columns([3, 1])
    with col_title:
        st.markdown(f'<h1 class="page-title">{t.get("home_title", "🏠 Home")}</h1>', unsafe_allow_html=True)
    with col_badge:
        st.markdown(f'<div class="season-badge">{t.get("season_badge", "Season: Rabi 2025")}</div>', unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
    
    # HERO BANNER
    st.markdown(f"""
    <div class="hero-banner">
        <h1 style="margin: 0; color: #ffffff; font-size: 32px;">🌾 {t.get('hero_title', 'Protect Your Wheat Crop')}</h1>
        <p style="margin: 12px 0 0 0; color: rgba(255,255,255,0.8); font-size: 16px;">{t.get('hero_subtitle', 'Early detection, precise treatment, better yields')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # STAT CARDS
    st.markdown(f"<h3 style='color: #2a4d2a; margin-top: 32px; margin-bottom: 16px;'>{t.get('quick_overview', 'Quick Overview')}</h3>", unsafe_allow_html=True)
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 24px;">📊</div>
            <div class="stat-number">0</div>
            <div class="stat-label">{t.get('scans_today', 'Scans Today')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 24px;">🌱</div>
            <div class="stat-number">0</div>
            <div class="stat-label">{t.get('weeds_found', 'Weeds Found')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col3:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 24px;">🎯</div>
            <div class="stat-number">98%</div>
            <div class="stat-label">{t.get('accuracy', 'Accuracy')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 32px 0; border: none; border-top: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
    
    # HOW TO USE - STEP CARDS (moved up, upload removed from home)
    st.markdown(f"<h3 style='color: #2a4d2a; margin-top: 32px; margin-bottom: 16px;'>{t.get('how_to_use_title', 'How to Use WeedShield AI')}</h3>", unsafe_allow_html=True)
    
    step_col1, step_col2, step_col3 = st.columns(3)
    
    with step_col1:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">1</div>
            <h3 style="margin-bottom: 8px;">{t.get('step1_title', 'Take Photo')}</h3>
            <p style="font-size: 13px; color: #666;">{t.get('step1_desc', 'Capture a clear image of your wheat field showing weeds or suspicious areas')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col2:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">2</div>
            <h3 style="margin-bottom: 8px;">{t.get('step2_title', 'Run Detection')}</h3>
            <p style="font-size: 13px; color: #666;">{t.get('step2_desc', 'Upload the image and click Run Detection for instant AI analysis')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col3:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">3</div>
            <h3 style="margin-bottom: 8px;">{t.get('step3_title', 'Get Results')}</h3>
            <p style="font-size: 13px; color: #666;">{t.get('step3_desc', 'Receive personalized treatment recommendations based on detection results')}</p>
        </div>
        """, unsafe_allow_html=True)


### DETECT ###
if t.get("nav_detect","Detect") in menu or menu == 'Detect':
    # Page header
    st.markdown(f'<h1 class="page-title">{t.get("detect_weeds_title", "🔍 Detect Weeds")}</h1>', unsafe_allow_html=True)
    st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        st.markdown(f"**{t.get('upload_field_image', '📸 Upload Field Image')}**")
        st.markdown(f"📷 {t.get('upload_hint_text', 'Take a clear photo of your wheat field and upload below')}")
        uploaded_file = st.file_uploader('', type=['jpg', 'jpeg', 'png'], label_visibility="collapsed",
                                        help=t.get('upload_hint', 'High-resolution field images give better results'))

        if uploaded_file is not None:
            upload_bytes = uploaded_file.getvalue()
            st.session_state['last_upload'] = {
                'name': getattr(uploaded_file, 'name', 'uploaded_image'),
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'bytes': upload_bytes
            }
            img = Image.open(io.BytesIO(upload_bytes)).convert('RGB')
            st.image(img, use_column_width=True)
            
            if st.button(t['detect_btn'], use_container_width=True):
                if model is None:
                    st.error('Model not loaded. Cannot run detection.')
                else:
                    t0 = time.time()
                    img_pil = Image.open(io.BytesIO(st.session_state['last_upload']['bytes'])).convert('RGB')
                    img_np = np.array(img_pil)
                    
                    with st.spinner('Running detection...'):
                        results = model(img_np, conf=0.5)
                    t1 = time.time()

                    boxes = results[0].boxes
                    st.success('✓ Detection completed')

                    img_annotated, weed_count, wheat_count = draw_detections_on_image(img_pil, boxes)

                    weed_confidences = [float(b.conf[0]) for b in boxes if int(b.cls[0]) == 0]
                    severity_level, severity_conf, severity_icon = calculate_severity(weed_count, weed_confidences)
                    
                    avg_weed_confidence = np.mean(weed_confidences) if weed_confidences else 0.0
                    treatment_info = format_recommendation("general_weed", avg_weed_confidence, language)

                    pdf_data = generate_pdf_report(img_annotated, weed_count, wheat_count, 
                                                  treatment_info.get('severity', 'LOW'), '📊',
                                                  treatment_info, boxes, st.session_state['last_upload']['name'],
                                                  st.session_state['last_upload']['time'], img_pil.size, t1-t0)

                    st.session_state['latest_result'] = {
                        'img_annotated': img_annotated,
                        'weed_count': weed_count,
                        'wheat_count': wheat_count,
                        'severity': severity_level,
                        'treatment': treatment_info,
                        'boxes': boxes,
                        'avg_conf': avg_weed_confidence,
                        'pdf': pdf_data,
                        'filename': f"{st.session_state['last_upload']['name'].rsplit('.', 1)[0]}_detection_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    }

        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        st.markdown(f"**{t.get('latest_detection', 'Latest Detection')}**")
        
        if 'latest_result' in st.session_state:
            result = st.session_state['latest_result']
            if result['weed_count'] > 0:
                st.markdown(f"<span style='color: #c62828; font-weight: bold;'>⚠️ {result['weed_count']} weed{'s' if result['weed_count'] != 1 else ''} detected</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color: #2e7d32; font-weight: bold;'>✅ {t.get('field_clear', 'Field Clear')}</span>", unsafe_allow_html=True)
            
            st.markdown(f"🌾 {t.get('wheat_label', 'Wheat')}: **{result['wheat_count']}**")
            st.markdown(f"🌱 {t.get('weeds_label', 'Weeds')}: **{result['weed_count']}**")
            st.markdown(f"🎯 {t.get('avg_confidence', 'Accuracy')}: **{result['avg_conf']:.1%}**")
        else:
            st.markdown(t.get('no_detections', 'No detections yet'))
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Show results below if available
    if 'latest_result' in st.session_state:
        result = st.session_state['latest_result']
        
        st.markdown("<hr style='margin: 24px 0; border: none; border-top: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: #2a4d2a;'>{t.get('detection_results', 'Detection Results')}</h3>", unsafe_allow_html=True)
        
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        st.image(result['img_annotated'], use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download button
        st.download_button(
            label=t['download_pdf'],
            data=result['pdf'],
            file_name=result['filename'],
            mime="application/pdf",
            use_container_width=True
        )
        
        # Detections details
        if result['boxes'] is not None and len(result['boxes']) > 0:
            with st.expander("📋 Individual Detections", expanded=False):
                for i, box in enumerate(result['boxes']):
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    class_name = CLASS_MAP.get(cls, f'Class {cls}')
                    st.markdown(f"{i+1}. **{class_name}** - {conf:.1%} confidence")
        
        # Treatment recommendations if weeds detected
        if result['weed_count'] > 0:
            st.markdown("<hr style='margin: 24px 0; border: none; border-top: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color: #2a4d2a;'>Treatment Recommendations</h3>", unsafe_allow_html=True)
            
            st.markdown('<div class="white-card">', unsafe_allow_html=True)
            
            severity_colors = {
                "LOW": "#4CAF50",
                "MEDIUM": "#FF9800",
                "HIGH": "#f44336"
            }
            severity_color = severity_colors.get(result['treatment'].get('severity', 'LOW'), "#666666")
            
            st.markdown(f"**Severity:** <span style='color: {severity_color}; font-weight: bold;'>{result['treatment'].get('severity', 'LOW')}</span>", unsafe_allow_html=True)
            st.markdown(f"**Action:** {result['treatment'].get('action', 'Monitor field')}")
            st.markdown(f"**Description:** {result['treatment'].get('description', 'N/A')}")
            
            if result['treatment'].get('methods'):
                st.markdown("**Recommended Methods:**")
                for method in result['treatment'].get('methods', []):
                    st.markdown(f"• {method}")
            
            if result['treatment'].get('all_herbicides'):
                st.markdown("**Recommended Herbicides:**")
                for herbicide in result['treatment'].get('all_herbicides', []):
                    st.markdown(f"• {herbicide}")
            
            st.markdown(f"**Urgency:** {result['treatment'].get('urgency', 'N/A')}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Add to history
        add_history({
            'image_name': st.session_state['last_upload']['name'],
            'result': f'{result["weed_count"]} weed{"s" if result["weed_count"] != 1 else ""} detected' if result['weed_count'] > 0 else 'No weeds detected',
            'weeds': result['weed_count'],
            'wheat': result['wheat_count'],
            'confidence': result['avg_conf'] * 100,
            'severity': result['severity'],
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })


### LEARN ###
if t.get("nav_learn","Learn") in menu or menu == 'Learn':
    # Page header
    st.markdown(f'<h1 class="page-title">{t.get("learn_title", "📚 Learn — Weeds in Wheat Crops")}</h1>', unsafe_allow_html=True)
    st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
    
    tabs = st.tabs([t['tab1'], t['tab2'], t['tab3']])

    with tabs[0]:
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        st.markdown(f"### {t['what_are_weeds']}")
        st.markdown(f"{t['weeds_desc']}")
        st.markdown(f"- {t['weed1']}\n- {t['weed2']}\n- {t['weed3']}")
        
        st.markdown(f"### {t['how_affect']}")
        st.markdown(f"- {t['affect1']}\n- {t['affect2']}\n- {t['affect3']}")
        
        st.markdown(f"### {t['how_identify']}")
        st.markdown(f"{t['identify_desc']}")
        
        st.markdown(f"### {t['why_early']}")
        st.markdown(f"{t['early_desc']}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]:
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        st.markdown(f"### {t['impact_title']}")
        st.markdown(f"- {t['impact1']}")
        st.markdown(f"- {t['impact2']}")
        st.markdown(f"\n{t['farmer_challenges']}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]:
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        st.markdown(f"### {t['prevention_title']}")
        st.markdown(f"- {t['prev1']}\n- {t['prev2']}\n- {t['prev3']}")
        st.markdown(f"\n{t['ai_benefits']}")
        st.markdown('</div>', unsafe_allow_html=True)

