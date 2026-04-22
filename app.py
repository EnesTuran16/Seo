import streamlit as st
import google.generativeai as genai
import json
import typing_extensions

# Page Configuration
st.set_page_config(page_title="Roots & Paws SEO Generator", page_icon="🌱", layout="centered")

# Custom CSS for Roots & Paws Branding
st.markdown("""
    <style>
    .stApp {
        background-color: #fcfaf7;
    }
    .stButton>button {
        background-color: #7b8e7e;
        color: white;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# Secure API Key Authorization via Streamlit Secrets
try:
    # On local testing, you can use st.secrets["GOOGLE_API_KEY"] or an environment variable
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.warning("⚠️ API Key not found. Please configure the 'GOOGLE_API_KEY' in Streamlit Secrets.")
    st.stop()

# Safety Settings to prevent false-positives on holistic/anatomical terms
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Pydantic-like Schema for Deterministic JSON Output
class MetadataSchema(typing_extensions.TypedDict):
    internal_title: str
    seo_page_title: str
    high_intent_tags: list[str]
    html_description: str
    meta_description: str

# System Instructions (Hard-coded Rules)
system_instruction = """
You are an elite E-Commerce Solutions Architect working for 'Roots & Paws Co.', a premium holistic pet health and vintage lifestyle brand.
Your task is to generate high-converting, SEO-optimized metadata strictly following these rules:

1. INTERNAL TITLE: Clean, operational name.
2. SEO PAGE TITLE: Use MIKE RHODES FORMULA: [Style] + [Subject] + [Vibe] + [Product Type]. (Max 70 chars).
3. TAGS: Exactly 13 high-intent, long-tail tags (hyphenated-clusters).
4. HTML DESCRIPTION: 
   - <h2>Benefit Headline</h2>
   - <p>Intro paragraph</p>
   - <ul> exactly 3-5 <li><strong>Feature:</strong> Benefit</li> units.
5. META DESCRIPTION: 120-150 chars ending with a Call to Action.

NEGATIVE CONSTRAINTS:
- NEVER use words: "cheap", "diy", "discount", "bargain".
- NEVER use generic placeholders.
- OUTPUT ONLY VALID JSON.
"""

# Model Initialization (Using Gemini 2.5 Flash for Free Tier efficiency)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instruction,
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=MetadataSchema,
        temperature=0.4,
    ),
    safety_settings=safety_settings
)

# UI Design
st.title("🌱 Roots & Paws SEO Generator")
st.caption("Generate premium, algorithm-ready product metadata in seconds.")

with st.form("seo_form"):
    product_name = st.text_input("Product Name", placeholder="e.g., Organic Lavender Dog Calming Balm")
    key_features = st.text_area("Key Features & Ingredients", placeholder="e.g., Organic Shea Butter, Lavender Oil, Calms anxiety, Heals dry paws")
    target_vibe = st.text_input("Target Audience / Vibe", placeholder="e.g., Senior dogs, sleep aid, boho aesthetic")
    
    submitted = st.form_submit_button("Generate Metadata ✨")

if submitted:
    if not product_name or not key_features:
        st.error("Please provide both Product Name and Key Features.")
    else:
        with st.spinner("Writing the perfect SEO copy..."):
            prompt = f"Product: {product_name}\nFeatures: {key_features}\nVibe: {target_vibe}"
            try:
                response = model.generate_content(prompt)
                data = json.loads(response.text)
                
                st.success("Metadata Generated!")
                
                st.subheader("📌 Mağaza İçi Başlık")
                st.code(data["internal_title"], language="text")
                
                st.subheader("🔍 SEO Başlığı (Mike Rhodes)")
                st.code(data["seo_page_title"], language="text")
                
                st.subheader("🏷️ Etiketler (Shopify/Etsy Ready)")
                st.write(", ".join(data["high_intent_tags"]))
                
                st.subheader("📄 HTML Ürün Açıklaması")
                st.code(data["html_description"], language="html")
                with st.expander("👁️ Görünüm Önizleme"):
                    st.markdown(data["html_description"], unsafe_allow_html=True)
                
                st.subheader("📱 Meta Açıklama")
                st.code(data["meta_description"], language="text")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
