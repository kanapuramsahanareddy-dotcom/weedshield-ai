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
        "ai_benefits": "AI detection benefits: fast field-scale scouting, early warning, and data-driven interventions to reduce costs and environmental impact."
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
        "ai_benefits": "AI గుర్తింపు ప్రయోజనాలు: వేగవంతమైన పొలం పర్యవేక్షణ మరియు ముందస్తు హెచ్చరిక."
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
        "ai_benefits": "AI पहचान के फायदे: तेज़ खेत निगरानी और प्रारंभिक चेतावनी।"
    }
}


st.set_page_config(page_title="WeedShield AI — Professional Weed Detector", layout="wide")


# Professional CSS: farm theme + glassmorphism
page_css = """
<style>
.stButton > button {
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(0,200,83,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-3px) scale(1.03) !important;
    box-shadow: 0 8px 25px rgba(0,200,83,0.6) !important;
}
@media (max-width: 768px) {
    .main .block-container { padding: 1rem !important; }
    h1 { font-size: 24px !important; }
}
:root{--farm-green:#2d5b3b; --farm-brown:#7a4a2b; --wheat:#d6b85a; --accent:#6fbf73; --glass: rgba(255,255,255,0.04); --glass-border: rgba(255,255,255,0.06)}
body {color: #f3f7f2; font-family: 'Segoe UI', Roboto, Arial, sans-serif}
[data-testid="stAppViewContainer"]{
    background-image: linear-gradient(rgba(6,10,6,0.55), rgba(6,10,6,0.55)), url('https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1920&q=80');
    background-size: cover; background-position: center; background-attachment: fixed
}
[data-testid="stSidebar"]{background: linear-gradient(180deg, rgba(10,45,19,0.9), rgba(8,30,18,0.95)); color: #f0fbf0}
.glass-card{background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));backdrop-filter: blur(6px);border-radius:12px;padding:16px;border:1px solid var(--glass-border)}
.title-centered{text-align:center;font-size:34px;color:var(--wheat);margin:0 0 6px 0;font-weight:700}
.subtitle-centered{text-align:center;color:#f7f5e6;margin:0 0 14px 0}
.muted{color:#d9ead8}
.result-card{background: linear-gradient(180deg, rgba(45,60,30,0.55), rgba(38,50,28,0.45)); border-radius:12px; padding:14px; border:1px solid rgba(219,189,115,0.06)}
.small{font-size:13px;color:#dbeed6}
.label{color:#fbf7e6;font-weight:600}
.value{color:#fff7e9;font-weight:700}
.conf{color:var(--wheat); font-weight:800}
.stats-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0}
.stat-box{background:rgba(45,75,45,0.6);padding:12px;border-radius:8px;border-left:3px solid var(--wheat)}
.stat-label{font-size:11px;color:#d4e69f;text-transform:uppercase;font-weight:600}
.stat-value{font-size:28px;color:#fff;font-weight:900;margin-top:4px}
.uploader {border-radius:10px; padding:12px}
.btn-wrap .stButton>button{background:var(--farm-green);color:white;border-radius:8px;padding:10px 14px;border:none;font-weight:700}
.btn-wrap .stButton>button:hover{transform:translateY(-3px);box-shadow:0 8px 20px rgba(0,0,0,0.35);opacity:0.95}
.file-label{font-weight:600;color:#fff7e9}
hr{border:0; border-top:1px solid rgba(255,255,255,0.04)}
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
st.sidebar.success("✓ Model Loaded Successfully")

try:
    with st.spinner('Loading model (YOLOv8)...'):
        model = YOLO(MODEL_PATH)
except Exception as e:
    st.sidebar.error(f"Failed to load model: {e}")
    model = None


# Sidebar navigation
language = st.sidebar.selectbox(
    "🌐 Language / భాష / भाषा",
    ["English", "Telugu (తెలుగు)", "Hindi (हिंदी)"]
)
t = TRANSLATIONS[language]

st.sidebar.title(t["title"])
menu = st.sidebar.radio("Navigation", ["Home", "Detect", "Learn", "About"])


# Session state initialization
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'last_upload' not in st.session_state:
    st.session_state['last_upload'] = None


def add_history(entry):
    st.session_state['history'].insert(0, entry)
    st.session_state['history'] = st.session_state['history'][:100]


def render_sidebar_history():
    st.sidebar.markdown(f"## {t['history']}")
    if not st.session_state['history']:
        st.sidebar.info(t['no_history'])
    else:
        for h in st.session_state['history']:
            st.sidebar.markdown(f"**{h['time']}** — {h['image_name']}")
            st.sidebar.markdown(f"- Weeds: **{h['weeds']}** | Wheat: **{h['wheat']}**")
            st.sidebar.markdown(f"- Confidence: **{h['confidence']:.1f}%**")
            st.sidebar.markdown("---")

    if st.sidebar.button(t['clear_history']):
        st.session_state['history'] = []


render_sidebar_history()


### HOME ###
if menu == 'Home':
    c1, c2 = st.columns([3,1])
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f'<h1 class="title-centered">{t["title"]}</h1>', unsafe_allow_html=True)
        st.markdown(f'<p class="subtitle-centered">{t["subtitle"]}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card" style="margin-top:12px">', unsafe_allow_html=True)
        st.markdown(f'**{t["how_to_use"]}**', unsafe_allow_html=True)
        st.markdown(f'- {t["step1"]}\n- {t["step2"]}\n- {t["step3"]}')
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('**Model**')
        st.markdown('</div>', unsafe_allow_html=True)


### DETECT ###
if menu == 'Detect':
    st.markdown(f'## Detect — {t["upload"]} for analysis')
    col_left, col_right = st.columns([2,1])

    with col_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="file-label">{t["upload"]}</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader('', type=['jpg', 'jpeg', 'png'], help='High-resolution field images give better results')

        if uploaded_file is not None:
            upload_bytes = uploaded_file.getvalue()
            st.session_state['last_upload'] = {'name': getattr(uploaded_file, 'name', 'uploaded_image'), 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'bytes': upload_bytes}
            img = Image.open(io.BytesIO(upload_bytes)).convert('RGB')
            st.image(img, caption='Uploaded image', use_column_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        if uploaded_file is not None and st.button(t['detect_btn'], use_container_width=True):
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
                
                st.success('✓ Detection completed successfully')

                img_annotated, weed_count, wheat_count = draw_detections_on_image(img_pil, boxes)
                total = weed_count + wheat_count

                weed_confidences = [float(b.conf[0]) for b in boxes if int(b.cls[0]) == 0]
                severity_level, severity_conf, severity_icon = calculate_severity(weed_count, weed_confidences)
                
                avg_weed_confidence = np.mean(weed_confidences) if weed_confidences else 0.0
                treatment_info = format_recommendation("general_weed", avg_weed_confidence)

                pdf_data = generate_pdf_report(img_annotated, weed_count, wheat_count, 
                                              treatment_info.get('severity', 'LOW'), '📊',
                                              treatment_info, boxes, st.session_state['last_upload']['name'],
                                              st.session_state['last_upload']['time'], img_pil.size, t1-t0)

                output_dir = "detection_results"
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, f"detected_{st.session_state['last_upload']['name']}")
                img_annotated_cv2 = np.array(img_annotated)
                img_annotated_cv2 = img_annotated_cv2[:, :, ::-1]
                
                

                if total == 0:
                    result_text = 'No weeds detected'
                    status = 'Clear'
                else:
                    result_text = f'{weed_count} weed{"s" if weed_count != 1 else ""} detected in {total} object{"s" if total != 1 else ""}'
                    status = 'Attention required' if weed_count > 0 else 'Clear'

                st.markdown('---')
                st.image(img_annotated, caption='Detection Results', width='stretch')

                pdf_filename = f"{st.session_state['last_upload']['name'].rsplit('.', 1)[0]}_detection_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                st.download_button(
                    label=t['download_pdf'],
                    data=pdf_data,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    use_container_width=True
                )

                st.markdown('---')
                if weed_count > 0:
                    weed_confidences = [float(b.conf[0]) * 100 for b in boxes if int(b.cls[0]) == 0]
                    max_conf = max(weed_confidences) if weed_confidences else 0
                    st.markdown(f'<div style="text-align: center; padding: 20px; background: rgba(255,0,0,0.15); border-radius: 12px; border: 2px solid #ff4444;">', unsafe_allow_html=True)
                    st.markdown(f'<h1 style="color: #ff4444; margin: 0;">{t["weed_detected"]}</h1>', unsafe_allow_html=True)
                    st.markdown(f'<h3 style="color: #ffcccc; margin: 8px 0 0 0;">{t["confidence"]}: {max_conf:.1f}%</h3>', unsafe_allow_html=True)
                    st.markdown(f'</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="text-align: center; padding: 20px; background: rgba(0,200,0,0.15); border-radius: 12px; border: 2px solid #00c800;">', unsafe_allow_html=True)
                    st.markdown(f'<h1 style="color: #00c800; margin: 0;">{t["no_weed"]}</h1>', unsafe_allow_html=True)
                    st.markdown(f'</div>', unsafe_allow_html=True)

                # Dropdown expander
                with st.expander('', expanded=False):
                    col_d1, col_d2 = st.columns(2)

                    with col_d1:
                        st.markdown(f"**Image Name:** {st.session_state['last_upload']['name']}")

                    with col_d2:
                        if boxes is not None and len(boxes) > 0:
                            st.markdown("**Individual Detections:**")
                            for i, box in enumerate(boxes):
                                cls = int(box.cls[0])
                                conf = float(box.conf[0])
                                class_name = CLASS_MAP.get(cls, f'Class {cls}')
                                st.markdown(f"{i+1}. **{class_name}** - {conf:.1%} confidence")
                        else:
                            st.markdown("No detections found.")

                # Treatment Recommendations section - only show when weeds are detected
                if weed_count > 0:
                    st.markdown("---")
                    st.markdown(f"**{t['treatment']}**")

                    severity_colors = {
                        "LOW": "#FFD700",
                        "MEDIUM": "#FFA500",
                        "HIGH": "#FF0000"
                    }
                    severity_color = severity_colors.get(treatment_info.get('severity', 'LOW'), "#CCCCCC")

                    st.markdown(f"<div style='padding: 12px; background-color: rgba({int(severity_color[1:3], 16)}, {int(severity_color[3:5], 16)}, {int(severity_color[5:7], 16)}, 0.2); border-left: 4px solid {severity_color}; border-radius: 6px;'>", unsafe_allow_html=True)
                    st.markdown(f"**{t['severity']}:** <span style='color: {severity_color}; font-weight: bold;'>{treatment_info.get('severity', 'LOW')}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Confidence Range:** {treatment_info.get('urgency', 'N/A')}", unsafe_allow_html=True)
                    st.markdown(f"**Confidence Score:** {avg_weed_confidence:.1%}", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown(f"**{t['action']}:** {treatment_info.get('action', 'Monitor field')}")
                    st.markdown(f"**Description:** {treatment_info.get('description', 'N/A')}")

                    st.markdown(f"**{t['methods']}:")
                    for method in treatment_info.get('methods', []):
                        st.markdown(f"- {method}")

                    if treatment_info.get('all_herbicides', []):
                        st.markdown(f"**{t['herbicides']}:**")
                        for herbicide in treatment_info.get('all_herbicides', []):
                            st.markdown(f"- {herbicide}")
                    else:
                        st.markdown(f"**{t['herbicides']}:** None - Preventive monitoring only")

                    st.markdown(f"**{t['urgency']}:** {treatment_info.get('urgency', 'N/A')}")
                    st.markdown(f"**Cost Impact:** {treatment_info.get('cost_impact', 'N/A')}")

                # Add to history
                avg_conf = float(np.mean([float(b.conf[0]) for b in boxes])) * 100 if (boxes and len(boxes) > 0) else 0
                add_history({
                    'image_name': st.session_state['last_upload']['name'],
                    'result': result_text,
                    'weeds': weed_count,
                    'wheat': wheat_count,
                    'confidence': avg_conf,
                    'severity': severity_level,
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })

    with col_right:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('### Latest Detection')
        if st.session_state['history']:
            latest = st.session_state['history'][0]
            st.markdown(f"**Status:** {latest['result']}")
            st.markdown(f"🌾 Wheat: **{latest['wheat']}** | 🌱 Weeds: **{latest['weeds']}**")
            st.markdown(f"Confidence: **{latest['confidence']:.1f}%**")
            st.markdown(f"*{latest['time']}*")
        else:
            st.markdown(t['no_history'])
        st.markdown('</div>', unsafe_allow_html=True)


### LEARN ###
if menu == 'Learn':
    st.header(t['learn_title'])
    tabs = st.tabs([t['tab1'], t['tab2'], t['tab3']])

    with tabs[0]:
        st.subheader(t['what_are_weeds'])
        st.write(t['weeds_desc'])
        st.markdown(f"- {t['weed1']}\n- {t['weed2']}\n- {t['weed3']}")
        st.write(t['how_affect'])
        st.markdown(f"- {t['affect1']}\n- {t['affect2']}\n- {t['affect3']}")
        st.subheader(t['how_identify'])
        st.write(t['identify_desc'])
        st.subheader(t['why_early'])
        st.write(t['early_desc'])

    with tabs[1]:
        st.subheader(t['impact_title'])
        st.markdown(f"- {t['impact1']}")
        st.markdown(f"- {t['impact2']}")
        st.write(t['farmer_challenges'])

    with tabs[2]:
        st.subheader(t['prevention_title'])
        st.markdown(f"- {t['prev1']}\n- {t['prev2']}\n- {t['prev3']}")
        st.write(t['ai_benefits'])


### ABOUT ###
if menu == 'About':
    st.header('About WeedShield AI')
    st.write('Professional weed detection prototype built with YOLOv8 and Streamlit. Designed for academic presentation and practical field testing.')
    st.markdown('**Contact:** Project repository and documentation available on request.')
