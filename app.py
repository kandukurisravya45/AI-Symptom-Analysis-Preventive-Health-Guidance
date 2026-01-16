import streamlit as st
import json
from datetime import datetime
import re

# ============================================================================
# KNOWLEDGE BASE (RAG COMPONENT - Local Dictionary)
# ============================================================================
KNOWLEDGE_BASE = {
    "common_cold": {
        "keywords": ["cold", "runny nose", "sneezing", "nasal congestion", "cough"],
        "condition_name": "Common Cold",
        "possible_related": ["Viral Infection", "Upper Respiratory Infection"],
        "preventive_advice": [
            "Maintain proper hydration: Drink 8-10 glasses of water daily",
            "Ensure adequate rest: Sleep 7-9 hours per night to boost immunity",
            "Practice hand hygiene: Wash hands frequently with soap and water",
            "Use a humidifier to relieve nasal congestion",
            "Eat vitamin C-rich foods: citrus fruits, berries, and leafy greens",
            "Avoid crowded places during acute symptoms to prevent spread"
        ],
        "when_to_consult_doctor": "If symptoms persist beyond 10 days or worsen significantly"
    },
    "influenza": {
        "keywords": ["flu", "fever", "body aches", "chills", "fatigue", "muscle pain"],
        "condition_name": "Influenza (Flu)",
        "possible_related": ["Viral Illness", "Systemic Infection"],
        "preventive_advice": [
            "Get annual flu vaccination (most effective prevention method)",
            "Practice respiratory hygiene: Cover coughs and sneezes",
            "Avoid touching face, eyes, and nose unnecessarily",
            "Stay home when sick to prevent transmission to others",
            "Maintain balanced nutrition with protein and micronutrients",
            "Stay physically active with moderate exercise (30 mins daily)"
        ],
        "when_to_consult_doctor": "Seek immediate medical attention if experiencing difficulty breathing or severe symptoms"
    },
    "allergies": {
        "keywords": ["allergy", "allergic", "itching", "hay fever", "hives", "rash", "itch"],
        "condition_name": "Allergic Reaction",
        "possible_related": ["Seasonal Allergies", "Environmental Sensitivity"],
        "preventive_advice": [
            "Identify and avoid known allergen triggers",
            "Keep living spaces clean: Regular vacuuming and dusting",
            "Use HEPA air filters to reduce airborne allergens",
            "Wash bedding regularly in hot water",
            "Monitor pollen forecasts and limit outdoor time on high pollen days",
            "Use natural remedies: Quercetin-rich foods, saline nasal drops"
        ],
        "when_to_consult_doctor": "If allergic reactions are severe, persistent, or affect daily activities"
    },
    "headache": {
        "keywords": ["headache", "head pain", "migraine", "throbbing", "pressure"],
        "condition_name": "Headache",
        "possible_related": ["Tension Headache", "Dehydration-related Discomfort"],
        "preventive_advice": [
            "Stay well-hydrated: Drink at least 8 glasses of water daily",
            "Manage stress through meditation, yoga, or breathing exercises",
            "Maintain consistent sleep schedule: 7-9 hours nightly",
            "Limit caffeine intake, especially in afternoons and evenings",
            "Take regular screen breaks: Follow 20-20-20 rule (every 20 mins, look away for 20 secs)",
            "Engage in regular physical activity to improve circulation"
        ],
        "when_to_consult_doctor": "If headaches are sudden, severe, or accompanied by vision changes or confusion"
    },
    "fatigue": {
        "keywords": ["fatigue", "tired", "exhaustion", "low energy", "weakness"],
        "condition_name": "Fatigue",
        "possible_related": ["Sleep Deprivation", "Nutrient Deficiency"],
        "preventive_advice": [
            "Prioritize sleep: Maintain 7-9 hours consistent sleep schedule",
            "Eat balanced meals: Include protein, complex carbs, and healthy fats",
            "Exercise regularly: 30 minutes of moderate activity daily",
            "Reduce caffeine consumption, especially in evenings",
            "Practice stress management: Meditation, journaling, or relaxation",
            "Ensure adequate hydration throughout the day"
        ],
        "when_to_consult_doctor": "If fatigue persists for more than 2 weeks despite adequate rest and nutrition"
    },
    "gastrointestinal": {
        "keywords": ["stomach", "nausea", "vomiting", "diarrhea", "cramps", "indigestion", "abdominal"],
        "condition_name": "Gastrointestinal Discomfort",
        "possible_related": ["Gastroenteritis", "Food Intolerance"],
        "preventive_advice": [
            "Eat small, frequent meals rather than large heavy ones",
            "Avoid spicy, greasy, and processed foods",
            "Stay hydrated with water and electrolyte solutions",
            "Include probiotic-rich foods: yogurt, fermented vegetables, kefir",
            "Practice proper food safety: Wash hands and cook food thoroughly",
            "Chew food slowly and thoroughly for proper digestion"
        ],
        "when_to_consult_doctor": "If symptoms persist beyond 3 days or if there is severe pain"
    }
}

