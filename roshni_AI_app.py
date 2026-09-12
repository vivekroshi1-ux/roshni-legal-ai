import streamlit as st
import json
import os

# ==========================================
# 1. ब्रांडिंग एवं पेज सेटअप (App Configuration)
# ==========================================
st.set_page_config(
    page_title="रोशनी: द लाइट - Roshni Legal AI",
    page_icon="💡",
    layout="wide"
)

# ==========================================
# 2. डेटाबेस इनिशियलाइज़ेशन (Data Layer)
# ==========================================
def get_roshni_database():
    return [
        {
            "id": "CONST_ART_21",
            "type": "statute",
            "source": "भारतीय संविधान (Constitution of India)",
            "reference": "अनुच्छेद 21 (Article 21)",
            "title": "प्राण और दैहिक स्वतंत्रता का संरक्षण",
            "content": "किसी भी व्यक्ति को उसके प्राण या दैहिक स्वतंत्रता से विधि द्वारा स्थापित प्रक्रिया के अनुसार ही वंचित किया जाएगा, अन्यथा नहीं।",
            "keywords": ["जीवन", "स्वतंत्रता", "निजता", "privacy", "liberty", "डेटा"],
            "is_active": True
        },
        {
            "id": "BNS_SEC_103",
            "type": "statute",
            "source": "भारतीय न्याय संहिता (BNS), 2023",
            "reference": "धारा 103 (Section 103)",
            "title": "हत्या के लिए दंड",
            "content": "जो कोई भी हत्या करेगा, उसे मृत्युदंड या आजीवन कारावास से दंडित किया जाएगा और वह जुर्माने के लिए भी उत्तरदायी होगा।",
            "keywords": ["हत्या", "खून", "murder", "death"],
            "is_active": True
        },
        {
            "id": "CASE_SC_2017_PUTTASWAMY",
            "type": "judgment",
            "source": "उच्चतम न्यायालय (Supreme Court of India)",
            "reference": "(2017) 10 SCC 1 - के.एस. पुट्टस्वामी बनाम भारत संघ",
            "title": "निजता का अधिकार मौलिक अधिकार है",
            "content": "सुप्रीम कोर्ट की 9 जजों की संवैधानिक पीठ ने सर्वसम्मति से यह निर्णय दिया कि निजता का अधिकार (Right to Privacy) संविधान के अनुच्छेद 21 के तहत एक मौलिक अधिकार है।",
            "keywords": ["निजता", "privacy", "डेटा लीक", "leak", "गुप्त"],
            "is_active": True
        }
    ]

# ==========================================
# 3. कोर प्रोसेसिंग इंजन (Safe AI & Search Logic)
# ==========================================
def roshni_legal_engine(user_query):
    database = get_roshni_database()
    query_lower = user_query.lower().strip()
    
    matched_statutes = []
    matched_judgments = []
    
    for item in database:
        # केवल सक्रिय और वैध कानूनों/फैसलों को शामिल करना
        if not item.get("is_active", True):
            continue
            
        for kw in item.get("keywords", []):
            if kw in query_lower:
                if item["type"] == "statute":
                    matched_statutes.append(item)
                elif item["type"] == "judgment":
                    matched_judgments.append(item)
                break
                
    return matched_statutes, matched_judgments

# ==========================================
# 4. यूज़र इंटरफ़ेस (UI & Header Layout)
# ==========================================
st.markdown("""
    <div style='text-align: center; padding: 10px; background-color: #f0f2f6; border-radius: 10px;'>
        <h1 style='color: #1E3A8A; margin-bottom: 0;'>💡 रोशनी: द लाइट (Roshni: The Light)</h1>
        <h4 style='color: #4B5563; margin-top: 5px;'>भारतीय संविधान | भारतीय न्याय संहिता (BNS) | न्यायालय निर्णय</h4>
        <p style='font-style: italic; color: #6B7280;'> "संविधान, न्याय संहिता और अदालती फैसलों से जलती न्याय की मशाल।"</p>
    </div>
    <br>
""", unsafe_allow_html=True)

# इनपुट बॉक्स
user_problem = st.text_area(
    "आपकी कानूनी समस्या या सवाल:",
    placeholder="उदाहरण: बिना मेरी अनुमति के कोई मेरा व्यक्तिगत डेटा सार्वजनिक कर रहा है, क्या यह अपराध है?",
    height=120
)

col1, col2 = st.columns([1, 5])
with col1:
    search_button = st.button("समाधान खोजें", type="primary", use_container_width=True)

# ==========================================
# 5. परिणाम प्रदर्शन (Output Section)
# ==========================================
if search_button:
    if not user_problem.strip():
        st.warning("कृपया पहले अपनी समस्या यहाँ दर्ज करें।")
    else:
        with st.spinner("रोशनी AI संविधान, BNS और कोर्ट के ऐतिहासिक फैसलों का विश्लेषण कर रहा है..."):
            statutes, judgments = roshni_legal_engine(user_problem)
            
            if not statutes and not judgments:
                st.info(
                    "🔍 **सत्यापित जानकारी उपलब्ध नहीं है:** आपकी समस्या से संबंधित सटीक धारा या निर्णय हमारे वर्तमान डेटाबेस में नहीं मिला। "
                    "गलत या मनगढ़ंत उत्तर से बचाने के लिए 'रोशनी AI' केवल सत्यापित डेटा प्रदर्शित करता है। कृपया किसी पंजीकृत वकील से संपर्क करें।"
                )
            else:
                st.success("आपकी समस्या का कानूनी विश्लेषण:")
                
                # संविधान एवं BNS धाराएं
                if statutes:
                    st.subheader("📜 संबंधित संविधान एवं न्याय संहिता की धाराएं")
                    for st_item in statutes:
                        with st.expander(f"{st_item['source']} - {st_item['reference']}: {st_item['title']}", expanded=True):
                            st.write(st_item["content"])
                
                # सुप्रीम कोर्ट / हाई कोर्ट के फैसले
                if judgments:
                    st.subheader("🏛️ न्यायपालिका के ऐतिहासिक फैसले (Case Laws / Precedents)")
                    for j_item in judgments:
                        with st.expander(f"{j_item['source']} - {j_item['reference']}", expanded=True):
                            st.write(f"**विषय:** {j_item['title']}")
                            st.write(f"**निर्णय सार:** {j_item['content']}")
                
                # कानूनी अस्वीकरण (Mandatory Safety Guardrail)
                st.markdown("---")
                st.warning(
                    "⚠️ **कानूनी अस्वीकरण (Disclaimer):** 'रोशनी: द लाइट' द्वारा दी गई जानकारी केवल प्राथमिक कानूनी मार्गदर्शन और जागरूकता के लिए है। "
                    "इसे किसी पंजीकृत अधिवक्ता (Advocate) की आधिकारिक कानूनी सलाह का विकल्प न मानें।"
                )
