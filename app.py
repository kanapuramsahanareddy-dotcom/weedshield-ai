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


# Page configuration
st.set_page_config(page_title="WeedShield AI — Professional Weed Detector", layout="wide")


# Premium dark-themed CSS with glowing effects and animations
page_css = """
<style>
@keyframes pulse-glow {
    0%, 100% { text-shadow: 0 0 10px #ffd700, 0 0 20px #ffaa00, 0 0 30px #ff8800; }
    50% { text-shadow: 0 0 15px #ffd700, 0 0 25px #ffaa00, 0 0 40px #ff8800; }
}

@keyframes red-pulse {
    0%, 100% { 
        color: #ff2d2d;
        text-shadow: 0 0 10px #ff0000, 0 0 20px #ff4444, 0 0 30px #ff0000;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.6), inset 0 0 20px rgba(255, 0, 0, 0.2);
    }
    50% { 
        color: #ff5555;
        text-shadow: 0 0 20px #ff0000, 0 0 30px #ff4444, 0 0 40px #ff8888;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.8), inset 0 0 25px rgba(255, 0, 0, 0.3);
    }
}

@keyframes green-pulse {
    0%, 100% {
        color: #00ff88;
        text-shadow: 0 0 10px #00c853, 0 0 20px #69f0ae, 0 0 30px #00e676;
    }
    50% {
        color: #69f0ae;
        text-shadow: 0 0 20px #00c853, 0 0 30px #69f0ae, 0 0 40px #00e676;
    }
}

@keyframes green-glow-hover {
    0% { box-shadow: 0 0 10px rgba(0, 200, 83, 0.5); }
    50% { box-shadow: 0 0 20px rgba(105, 240, 174, 0.8), inset 0 0 10px rgba(0, 200, 83, 0.2); }
    100% { box-shadow: 0 0 10px rgba(0, 200, 83, 0.5); }
}

@keyframes checkmark {
    0% { transform: scale(0); }
    50% { transform: scale(1.2); }
    100% { transform: scale(1); }
}

:root {
    --primary-dark: #0a1628;
    --secondary-dark: #1a3a2a;
    --accent-dark: #0d2818;
    --primary-green: #00c853;
    --bright-green: #69f0ae;
    --gold: #ffd700;
    --bright-gold: #ffaa00;
    --warn-red: #ff2d2d;
    --glass-light: rgba(255, 255, 255, 0.05);
    --glass-border: rgba(255, 255, 255, 0.1);
}

body {
    color: #e0e0e0;
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    background: linear-gradient(135deg, #0a1628 0%, #1a3a2a 50%, #0d2818 100%);
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a1628 0%, #1a3a2a 50%, #0d2818 100%);
    background-attachment: fixed;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1f0f 0%, #051407 100%);
    border-right: 1px solid rgba(0, 200, 83, 0.2);
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    transition: all 0.3s ease;
}

.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(0, 200, 83, 0.3);
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.glass-card:hover {
    border: 1px solid rgba(0, 200, 83, 0.6);
    box-shadow: 0 4px 25px rgba(0, 200, 83, 0.2);
    background: rgba(255, 255, 255, 0.08);
}

.title-centered {
    text-align: center;
    font-size: 48px;
    color: var(--gold);
    margin: 0 0 12px 0;
    font-weight: 900;
    animation: pulse-glow 3s ease-in-out infinite;
    letter-spacing: 2px;
}

.subtitle-centered {
    text-align: center;
    color: rgba(255, 255, 255, 0.8);
    margin: 0 0 20px 0;
    font-size: 16px;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
}

.muted {
    color: rgba(255, 255, 255, 0.6);
}

.small {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.7);
}

.label {
    color: rgba(255, 255, 255, 0.9);
    font-weight: 600;
    text-transform: uppercase;
    font-size: 12px;
    letter-spacing: 1px;
}

.value {
    color: var(--bright-green);
    font-weight: 900;
    font-size: 20px;
}

.conf {
    color: var(--gold);
    font-weight: 800;
}

.file-label {
    font-weight: 700;
    color: var(--bright-green);
    text-transform: uppercase;
    font-size: 14px;
    letter-spacing: 1px;
    transition: all 0.3s ease;
}

hr {
    border: 0;
    border-top: 1px solid rgba(0, 200, 83, 0.2);
    margin: 20px 0;
}

/* Button styling - Bright green gradient with glow */
[data-testid="stForm"] button,
.stButton > button {
    background: linear-gradient(135deg, #00c853 0%, #69f0ae 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 15px rgba(0, 200, 83, 0.4) !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 0 30px rgba(0, 200, 83, 0.8), inset 0 0 10px rgba(105, 240, 174, 0.3) !important;
    background: linear-gradient(135deg, #69f0ae 0%, #00c853 100%) !important;
}

.stButton > button:active {
    transform: scale(0.98) !important;
}

/* Download button */
[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, #00c853 0%, #69f0ae 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    box-shadow: 0 0 15px rgba(0, 200, 83, 0.4) !important;
    transition: all 0.3s ease !important;
}

[data-testid="stDownloadButton"] button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 0 30px rgba(0, 200, 83, 0.8) !important;
}

/* File uploader styling */
[data-testid="stFileUploadDropzone"] {
    border: 2px dashed var(--primary-green) !important;
    border-radius: 12px !important;
    background: rgba(0, 200, 83, 0.05) !important;
    transition: all 0.3s ease !important;
}

[data-testid="stFileUploadDropzone"]:hover {
    background: rgba(0, 200, 83, 0.1) !important;
    border-color: var(--bright-green) !important;
    box-shadow: 0 0 20px rgba(0, 200, 83, 0.3) !important;
}

/* Sidebar navigation */
[data-testid="stSidebarNav"] a {
    color: rgba(255, 255, 255, 0.7) !important;
    transition: all 0.3s ease !important;
    border-bottom: 2px solid transparent !important;
    padding-bottom: 4px !important;
}

[data-testid="stSidebarNav"] a:hover {
    color: var(--bright-green) !important;
    border-bottom: 2px solid var(--primary-green) !important;
}

/* Radio button (navigation menu) */
[data-testid="stRadio"] {
    transition: all 0.3s ease !important;
}

[data-testid="stRadio"] label {
    color: rgba(255, 255, 255, 0.8) !important;
    transition: all 0.3s ease !important;
}

[data-testid="stRadio"] label:hover {
    color: var(--bright-green) !important;
}

/* Active radio button */
[data-testid="stRadio"] [aria-checked="true"] + label {
    color: var(--bright-green) !important;
    font-weight: 700 !important;
    text-shadow: 0 0 10px rgba(0, 200, 83, 0.5) !important;
}

/* Expander styling */
[data-testid="stExpander"] {
    border: 1px solid rgba(0, 200, 83, 0.2) !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}

[data-testid="stExpander"]:hover {
    border: 1px solid rgba(0, 200, 83, 0.5) !important;
    background: rgba(0, 200, 83, 0.05) !important;
}

/* Tabs styling */
[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--bright-green) !important;
    border-bottom: 3px solid var(--primary-green) !important;
    text-shadow: 0 0 10px rgba(0, 200, 83, 0.4) !important;
}

/* Success message */
[data-testid="stAlert"] {
    background: rgba(0, 200, 83, 0.1) !important;
    border: 1px solid rgba(0, 200, 83, 0.4) !important;
    border-radius: 12px !important;
    color: var(--bright-green) !important;
}

/* Error message */
[data-testid="stAlert"] .stAlert {
    background: rgba(255, 45, 45, 0.1) !important;
    border: 1px solid rgba(255, 45, 45, 0.4) !important;
    color: #ff5555 !important;
}

/* Info message */
[data-testid="stAlert"] {
    border-radius: 12px !important;
}

/* Treatment recommendation card with severity badge */
.severity-badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 11px;
    letter-spacing: 1px;
    transition: all 0.3s ease;
}

.severity-low {
    background: rgba(0, 200, 83, 0.2);
    color: #69f0ae;
    border: 1px solid rgba(0, 200, 83, 0.5);
    box-shadow: 0 0 10px rgba(0, 200, 83, 0.3);
}

.severity-medium {
    background: rgba(255, 165, 0, 0.2);
    color: #ffa500;
    border: 1px solid rgba(255, 165, 0, 0.5);
    box-shadow: 0 0 10px rgba(255, 165, 0, 0.3);
}

.severity-high {
    background: rgba(255, 45, 45, 0.2);
    color: #ff5555;
    border: 1px solid rgba(255, 45, 45, 0.5);
    box-shadow: 0 0 10px rgba(255, 45, 45, 0.3);
}

.severity-badge:hover {
    transform: scale(1.05);
    text-shadow: 0 0 10px currentColor;
}

/* Recommendation cards */
.recommendation-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(0, 200, 83, 0.3);
    border-radius: 12px;
    padding: 16px;
    margin: 12px 0;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.recommendation-card:hover {
    border: 1px solid rgba(0, 200, 83, 0.6);
    box-shadow: 0 4px 25px rgba(0, 200, 83, 0.25);
    background: rgba(255, 255, 255, 0.08);
}

/* History items in sidebar */
.history-item {
    background: rgba(0, 200, 83, 0.08);
    border: 1px solid rgba(0, 200, 83, 0.2);
    border-radius: 10px;
    padding: 12px;
    margin: 8px 0;
    transition: all 0.3s ease;
}

.history-item:hover {
    border: 1px solid rgba(0, 200, 83, 0.5);
    background: rgba(0, 200, 83, 0.12);
    box-shadow: 0 0 15px rgba(0, 200, 83, 0.2);
}

.history-dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 8px;
    animation: pulse 2s ease-in-out infinite;
}

.history-dot-weed {
    background: #ff2d2d;
    box-shadow: 0 0 10px rgba(255, 45, 45, 0.6);
}

.history-dot-clear {
    background: var(--bright-green);
    box-shadow: 0 0 10px rgba(105, 240, 174, 0.6);
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

/* Latest detection panel */
.latest-detection {
    background: rgba(0, 200, 83, 0.08);
    border: 2px solid rgba(0, 200, 83, 0.3);
    border-radius: 12px;
    padding: 16px;
    transition: all 0.3s ease;
}

.latest-detection:hover {
    border: 2px solid rgba(0, 200, 83, 0.6);
    background: rgba(0, 200, 83, 0.12);
    box-shadow: 0 0 20px rgba(0, 200, 83, 0.25);
}

/* Markdown text styling */
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4 {
    color: rgba(255, 255, 255, 0.95) !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    margin-top: 20px !important;
    margin-bottom: 12px !important;
    transition: all 0.3s ease !important;
}

[data-testid="stMarkdownContainer"] h2 {
    color: var(--bright-green) !important;
    font-size: 28px !important;
}

[data-testid="stMarkdownContainer"] h3 {
    color: var(--gold) !important;
    font-size: 20px !important;
}

[data-testid="stMarkdownContainer"] a {
    color: var(--bright-green) !important;
    text-decoration: none !important;
    border-bottom: 1px solid rgba(0, 200, 83, 0.5) !important;
    transition: all 0.3s ease !important;
}

[data-testid="stMarkdownContainer"] a:hover {
    color: var(--gold) !important;
    border-bottom: 1px solid var(--gold) !important;
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.5) !important;
}

/* Image styling */
[data-testid="stImage"] {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 200, 83, 0.15);
    transition: all 0.3s ease;
}

[data-testid="stImage"]:hover {
    box-shadow: 0 4px 30px rgba(0, 200, 83, 0.3);
}

/* Column spacing */
[data-testid="stColumns"] {
    gap: 20px;
}

/* Smooth all transitions */
* {
    transition: all 0.3s ease;
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
st.sidebar.markdown('<p style="text-align: center; margin-top: 16px; padding: 12px; background: rgba(0, 200, 83, 0.1); border: 1px solid rgba(0, 200, 83, 0.5); border-radius: 8px; color: #69f0ae; font-weight: 700;">✅ Model Loaded Successfully</p>', unsafe_allow_html=True)

try:
    with st.spinner('Loading model (YOLOv8)...'):
        model = YOLO(MODEL_PATH)
except Exception as e:
    st.sidebar.error(f"Failed to load model: {e}")
    model = None


# Sidebar navigation
st.sidebar.markdown('<h2 style="color: #ffd700; text-align: center; text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);">⚡ WEEDSHIELD AI ⚡</h2>', unsafe_allow_html=True)
menu = st.sidebar.radio("Navigation", ["🏠 Home", "🔍 Detect", "📚 Learn", "ℹ️ About"])


# Session state initialization
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'last_upload' not in st.session_state:
    st.session_state['last_upload'] = None


def add_history(entry):
    st.session_state['history'].insert(0, entry)
    st.session_state['history'] = st.session_state['history'][:100]


def render_sidebar_history():
    st.sidebar.markdown("---")
    st.sidebar.markdown('<h3 style="color: #69f0ae; text-align: center;">📋 Detection History</h3>', unsafe_allow_html=True)
    if not st.session_state['history']:
        st.sidebar.info("ℹ️ No detections yet.")
    else:
        for h in st.session_state['history']:
            dot_class = "history-dot-weed" if h['weeds'] > 0 else "history-dot-clear"
            dot_icon = "🚨" if h['weeds'] > 0 else "✅"
            st.sidebar.markdown(f'<div class="history-item">', unsafe_allow_html=True)
            st.sidebar.markdown(f"<p style='margin: 0; color: #e0e0e0;'><strong>{dot_icon} {h['time']}</strong></p>", unsafe_allow_html=True)
            st.sidebar.markdown(f"<p style='margin: 4px 0; font-size: 13px; color: rgba(255, 255, 255, 0.7);'>{h['image_name']}</p>", unsafe_allow_html=True)
            st.sidebar.markdown(f"<p style='margin: 4px 0; font-size: 12px;'>🌾 Wheat: <strong>{h['wheat']}</strong> | 🌱 Weeds: <strong>{h['weeds']}</strong></p>", unsafe_allow_html=True)
            st.sidebar.markdown(f"<p style='margin: 4px 0; font-size: 12px; color: #69f0ae;'>📈 Confidence: <strong>{h['confidence']:.1f}%</strong></p>", unsafe_allow_html=True)
            st.sidebar.markdown('</div>', unsafe_allow_html=True)

    if st.sidebar.button('🗑️ Clear History', use_container_width=True):
        st.session_state['history'] = []
        st.rerun()


render_sidebar_history()


### HOME ###
if menu == 'Home':
    c1, c2 = st.columns([3,1])
    with c1:
        st.markdown('<div class="glass-card" style="border: 2px solid rgba(0, 200, 83, 0.5); background: rgba(0, 200, 83, 0.08);">', unsafe_allow_html=True)
        st.markdown('<h1 class="title-centered">⚡ WEEDSHIELD AI ⚡</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle-centered">🌾 Professional AI-Powered Weed Detection in Wheat Fields 🌾</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card" style="margin-top:16px; border-left: 4px solid #69f0ae;">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #69f0ae; margin-top: 0;">🎯 How to use</h3>', unsafe_allow_html=True)
        st.markdown('- 📤 Upload a farm image (JPEG/PNG)\n- 🔍 Click "Detect" to analyze the image\n- 📊 Review detailed detection results with bounding boxes, counts, and confidence scores')
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="latest-detection">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #69f0ae; margin-top: 0; text-align: center;">🤖 AI Model</h4>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; margin: 12px 0; color: rgba(255, 255, 255, 0.8);">YOLOv8 Vision</p>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-size: 12px; color: rgba(255, 255, 255, 0.6);">Advanced Deep Learning</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


### DETECT ###
if menu == 'Detect':
    st.markdown('<h1 style="color: var(--bright-green); text-align: center; text-shadow: 0 0 15px rgba(0, 200, 83, 0.5);">🔍 WEED DETECTION ANALYSIS</h1>', unsafe_allow_html=True)
    col_left, col_right = st.columns([2,1])

    with col_left:
        st.markdown('<div class="glass-card" style="border: 2px solid var(--primary-green);">', unsafe_allow_html=True)
        st.markdown('<div class="file-label">📸 Upload Farm Image</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader('', type=['jpg', 'jpeg', 'png'], help='High-resolution field images give better results')

        if uploaded_file is not None:
            upload_bytes = uploaded_file.getvalue()
            st.session_state['last_upload'] = {'name': getattr(uploaded_file, 'name', 'uploaded_image'), 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'bytes': upload_bytes}
            img = Image.open(io.BytesIO(upload_bytes)).convert('RGB')
            st.image(img, caption='📷 Uploaded Image Preview', use_column_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        if uploaded_file is not None and st.button('🚀 RUN DETECTION', use_container_width=True):
            if model is None:
                st.error('❌ Model not loaded. Cannot run detection.')
            else:
                t0 = time.time()
                img_pil = Image.open(io.BytesIO(st.session_state['last_upload']['bytes'])).convert('RGB')
                img_np = np.array(img_pil)
                
                with st.spinner('🔄 Running detection...'):
                    results = model(img_np, conf=0.5)
                t1 = time.time()

                boxes = results[0].boxes
                
                st.success('✅ Detection completed successfully')

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
                st.image(img_annotated, caption='🎯 Detection Results with Bounding Boxes', use_column_width=True)

                pdf_filename = f"{st.session_state['last_upload']['name'].rsplit('.', 1)[0]}_detection_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                st.download_button(
                    label="📥 DOWNLOAD DETECTION REPORT (PDF)",
                    data=pdf_data,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    use_container_width=True
                )

                st.markdown('---')
                if weed_count > 0:
                    weed_confidences = [float(b.conf[0]) * 100 for b in boxes if int(b.cls[0]) == 0]
                    max_conf = max(weed_confidences) if weed_confidences else 0
                    st.markdown(f'<div style="text-align: center; padding: 30px; background: rgba(255, 45, 45, 0.15); border-radius: 16px; border: 2px solid #ff2d2d; animation: red-pulse 2s ease-in-out infinite;">', unsafe_allow_html=True)
                    st.markdown(f'<h1 style="color: #ff2d2d; margin: 0; animation: red-pulse 2s ease-in-out infinite; text-shadow: 0 0 20px rgba(255, 0, 0, 0.8);">⚠️ WEED DETECTED</h1>', unsafe_allow_html=True)
                    st.markdown(f'<h3 style="color: #ffcccc; margin: 12px 0 0 0;">Confidence: {max_conf:.1f}%</h3>', unsafe_allow_html=True)
                    st.markdown(f'</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="text-align: center; padding: 30px; background: rgba(0, 200, 83, 0.15); border-radius: 16px; border: 2px solid #00c853; animation: green-pulse 2s ease-in-out infinite;">', unsafe_allow_html=True)
                    st.markdown(f'<h1 style="color: #69f0ae; margin: 0; animation: green-pulse 2s ease-in-out infinite; text-shadow: 0 0 20px rgba(0, 200, 83, 0.8);">✅ NO WEED FOUND</h1>', unsafe_allow_html=True)
                    st.markdown(f'<p style="color: #a8f5d8; margin-top: 12px; font-size: 16px;">Field is clear and weed-free</p>', unsafe_allow_html=True)
                    st.markdown(f'</div>', unsafe_allow_html=True)

                # Dropdown expander
                with st.expander('📋 View Detailed Detection Report', expanded=False):
                    col_d1, col_d2 = st.columns(2)

                    with col_d1:
                        st.markdown(f"**Image Name:** `{st.session_state['last_upload']['name']}`")
                        st.markdown(f"**Processing Time:** `{t1-t0:.2f}s`")

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
                    st.markdown('<h2 style="color: #69f0ae; text-shadow: 0 0 10px rgba(0, 200, 83, 0.5);">🛠️ TREATMENT RECOMMENDATIONS</h2>', unsafe_allow_html=True)

                    severity_colors = {
                        "LOW": "#00c853",
                        "MEDIUM": "#FFA500",
                        "HIGH": "#FF0000"
                    }
                    severity_color = severity_colors.get(treatment_info.get('severity', 'LOW'), "#CCCCCC")
                    severity_class = treatment_info.get('severity', 'LOW').lower()

                    st.markdown(f"<div class='recommendation-card' style='border-left: 4px solid {severity_color};'>", unsafe_allow_html=True)
                    st.markdown(f"<span class='severity-badge severity-{severity_class}'>{treatment_info.get('severity', 'LOW')}</span>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin: 16px 0 8px 0;'><strong>Confidence Score:</strong> <span style='color: {severity_color}; font-weight: 900;'>{avg_weed_confidence:.1%}</span></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin: 8px 0;'><strong>Urgency Level:</strong> {treatment_info.get('urgency', 'N/A')}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown(f"**Action Required:** {treatment_info.get('action', 'Monitor field')}")
                    st.markdown(f"**Description:** {treatment_info.get('description', 'N/A')}")

                    st.markdown("**✓ Recommended Methods:**")
                    for method in treatment_info.get('methods', []):
                        st.markdown(f"  • {method}")

                    if treatment_info.get('all_herbicides', []):
                        st.markdown("**💊 Recommended Herbicides:**")
                        for herbicide in treatment_info.get('all_herbicides', []):
                            st.markdown(f"  • <span style='color: #ffd700; font-weight: 700;'>{herbicide}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("**💡 Recommended Herbicides:** None - Preventive monitoring only")

                    st.markdown(f"**⏱️ Urgency:** {treatment_info.get('urgency', 'N/A')}")
                    st.markdown(f"**💰 Cost Impact:** {treatment_info.get('cost_impact', 'N/A')}")

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
        st.markdown('<div class="latest-detection">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #69f0ae; margin-top: 0; text-align: center;">📊 Latest Detection</h3>', unsafe_allow_html=True)
        if st.session_state['history']:
            latest = st.session_state['history'][0]
            status_color = "#ff2d2d" if latest['weeds'] > 0 else "#69f0ae"
            status_text = "🚨 Weeds Detected" if latest['weeds'] > 0 else "✅ No Weeds"
            st.markdown(f"<p style='text-align: center; color: {status_color}; font-weight: 700; font-size: 16px;'>{status_text}</p>", unsafe_allow_html=True)
            st.markdown(f"🌾 Wheat: **{latest['wheat']}** | 🌱 Weeds: **{latest['weeds']}**")
            st.markdown(f"📈 Confidence: **{latest['confidence']:.1f}%**")
            st.markdown(f"*{latest['time']}*")
        else:
            st.markdown('<p style="text-align: center; color: rgba(255, 255, 255, 0.6);">No detections yet</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


### LEARN ###
if menu == 'Learn':
    st.markdown('<h1 style="color: var(--bright-green); text-shadow: 0 0 15px rgba(0, 200, 83, 0.5);">📚 LEARN — Weeds in Wheat Crops</h1>', unsafe_allow_html=True)
    tabs = st.tabs(['🌾 Weeds in Wheat', '📊 Impact on Agriculture', '🛡️ Prevention Methods'])

    with tabs[0]:
        st.markdown('<h2 style="color: #69f0ae;">What are weeds in wheat fields?</h2>', unsafe_allow_html=True)
        st.write('Weeds are non-crop plants that grow within crop stands and compete for resources. Common examples in wheat fields:')
        st.markdown('- 🌱 **Phalaris minor** (Little seed canary grass)\n- 🌾 **Avena fatua** (Wild oats)\n- 🍃 Other broadleaf and grassy weeds')
        
        st.markdown('<h3 style="color: #ffd700;">How weeds affect wheat yield:</h3>', unsafe_allow_html=True)
        st.markdown('- 💧 Compete for light, water and nutrients\n- 📉 Reduce grain yield and quality\n- 💰 Increase production costs')
        
        st.markdown('<h3 style="color: #ffd700;">How to identify weeds vs wheat</h3>', unsafe_allow_html=True)
        st.write('Identify by leaf shape, growth habit and tiller structure; automated detection uses visual features learned by the model.')
        
        st.markdown('<h3 style="color: #ffd700;">Why early detection is important</h3>', unsafe_allow_html=True)
        st.write('Early detection enables targeted treatment, reduces herbicide use and limits yield loss.')

    with tabs[1]:
        st.markdown('<h2 style="color: #69f0ae;">Impact on Agriculture</h2>', unsafe_allow_html=True)
        st.markdown('- 📊 Typical crop loss from severe weed infestation: **10–30%** (varies by species and timing)')
        st.markdown('- 💼 Economic impact: reduced marketable yield, increased input costs, and labor')
        st.write('Farmer challenges include timely identification, selective application of control measures, and labor limitations.')

    with tabs[2]:
        st.markdown('<h2 style="color: #69f0ae;">Prevention Methods</h2>', unsafe_allow_html=True)
        st.markdown('- 🤲 Manual removal where feasible\n- 💊 Herbicide programs (selective and rotational use)\n- 🔄 Cultural practices (crop rotation, competitive cultivars)')
        st.write('AI detection benefits: fast field-scale scouting, early warning, and data-driven interventions to reduce costs and environmental impact.')


### ABOUT ###
if menu == 'About':
    st.markdown('<h1 style="color: var(--bright-green); text-shadow: 0 0 15px rgba(0, 200, 83, 0.5);">ℹ️ About WeedShield AI</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card" style="border: 2px solid rgba(105, 240, 174, 0.4);">', unsafe_allow_html=True)
    st.write('🚀 Professional weed detection prototype built with **YOLOv8** and **Streamlit**.')
    st.write('Designed for academic presentation and practical field testing.')
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h3 style="color: #ffd700; margin-top: 24px;">🔧 Technology Stack</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #69f0ae; margin-top: 0;">🤖 AI Model</h4>', unsafe_allow_html=True)
        st.markdown('YOLOv8 - State-of-the-art object detection')
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #69f0ae; margin-top: 0;">🎨 Frontend</h4>', unsafe_allow_html=True)
        st.markdown('Streamlit - Interactive web interface')
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #69f0ae; margin-top: 0;">📊 Data</h4>', unsafe_allow_html=True)
        st.markdown('Custom wheat & weed dataset')
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('---')
    st.markdown('**📧 Contact:** Project repository and documentation available on request.')
