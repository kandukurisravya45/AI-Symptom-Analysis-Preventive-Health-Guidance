# AI-Powered Symptom Analysis & Preventive Health Guidance System

## 🎯 Project Overview

An intelligent system that analyzes user-described symptoms and provides **evidence-based preventive health guidance** using Natural Language Processing (NLP) and Retrieval-Augmented Generation (RAG) principles. Aligned with **SDG 3: Good Health and Well-Being**.

**Problem Addressed:** Many individuals ignore initial symptoms or rely on unverified online sources, delaying medical attention. This system bridges the gap between symptom onset and professional consultation by providing responsible, preliminary health awareness.

---

## ⚠️ CRITICAL DISCLAIMER

This system:
- **DOES NOT provide medical diagnosis**
- **DOES NOT replace professional healthcare advice**
- **DOES NOT substitute for consultation with a licensed healthcare provider**

**Always seek professional medical help for symptoms requiring diagnosis or treatment.**

---

## 🚀 Features

✅ User-friendly symptom input interface  
✅ NLP-based symptom matching  
✅ RAG-powered knowledge base retrieval  
✅ Confidence scoring for matched conditions  
✅ Preventive health guidance (non-diagnostic)  
✅ Clear "when to see a doctor" indicators  
✅ Ethical safeguards and disclaimers  

---

## 🏗️ How It Works

### 1. **Input Phase**
- User enters symptoms in natural language
- Example: "I have a runny nose and keep sneezing"

### 2. **NLP Processing**
- Text preprocessing (lowercase, punctuation removal)
- Tokenization into words

### 3. **RAG Matching**
- Input keywords matched against internal medical knowledge base
- Confidence scoring: (matched keywords) / (total keywords)
- Top matches retrieved and ranked

### 4. **Guidance Generation**
- Preventive advice retrieved from knowledge base
- "When to see a doctor" guidance provided
- Results displayed with confidence levels

---

## 📊 AI Methodology

### Techniques Used:
- **Natural Language Processing**: Text analysis and keyword extraction
- **Retrieval-Augmented Generation**: Knowledge base retrieval without ML training
- **Rule-Based Logic**: Transparent, explainable decision making
- **Confidence Scoring**: Prevents false positives

### Why This Approach?
✓ Explainable AI (no black box)  
✓ Ethical and safe,  
✓ Quick and lightweight  
✓ Easy to audit and improve  
✓ No risk of biased ML models  

---

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Steps

1. Clone the repository:
```bash
git clone https://github.com/Shaikirfan007/AI-Symptom-Analysis-Preventive-Health-Guidance.git
cd AI-Symptom-Analysis-Preventive-Health-Guidance
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run app.py
```

5. Open your browser to `http://localhost:8501`

---

## 💡 Usage Example

**Input:**
"I have a runny nose, sneezing, and a mild cough"

**Output:**
The system identifies relevant information related to the common cold and provides preventive health guidance along with advice on when to consult a doctor.

