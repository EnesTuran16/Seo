import streamlit as st
import google.generativeai as genai
import json
import typing_extensions

# Page Configuration
st.set_page_config(
    page_title="Roots & Paws | Elite SEO Studio v3",
    page_icon="🌿",
    layout="wide"
)

# Advanced Aesthetic CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; background-color: #fcfaf7; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #ffffff; border: 1px solid #e0d9d1; border-radius: 10px; color: #4a5d4d; }
    .stButton>button { background-color: #7b8e7e !important; color: white !important; border-radius: 12px; padding: 15px; font-weight: 600; border: none; }
    .stButton>button:hover { background-color: #5d6d5f !important; }
    .html-preview { background-color: white !important; color: #333333 !important; padding: 25px; border-radius: 12px; border: 1px solid #ddd; line-height: 1.6; }
    .html-preview h2, .html-preview p, .html-preview li, .html-preview strong { color: #333333 !important; }
    .intent-badge { padding: 5px 12px; border-radius: 20px; background-color: #e8f0e9; color: #4a5d4d; font-weight: 600; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# API Configuration
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("⚠️ GOOGLE_API_KEY not found in Secrets.")
    st.stop()

# UPDATED FIXED FOOTER (Full version with Youth & Toddler)
FIXED_FOOTER = """
<hr>
<p>🚚 <strong>Estimated Delivery:</strong> 7-10 Business Days (Includes 2-3 days production + 5-7 days standard US shipping).</p>
<p><strong>Premium Quality for the Whole Family 🌿</strong></p>
<p>At Roots & Paws Co., we believe in quality that lasts and memories that matter. We select only the finest, softest fabrics tailored to each age group:</p>
<ul>
<li><strong>Adult T-Shirts (Unisex):</strong> Comfort Colors® 1717 — garment-dyed, 100% ring-spun cotton. Vintage feel from day one.</li>
<li><strong>Youth T-Shirts:</strong> Comfort Colors® 9018 — same premium vintage style, built for kids.</li>
<li><strong>Toddler T-Shirts:</strong> Rabbit Skins™ 3321 — gentle on sensitive skin, durable combed ringspun cotton.</li>
<li><strong>Long Sleeve Tees:</strong> Comfort Colors® 6014 — heavyweight warmth for cooler days.</li>
</ul>
<p>📏 <strong>Sizing & Fit</strong></p>
<ul>
<li><strong>Adults:</strong> Relaxed, unisex fit. For an oversized look, size up 1–2 sizes.</li>
<li><strong>Kids & Toddlers:</strong> True to size. When in doubt, size up for longer wear.</li>
</ul>
<p>🧺 <strong>Care Instructions:</strong> Machine wash cold, inside out. Tumble dry low. Do not iron directly on the design. Our garment-dyed fabrics get even softer with every wash!</p>
"""

class EliteMetadataSchema(typing_extensions.TypedDict):
    detected_intent: str
    tone_profile: str
    seo_page_title: str
    high_intent_tags: list[str]
    aeo_html_description: str
    meta_description: str
    json_ld_schema: str
    semantic_entities: list[str]

# SYSTEM INSTRUCTION
system_instruction = """
You are an elite E-Commerce Solutions Architect and AEO Strategist for 'Roots & Paws Co.'
Regardless of the input language, ALWAYS generate all outputs in English.

MODULE 1: INTENT CLASSIFIER
- Analyze input to determine intent (Transactional, Investigational, Informational).
- Adjust tone: Transactional = Persuasive/Urgent; Informational = Educational/Authoritative.

MODULE 2: AEO & GEO CONTENT GENERATION (2026 Standards)
- INVERTED PYRAMID: Answer the core user query in the first 40 words.
- ENTITY MAPPING: Use LSI concepts (e.g., microbiome, regenerative, bioavailability).
- E-E-A-T: Include one realistic veterinarian-style quote or data statistic.
- PSYCHOLOGICAL TRIGGERS: Use the 'Anchoring Effect' for products >$50. Integrate social proof.
- HTML FORMAT: Use <h2> for benefits. No exclamation marks. British spelling. Oxford commas.

MODULE 3: JSON-LD SCHEMA GENERATOR
- Output a valid <script type="application/ld+json"> block.
- Include Product, Offer (USD, InStock), and AggregateRating (liquid variables).
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instruction,
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=EliteMetadataSchema,
        temperature=0.4,
    )
)

# UI Layout
st.markdown('### 🌱 Roots & Paws | Elite SEO Studio v3')
st.caption("AEO Optimized & Full-Family Logistics Integrated")
st.markdown("---")

col1, col2 = st.columns([1, 1.8], gap="large")

with col1:
    st.markdown("#### 🛠️ Ürün Konfigürasyonu")
    p_name = st.text_input("Ürün Adı", placeholder="Örn: Cool Aunt Club T-Shirt")
    p_features = st.text_area("Özellikler & İçerik", placeholder="Örn: %100 Pamuk, Terracotta Renk, Vintage Tasarım", height=120)
    p_vibe = st.text_input("Hedef Kitle / Vibe", placeholder="Örn: Köpek seven teyzeler")
    
    gen_btn = st.button("Elite SEO Üret ✨")

with col2:
    if gen_btn:
        with st.spinner("Stratejik içerik üretiliyor..."):
            prompt = f"Product: {p_name}\nFeatures: {p_features}\nVibe: {p_vibe}"
            try:
                response = model.generate_content(prompt)
                data = json.loads(response.text)
                
                st.markdown(f'<span class="intent-badge">Intent: {data["detected_intent"]}</span> <span class="intent-badge">Tone: {data["tone_profile"]}</span>', unsafe_allow_html=True)
                
                tab1, tab2, tab3 = st.tabs(["📄 Content & SEO", "🏷️ Semantic Tags", "💻 JSON-LD Schema"])
                
                with tab1:
                    st.markdown("##### 🔍 SEO Page Title")
                    st.code(data["seo_page_title"], language="text")
                    
                    st.markdown("##### 📱 Meta Description")
                    st.code(data["meta_description"], language="text")
                    
                    st.markdown("##### 📝 AEO Product Description")
                    full_html = data["aeo_html_description"] + FIXED_FOOTER
                    st.code(full_html, language="html")
                    
                    with st.expander("👁️ Rendered Preview"):
                        st.markdown(f'<div class="html-preview">{full_html}</div>', unsafe_allow_html=True)
                
                with tab2:
                    st.markdown("##### 🏷️ 13 Strategic Tags")
                    st.write(", ".join(data["high_intent_tags"]))
                    st.markdown("##### 🧠 Semantic Entities Detected")
                    st.write(", ".join(data["semantic_entities"]))
                
                with tab3:
                    st.markdown("##### 🤖 Technical SEO (JSON-LD)")
                    st.code(data["json_ld_schema"], language="html")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
