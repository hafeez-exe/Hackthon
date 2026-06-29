<div align="center">
  <img src="https://raw.githubusercontent.com/jobingen/brand-assets/main/logo.png" alt="JobInGen Engine Logo" width="150" height="150">
  
  # JobInGen Enterprise: Brand Intelligence Platform (BIP)
  
  **An Autonomous, Event-Driven Multi-Agent AI Content Engine designed to scale student-focused recruitment marketing.**

  [![Python](https://img.shields.io/badge/Python-3.10+-1B4DFF?logo=python&logoColor=white)](#)
  [![Playwright](https://img.shields.io/badge/Playwright-Chromium-2EAD33?logo=playwright&logoColor=white)](#)
  [![SQLite](https://img.shields.io/badge/SQLite-State%20Store-003B57?logo=sqlite&logoColor=white)](#)
  [![Groq](https://img.shields.io/badge/Groq-Llama%203.1-F55036?logo=groq&logoColor=white)](#)

  *Engineered for the modern hiring landscape. Built to bypass ATS black holes.*
</div>

---

## Executive Summary

The **JobInGen Brand Intelligence Platform (BIP)** is a highly specialized, production-ready content orchestration engine built for the JobInGen AI Hackathon. Moving beyond primitive prompt-engineering, BIP deploys a robust network of specialized agents that autonomously calculate content deficits, draft copy, mathematically score brand alignment, and natively render HTML templates into pixel-perfect social assets.

This platform operates as a completely self-sustaining marketing architecture, actively bridging the gap between early-career technical talent and vetted hiring managers.

## 🔑 Core Technical Innovations

| Innovation | Description | Impact |
| :--- | :--- | :--- |
| **Mathematical Deficit Planning** | Reads historical distributions from a persistent SQLite operational store to calculate dynamic quotas (e.g., *40% Educate, 25% Opportunity*). | Ensures algorithmic brand equilibrium and prevents topic fatigue without human scheduling. |
| **Active Schema-Healing** | Intercepts LLM JSON drift (e.g., generating `headline` instead of `hook`) and forces it into strict Pydantic `CopyVariant` contracts. | Guarantees zero runtime crashes or silent formatting failures during autonomous runs. |
| **Generative PNG Rendering** | A headless Playwright Chromium agent that dynamically compiles Jinja2 parametric HTML/CSS into high-fidelity image assets. | Eliminates the need for manual design work or generic Canva templates. |
| **Interactive Visual Studio** | A completely integrated, real-time `contenteditable` dashboard that allows for direct CSS color manipulation and text editing on generated assets. | Empowers human-in-the-loop review with immediate, frictionless visual customization. |
| **10-Point Scoring Critic** | A dedicated agent that algorithmically scores every draft for Value Density, Brand Voice, Hook Strength, and applies a strict *Cringe Filter*. | Maintains a relentless, high-value, peer-to-peer tone and rejects corporate jargon. |

## ⚙️ The Orchestration Lifecycle

JobInGen BIP rejects the traditional "one-prompt" pipeline in favor of a strict **Single State Context** model. Data moves systematically through isolated intelligence nodes:

1. **The Math (Planner):** Analyzes the SQLite state store, identifies the largest structural deficit in the content matrix, and formulates a strategic blueprint.
2. **The Draft (Copywriter):** "Gen," our primary Llama 3.1 8b agent, generates deep, actionable A/B variants targeted directly at bypassing applicant tracking systems.
3. **The Audit (Critic):** The 10-point scoring matrix evaluates the variants. If a draft scores below threshold, it is actively rejected and routed back for a rewrite.
4. **The Canvas (Renderer):** The approved state object is injected into responsive Jinja2 templates, rendering pixel-perfect PNG graphics via Playwright.

## 🚀 Roadmap & Feature Improvements

As we scale the JobInGen Enterprise Engine, the following capabilities are scheduled for development:

- [ ] **Cross-Platform Syndication:** Direct API integration with LinkedIn and Instagram for zero-click autonomous publishing based on optimal engagement windows.
- [ ] **Semantic Vector Search:** Upgrading the SQLite store to a vector database (e.g., Pinecone/Chroma) to match generated content against deeply specialized technical skill trees.
- [ ] **A/B Performance Loop:** Ingesting live engagement telemetry (impressions, CTR) back into the Critic agent to dynamically weight scoring algorithms based on real-world performance.
- [ ] **Multi-Brand Toggling:** Expanding the Interactive Visual Studio to support dynamic, instantaneous multi-tenant brand kit swapping for enterprise agencies.

## 🛠️ Deployment Instructions

### Prerequisites
- Python 3.10+
- Node.js (for syntax tooling, optional)

### Installation
```bash
git clone https://github.com/hafeez-exe/Hackthon.git
cd Hackthon

# Initialize environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install core dependencies and browser engine
pip install -r requirements.txt
playwright install chromium
```

### Environment Configuration
Provide your inference keys in a `.env` file at the root:
```env
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key_for_blazing_fast_inference
```

### Ignition
```bash
python app.py
```
*Access the Glassmorphic Command Center at `http://127.0.0.1:8000`*

---
<div align="center">
  <i>Built with relentless precision. Stop applying. Start bypassing.</i><br>
  <b>Designed for the JobInGen AI Hackathon</b>
</div>
