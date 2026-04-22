import streamlit as st
import google.generativeai as genai
import json
import typing_extensions

# Page Configuration for Premium Feel
st.set_page_config(
    page_title="Roots & Paws | SEO Studio",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Roots & Paws Branding CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #fcfaf7;
    }
    
    .main {
        background-color: #fcfaf7;
    }
    
    /* Header Styling */
    .header-style {
        font-size: 32px;
        font-weight: 600;
        color: #4a5d4d;
        margin-bottom: 0px;
    }
    
    /* Input Box Styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #ffffff;
        border: 1px solid #e0d9d1;
        border-radius: 10px;
        color: #4a5d4d;
    }
    
    /* Button Styling */
    .stButton>button {
        width: 100%;
        background-color: #7b8e7e !important;
        color: white !important;
        border-radius: 12px;
        border: none;
        padding: 15px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #5d6d5f !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Result Card Styling */
    .result-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #7b8e7e;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    .tag-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }
    
    .tag-item {
        background-color: #f0ede9;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 14px;
        color: #4a5d4d;
        border: 1px solid #e0d9d1;
    }
    </style>
    """, unsafe_allow_html=True)

# Secure API Configuration
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("⚠️ API Key found in Secrets. Please add GOOGLE_API_KEY to Advanced Settings.")
    st.stop()

# Pydantic-like Schema
class MetadataSchema(typing_extensions.TypedDict):
    internal_title: str
    seo_page_title: str
    high_intent_tags: list[str]
    html_description: str
    meta_description: str

# System Instruction
system_instruction = """
You are an elite E-Commerce Architect for 'Roots & Paws Co.'
RULES:
1. SEO TITLE: [Style] + [Subject] + [Vibe] + [Product Type]. (Max 70 chars).
2. TAGS: 13 specific long-tail tags.
3. HTML: Use <h2>, <p>, and <ul> with 3-5 <li> elements. Turn features into emotional benefits.
4. BANNED WORDS: "cheap", "diy", "discount", "bargain".
5. TONE: Premium, Nostalgic, Holistic.
6. OUTPUT ONLY VALID JSON.
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instruction,
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=MetadataSchema,
        temperature=0.4,
    )
)

# Sidebar Instructions
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/sprout.png", width=80)
    st.markdown("### 📋 SEO Studio Guide")
    st.info("""
    **İpucu:** Daha iyi sonuç için ürün özelliklerini virgülle ayırarak yazın. 
    Örn: 'Organik Pamuk, El yapımı, Lavanta Kokulu'
    """)
    st.divider()
    st.caption("Roots & Paws Co. | 2026 Internal Tool")

# Main UI
st.markdown('<p class="header-style">🌱 Roots & Paws | SEO Studio</p>', unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    st.markdown("#### 🛠️ Ürün Detayları")
    with st.container():
        product_name = st.text_input("Ürün Adı", placeholder="Örn: Cool Aunt Club T-Shirt")
        key_features = st.text_area("Ana Özellikler & Materyal", placeholder="Örn: %100 Pamuk, Vintage Gözlük İllüstrasyonu, Terracotta Renk", height=150)
        target_vibe = st.text_input("Hedef Kitle / Vibe", placeholder="Örn: Retro seven teyzeler, Anneler Günü hediyesi")
        
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("Sihri Başlat ✨")

with col2:
    if generate_btn:
        if not product_name or not key_features:
            st.warning("Lütfen en az Ürün Adı ve Özellikleri girin.")
        else:
            with st.spinner("Roots & Paws standartlarında SEO yazılıyor..."):
                prompt = f"Product: {product_name}\nFeatures: {key_features}\nVibe: {target_vibe}"
                try:
                    response = model.generate_content(prompt)
                    data = json.loads(response.text)
                    
                    st.markdown("#### ✅ Hazır Metadata")
                    
                    # Store Title
                    st.markdown("##### 📌 Mağaza Başlığı")
                    st.code(data["internal_title"], language="text")
                    
                    # SEO Title
                    st.markdown("##### 🔍 SEO Başlığı (Mike Rhodes)")
                    st.code(data["seo_page_title"], language="text")
                    
                    # Tags
                    st.markdown("##### 🏷️ 13 Stratejik Etiket")
                    tags_html = "".join([f'<span class="tag-item">{tag}</span>' for tag in data["high_intent_tags"]])
                    st.markdown(f'<div class="tag-container">{tags_html}</div>', unsafe_allow_html=True)
                    st.code(", ".join(data["high_intent_tags"]), language="text")
                    
                    # HTML Description
                    st.markdown("##### 📄 HTML Ürün Açıklaması")
                    st.code(data["html_description"], language="html")
                    with st.expander("👁️ Önizlemeyi Göster"):
                        st.markdown(f'<div style="background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #eee;">{data["html_description"]}</div>', unsafe_allow_html=True)
                    
                    # Meta Description
                    st.markdown("##### 📱 Google Meta Açıklama")
                    st.code(data["meta_description"], language="text")
                    
                except Exception as e:
                    st.error(f"Bir hata oluştu: {str(e)}")
    else:
        st.info("Sol taraftaki bilgileri doldurup butona bastığında sonuçlar burada görünecek.")
