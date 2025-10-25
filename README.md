# ⚖️ LegalEase — AI Contract Analyzer

> **Understand. Analyze. Protect.**  
> Empowering individuals and businesses to decode complex contracts using AI.

---

## 🚨 Problem Statement

Every day, people sign **contracts** — employment offers, NDAs, leases, vendor agreements — filled with **dense legal jargon** and **hidden risks**.  
Most individuals and startups lack the legal expertise or resources to interpret these documents accurately.  

💥 This leads to:
- Unintended legal obligations  
- Hidden financial liabilities  
- Breach of confidentiality or IP rights  

Traditional legal review is **slow, expensive, and inaccessible** — creating a massive gap between the legal and everyday world.

---

## 💡 Solution Overview

**LegalEase** is an **AI-powered web app** that makes contracts understandable, transparent, and safe.  
Using **Gemini Pro**, **Perplexity Pro**, and **open legal datasets**, it helps users:

- 🧾 **Upload and analyze** any contract (PDF, text, or image)
- 🧠 **Extract and classify clauses** by type (confidentiality, liability, etc.)
- 🚦 **Highlight risk levels** (High, Medium, Low)
- 🗣️ **Simplify legal terms** into plain English
- 💬 **Chat with the contract** using a conversational AI
- 📊 **Visualize clause insights** with risk dashboards
- 📚 **Learn from real-world clauses** using a public Kaggle dataset

LegalEase acts as your **personal legal assistant**, helping you understand and negotiate contracts confidently.

---

## 🏗️ System Architecture

               ┌────────────────────────────────────────────┐
               │                  User UI                   │
               │────────────────────────────────────────────│
               │  • Landing Page (Upload / Compare / Learn) │
               │  • Clause Insights Dashboard               │
               │  • AI Legal Chat (Ask LegalEase)           │
               │  • Analytics & Risk Visualizations         │
               └────────────────────────────────────────────┘
                                  │
                                  ▼
               ┌────────────────────────────────────────────┐
               │             Backend Layer (Free)            │
               │────────────────────────────────────────────│
               │  • Node.js + Express API                   │
               │  • File Upload (Multer)                    │
               │  • PDF/Text Extraction (pdf-parse)         │
               │  • OCR Support (Tesseract.js for images)   │
               │  • MongoDB Atlas (Free tier) for storage   │
               │  • AI Integration (Gemini / Perplexity)    │
               └────────────────────────────────────────────┘
                                  │
                                  ▼
               ┌────────────────────────────────────────────┐
               │        AI & Intelligence Layer              │
               │────────────────────────────────────────────│
               │  • Gemini Pro: Summarization, Risk Scoring  │
               │  • Perplexity API: Factual Verification     │
               │  • Kaggle Dataset: Fine-tuned prompts       │
               │  • Optional: Hugging Face legal models      │
               └────────────────────────────────────────────┘
                                  │
                                  ▼
               ┌────────────────────────────────────────────┐
               │             Data Layer (Free)               │
               │────────────────────────────────────────────│
               │  • Kaggle Contract Clauses Dataset          │
               │  • MongoDB Atlas (user analytics & logs)    │
               │  • JSON embeddings for RAG search           │
               └────────────────────────────────────────────┘



---

## ⚙️ Tech Stack (All Free Tools)

| Layer | Tools / Frameworks | Purpose |
|-------|--------------------|----------|
| **Frontend** | React + Tailwind CSS | Modern, responsive UI |
| | Framer Motion | Animations & smooth transitions |
| | Recharts | Visual risk analysis graphs |
| **Backend** | Node.js + Express.js | REST API & orchestration |
| | pdf-parse / Tesseract.js | Extract text from PDFs & images |
| **Database** | MongoDB Atlas (Free Tier) | Store history, users, analytics |
| **AI Layer** | Gemini Pro | Clause summarization & risk detection |
| | Perplexity Pro | Factual clause validation |
| | LangChain.js (optional) | RAG & clause similarity search |
| **Dataset** | [Kaggle Contract Clauses Dataset](https://www.kaggle.com/datasets/mohammedalrashidan/contracts-clauses-datasets/data) | Legal clause classification data |
| **Hosting** | Vercel / Netlify + Firebase Auth | Free, fast, secure hosting |

---

## 🧩 Key Features

| Feature | Description |
|----------|-------------|
| 🧾 **Upload Contract** | Upload PDF / DOCX / image; automatically extract text |
| 🧠 **Clause Intelligence** | AI detects and labels clauses by type |
| 🚦 **Risk Analyzer** | Color-coded risk scoring for each clause |
| 🗣️ **Plain English Summary** | Simplified explanation for non-lawyers |
| 💬 **Ask LegalEase Chat** | Chat with the contract using contextual AI |
| ⚖️ **Compare Contracts** | Compare two contracts for differences and risk |
| 📊 **Analytics Dashboard** | Visual graphs showing clause types & risk distribution |
| 📚 **Clause Explorer** | Learn from real clauses using Kaggle dataset |
| 🧠 **Smart Recommendations** | Suggests next steps for risky clauses |

---

## 🧠 How It Works

[User Uploads PDF or Image]
↓
[Backend Extracts Text via pdf-parse / OCR]
↓
[Gemini Pro Analyzes Clauses + Summarizes + Scores Risk]
↓
[Perplexity API Cross-verifies Clause Facts]
↓
[Insights + Risk Data Saved in MongoDB]
↓
[Frontend Displays Dashboard + Clause Cards + Chat]


---

## 🌐 UI Overview

### 🎯 Landing Page
- Clean, professional UI  
- Options:
  - Upload Contract
  - Compare Contracts
  - Explore Clause Library
  - Try AI Legal Chat  

### 📊 Dashboard
- Clause cards with:
  - Clause type tags
  - Risk color indicator
  - Simplified summary
  - “View Full Clause” button
- Recharts visual analytics for risk levels  

### 💬 Ask LegalEase
- Chat interface with context from user-uploaded contracts  
- Example:  
  > “Explain the confidentiality clause in simple terms”  
  > “Is this contract one-sided?”  

### 📚 Learning Hub
- Interactive clause samples from Kaggle dataset  
- Users can explore real contract examples by category  
- AI explains what each clause means  

---

## 🚀 Installation Guide

```bash
# Clone the repo
git clone https://github.com/<your-username>/LegalEase.git

# Go to project directory
cd LegalEase

# Install dependencies
npm install

# Run backend server
npm run server

# Run frontend
npm run dev

Environment Variables:

GEMINI_API_KEY=<your_key>
PERPLEXITY_API_KEY=<your_key>
MONGO_URI=<your_mongo_connection_string>