# ============================================================================
# NLP PREPROCESSING & RAG MATCHING
# ============================================================================
def preprocess_text(text):
    """Convert text to lowercase and remove punctuation"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def calculate_match_score(user_input, condition_keywords):
    """
    Calculate symptom match score using keyword intersection
    Score = (matched keywords / total keywords) * 100
    This is the RAG retrieval mechanism
    """
    processed_input = set(preprocess_text(user_input).split())
    keywords_set = set([kw.lower() for kw in condition_keywords])
    
    matched = processed_input.intersection(keywords_set)
    
    if not matched:
        return 0, []
    
    score = (len(matched) / len(keywords_set)) * 100
    return round(score, 1), list(matched)

def retrieve_matching_conditions(user_input):
    """
    RAG Process: Retrieve conditions from knowledge base that match user input
    Returns sorted list of conditions with match scores
    """
    matches = []
    
    for condition_key, condition_data in KNOWLEDGE_BASE.items():
        score, matched_keywords = calculate_match_score(
            user_input, 
            condition_data["keywords"]
        )
        
        if score > 0:
            matches.append({
                "key": condition_key,
                "name": condition_data["condition_name"],
                "match_score": score,
                "matched_keywords": matched_keywords,
                "data": condition_data
            })
    
    # Sort by match score (highest first)
    matches.sort(key=lambda x: x["match_score"], reverse=True)
    return matches

# ============================================================================
# STREAMLIT APP CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Symptom Analysis System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better appearance
st.markdown("""
    <style>
    .disclaimer-box {
        background-color: #fff3cd;
        border-left: 4px solid #ff6b6b;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# APP HEADER
# ============================================================================
st.title("🏥 AI-Powered Symptom Analysis & Preventive Health Guidance System")
st.markdown("---")

# ============================================================================
# CRITICAL DISCLAIMER (MANDATORY - NON-NEGOTIABLE)
# ============================================================================
st.warning(
    "⚠️ **IMPORTANT MEDICAL DISCLAIMER**\n\n"
    "**This system is for INFORMATIONAL and PREVENTIVE GUIDANCE ONLY.**\n\n"
    "This system does NOT:\n"
    "• Provide medical diagnosis or substitute for diagnosis\n"
    "• Replace professional medical advice from healthcare providers\n"
    "• Constitute medical treatment or advice\n"
    "• Guarantee accuracy of any analysis\n\n"
    "**Always consult a licensed healthcare professional for diagnosis and treatment.**\n\n"
    "**For emergencies, call emergency services immediately.**"
)

st.markdown("---")

# ============================================================================
# MAIN INTERFACE
# ============================================================================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Describe Your Symptoms")
    st.caption("Enter symptoms in your own words (e.g., 'I have a runny nose and keep sneezing')")
    
    user_input = st.text_area(
        label="Your symptoms:",
        placeholder="Describe your symptoms here...",
        height=120,
        label_visibility="collapsed"
    )

with col2:
    st.subheader("ℹ️ System Overview")
    with st.info("**AI Methods Used:**"):
        st.markdown("""
        • **NLP**: Text preprocessing  
        • **RAG**: Knowledge base retrieval  
        • **Rule-Based**: Match scoring  
        
        **Output**: Preventive guidance only (NOT diagnosis)
        """)

st.markdown("---")

# ============================================================================
# ANALYSIS BUTTON & RESULTS
# ============================================================================
if st.button("🔍 Analyze Symptoms", use_container_width=True, type="primary"):
    
    if not user_input.strip():
        st.error("❌ Please enter your symptoms to proceed.")
    
    else:
        st.subheader("📊 Analysis Results")
        
        # Step 1: Input Display
        st.write("**STEP 1: Input Received**")
        st.info(f"'{user_input}'")
        
        # Step 2: RAG Retrieval
        st.write("**STEP 2: Knowledge Base Retrieval (RAG Process)**")
        
        matches = retrieve_matching_conditions(user_input)
        
        if not matches:
            st.warning(
                "⚠️ No matching information found in our knowledge base.\n\n"
                "**Please consult a healthcare professional for proper assessment.**"
            )
        
        else:
            st.success(f"✅ Found {len(matches)} potential match(es)")
            
            # Display top matches
            for idx, match in enumerate(matches[:3], 1):
                with st.container():
                    col_cond, col_score = st.columns([3, 1])
                    
                    with col_cond:
                        st.markdown(f"**Match {idx}: {match['name']}**")
                    with col_score:
                        st.metric("Match Score", f"{match['match_score']}%")
                    
                    st.caption(
                        f"Matching keywords: {', '.join(match['matched_keywords'])}"
                    )
            
            # Step 3: Preventive Guidance
            st.write("**STEP 3: Preventive Health Guidance**")
            
            top_match = matches[0]
            
            st.success(
                f"**Based on your input, we identified relevant information about: {top_match['name']}**"
            )
            
            st.subheader("💡 Suggested Preventive Actions:")
            for i, advice in enumerate(top_match['data']['preventive_advice'], 1):
                st.write(f"{i}. {advice}")
            
            st.warning(
                f"🔴 **Medical Consultation Recommended:** {top_match['data']['when_to_consult_doctor']}"
            )
        
        st.markdown("---")
        st.caption(
            f"Analysis generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
            f"System: AI-Symptom Analysis v1.0 (Informational Only)"
        )

# ============================================================================
# SIDEBAR: EDUCATIONAL INFORMATION
# ============================================================================
with st.sidebar:
    st.title("ℹ️ About This System")
    
    st.subheader("🔬 AI Workflow")
    st.markdown("""
    1. **Input**: User describes symptoms in natural language
    2. **NLP Processing**: Text preprocessing and tokenization
    3. **RAG Retrieval**: Symptoms matched against knowledge base
    4. **Scoring**: Calculate match percentage (0-100%)
    5. **Output**: Retrieve preventive advice (NOT diagnosis)
    """)
    
    st.subheader("🧠 AI Techniques Explained")
    with st.expander("Natural Language Processing (NLP)"):
        st.write(
            "NLP processes user text by converting it to lowercase, removing punctuation, "
            "and breaking it into individual words. This allows the system to identify key terms."
        )
    
    with st.expander("Retrieval-Augmented Generation (RAG)"):
        st.write(
            "RAG retrieves relevant information from a local knowledge base. "
            "Instead of generating new text, it matches user input against pre-defined "
            "conditions and retrieves curated, safe, non-diagnostic guidance."
        )
    
    with st.expander("Rule-Based Scoring"):
        st.write(
            "A simple rule-based system calculates match scores: "
            "(Number of matched keywords) / (Total keywords for condition) × 100. "
            "Higher scores indicate better relevance."
        )
    
    st.subheader("❓ FAQ")
    with st.expander("Is this a diagnosis tool?"):
        st.write("❌ No. This provides informational guidance only, not diagnosis.")
    
    with st.expander("Can I replace my doctor?"):
        st.write("❌ No. Always consult healthcare professionals for diagnosis and treatment.")
    
    with st.expander("How accurate is this?"):
        st.write(
            "This system is designed for educational and preventive guidance, "
            "not clinical accuracy. Match scores indicate relevance, not medical certainty."
        )
    
    with st.expander("What conditions are covered?"):
        conditions = ", ".join([cond['condition_name'] for cond in KNOWLEDGE_BASE.values()])
        st.write(f"Current coverage: {conditions}")
    
    st.divider()
    
    st.subheader("🌍 SDG Alignment")
    st.markdown("""
    **SDG 3: Good Health and Well-Being**
    
    This project promotes:
    • Early health awareness
    • Preventive care practices
    • Accessible health information
    • Responsible AI in healthcare
    """)
    
    st.caption("Project: 1M1B AI for Sustainability Virtual Internship")
    st.caption("Version: 1.0 | Status: Educational & Informational")