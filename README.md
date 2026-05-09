# Saarthi AI: Right Scheme, Bright Dream. 🦋

> **Bridging citizens with government opportunities while creating micro-employment ecosystems.**

![Saarthi AI Banner](frontend/img/hero_bg.jpg)

## 📌 Project Overview
Millions of citizens miss out on life-changing government resources because information is scattered, forms are complex, eligibility rules are confusing, and many face language or digital literacy barriers. 

**Saarthi** is a multilingual AI + human-assisted platform that bridges the gap between citizens and government resources. Unlike normal portals or chatbots, Saarthi does not just provide information — **it helps users complete the full application workflow.**

---

## 💡 The Core Problem & Our Solution
* **The Problem:** Citizens don't know what schemes they are eligible for or how to apply for them. Language barriers and digital illiteracy prevent them from accessing welfare.
* **The Solution:** An AI engine that matches citizens to schemes in their native language (via voice or text), coupled with a human "Saarthi Assistant" marketplace where local digital helpers physically assist them in filling out forms.

---

## 💰 "Earn While Helping": Our Unique Micro-Employment USP
Saarthi’s biggest USP is its AI + human-assisted **micro-employment model**. 
It helps users find government schemes, jobs, scholarships, funding, welfare benefits, and public services. At the same time, it creates earning opportunities for:
- Students
- Rural youth
- Freelancers
- Women working from home
- NGO volunteers
- Local digital helpers

**How it works:** 
The user pays a micro-fee (e.g., ₹50) for guided application assistance. The local Saarthi Assistant earns ₹35, and the platform keeps a ₹15 service margin. 
*“Saarthi turns public service access into a micro-employment ecosystem. Helping citizens apply, helping assistants earn.”*

---

## ⚙️ How Saarthi Works (User Workflow)
1. **Enter Need 🎙️:** User describes what they want via voice or text in their native language.
2. **AI Matches Schemes 🤖:** AI identifies language, location, occupation, and maps it to the exact government scheme.
3. **Check Eligibility ✅:** Platform instantly verifies eligibility criteria.
4. **Request Assistant 👨🏽‍💼:** User requests a local trained assistant for form-filling help.
5. **DigiLocker Verify 🔐:** User securely authenticates documents.
6. **Form Filled 📝:** Assistant remotely or physically helps fill the required forms.
7. **Admin Review 👁️:** Quality check by platform admins.
8. **User OTP Consent 📱:** User provides final OTP consent before submission.
9. **Final Submission 🚀:** Application is submitted to the government portal.

---

## 🚀 Platform Core Features
1. **AI Opportunity Finder:** Finds relevant schemes, jobs, scholarships, welfare programs, and public services.
2. **Eligibility Checker:** Checks eligibility and explains the result in simple language.
3. **Human Assistant Marketplace:** Connects users with trained assistants for form filling and application support.
4. **Multilingual & Voice Support:** Supports English, Hindi, Kannada, Tamil, Telugu, Malayalam, Marathi, Bengali, Gujarati, Punjabi, and Odia.
5. **Smart Dashboard:** Amazon-style tracking for applications, deadlines, documents, and tasks.
6. **Income Generation:** Creates micro-employment opportunities for trained helpers.
7. **Trust & Safety Layer:** Consent-first workflows, OTP approvals, verified assistants, and strict NDAs.
8. **Feedback Learning System:** Captures user feedback to constantly improve AI recommendations.

---

## 🏛️ Scheme Categories Covered
* **🎓 Education & Jobs:** Scholarships, skill programs, student support.
* **📈 Finance & Business:** MSME loans, startup funding, Mudra loans, women entrepreneurship schemes.
* **🌾 Agriculture:** Farmer subsidies, crop insurance, agri-loans.
* **🏥 Health:** Medical schemes, insurance, hospital aid.
* **🍲 Food & Welfare:** Ration support, nutrition programs.
* **🤝 Community & Social:** NGO grants, disability support, senior citizen welfare.
* **🏛️ Public Services:** Legal aid, digital citizen services.

---

## 🛡️ Trust & Safety Model
Data privacy is paramount when dealing with government documents. Saarthi enforces:
1. **Consent-First Workflow:** User consent is required before document verification.
2. **OTP Approval:** Required before final submission to government portals.
3. **Certified Assistants:** Only ID-verified and trained assistants can operate on the platform.
4. **Strict NDAs:** Assistants face strict legal consequences and permanent bans for data leakage.
5. **No Data Hoarding:** No unnecessary storage of sensitive documents on Saarthi servers.

---

## 💻 Tech Stack & Architecture (MVP)
The MVP is built for speed, performance, and cross-platform compatibility:
* **Frontend:** Vanilla JS, HTML5, Modern CSS with Glassmorphism, Web Speech API (Voice-to-Text).
* **Backend:** Python (Flask).
* **AI Engine:** Google Gemini (gemini-2.5-flash) for intent extraction, eligibility mapping, and conversational guidance.
* **Localization:** Sarvam AI for native Indic language translation.
* **Database:** Local JSON (simulating MongoDB for the Hackathon MVP).

---

## 🔧 Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/saarthi-ai.git
   cd saarthi-ai
   ```

2. **Set up Python Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_google_ai_studio_api_key
   SARVAM_API_KEY=your_sarvam_translation_api_key
   ```

4. **Run the Application**
   ```bash
   python main.py
   ```
   Open `http://localhost:5000` in your browser.

---

## 🎯 Hackathon Demo Flow
1. Load `http://localhost:5000`. Show the beautiful glassmorphic landing page.
2. Click **Login/Register** to show the Auth Modal workflow.
3. Scroll to **Discover Schemes**. Use the Voice Mic 🎙️ to say *"I need a bike loan"*.
4. Watch the AI instantly match the query to the **Personal Two-Wheeler Loan** scheme and light it up in bright green.
5. Show the **Available Assistants** marketplace.
6. Open the **Assistant Dashboard** to show the live Amazon-style delivery tracker progressing from "Requested" to "Delivered".
7. Click the **Floating AI Chatbot** widget to have a conversational summary of the website in regional languages.

---

Built with ❤️ for social impact.
