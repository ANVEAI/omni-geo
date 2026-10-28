# OmniGEO: Generative Engine Optimization & AI Search Audit Platform

> **The Turnkey Zero-Investment Startup Machine for the AI Search Era.**  
> Audit how brands appear in **ChatGPT Search, Perplexity AI, Google Gemini, and Anthropic Claude**, quantify competitor pipeline displacement, and sell **$2,500 – $5,000/mo** remediation engagements with zero upfront capital.

---

## 🎯 Executive Overview: Why GEO Right Now?

Traditional organic Google search traffic is declining rapidly as enterprise decision-makers and consumers transition to **Generative AI Search Engines**.

When prospective buyers prompt:
* *"What is the best modern issue tracking software for startups?"*
* *"Compare top cloud databases with native PostgreSQL support in 2026"*
* *"Which corporate card platform has the lowest FX fees and best accounting integrations?"*

**Only 2 to 3 vendors are cited and recommended.** If a brand is omitted from that generated response, they lose the deal before an inbound lead is ever generated.

**OmniGEO** is a full-stack, enterprise-grade software and agency operational suite that:
1. **Audits Technical AI Crawlability**: Scans `robots.txt` for `GPTBot`, `ClaudeBot`, `PerplexityBot`, and checks `/llms.txt` compliance.
2. **Inspects Semantic Knowledge Graphs**: Analyzes JSON-LD Schema.org entities and `sameAs` linkage to Wikidata and Crunchbase.
3. **Simulates Multi-Model Prompt Share of Voice (SOV)**: Evaluates visibility and recommendation rank across ChatGPT, Perplexity, Gemini, and Claude.
4. **Calculates Pipeline at Risk**: Computes financial loss in hard dollars based on monthly commercial query volume and competitor leakage.
5. **Generates Executable 30-Day Blueprints**: Generates pre-written `/llms.txt`, `robots.txt`, JSON-LD Schema snippets, and digital PR plays ready for deployment.
6. **Includes a Complete High-Ticket GTM Sales Machine**: Cold outreach sequences, 3-minute Loom teardown scripts, high-ticket proposals, contracts, and fulfillment playbooks.

---

## 🚀 Quick Start (Single Command)

```bash
cd /Users/adarshkant/.gemini/antigravity/scratch/geo-audit-platform
./run.sh
```

Then open your browser:
* **Flagship SaaS Website & Instant Scanner**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **SaaS Application Workspace**: [http://127.0.0.1:8000/dashboard](http://127.0.0.1:8000/dashboard)
* **Free /llms.txt Builder Tool**: [http://127.0.0.1:8000/tools/llms-txt-generator](http://127.0.0.1:8000/tools/llms-txt-generator)
* **Live AI Bot robots.txt Inspector**: [http://127.0.0.1:8000/tools/robots-txt-tester](http://127.0.0.1:8000/tools/robots-txt-tester)
* **SaaS Pricing & Plan Matrix**: [http://127.0.0.1:8000/pricing](http://127.0.0.1:8000/pricing)
* **Benchmark Audit Report (Print to PDF)**: [http://127.0.0.1:8000/report/audit_linear_sample](http://127.0.0.1:8000/report/audit_linear_sample)
* **Turnkey Agency GTM Sales Kit**: [http://127.0.0.1:8000/gtm-kit](http://127.0.0.1:8000/gtm-kit)

---

## 📁 Architecture & File Layout

```text
geo-audit-platform/
├── app.py                          # FastAPI backend application & API routes
├── core/
│   ├── crawler.py                  # Live robots.txt, llms.txt & JSON-LD crawler
│   ├── citation_checker.py         # Wikidata, Reddit & review platform footprint analyzer
│   ├── llm_evaluator.py            # Multi-model evaluation across ChatGPT, Perplexity, Gemini, Claude
│   ├── scoring.py                  # 4-Pillar GEO scoring algorithm & pipeline risk calculator
│   ├── remediation.py              # Dynamic 30-day action plan & code asset generator
│   └── sample_generator.py         # Benchmark audit datasets (Linear, Supabase, Brex)
├── templates/
│   ├── index.html                  # High-converting SaaS marketing website & scanner
│   ├── dashboard.html              # SaaS workspace managing monitored domains & audits
│   ├── report.html                 # Executive presentation report (with print-to-PDF styles)
│   ├── tools_llms_txt.html         # Interactive /llms.txt builder & downloader
│   ├── tools_robots_txt.html       # Live AI crawler robots.txt inspector
│   ├── pricing.html                # SaaS pricing plans, annual toggle & feature matrix
│   └── gtm_kit.html                # Turnkey sales scripts, proposals, and contracts
├── static/
│   ├── style.css                   # Custom styling & @media print PDF layout rules
│   └── app.js                      # Dynamic forms, progress animations & clipboard tools
├── gtm_kit/
│   ├── 01_COLD_OUTREACH_PLAYBOOK.md         # Word-for-word 3-min Loom scripts & cold emails
│   ├── 02_HIGH_TICKET_PROPOSAL_TEMPLATE.md  # $2,500 Audit + $5,000/mo Retainer proposal
│   ├── 03_STATEMENT_OF_WORK_CONTRACT.md     # Production service agreement & SOW contract
│   ├── 04_30_DAY_FULFILLMENT_PLAYBOOK.md    # Internal agency execution manual for client delivery
│   └── 05_SALES_DECK_PITCH_FRAMEWORK.md    # 10-slide sales deck presentation script
├── run.sh                          # One-click startup script
└── README.md                       # Complete documentation and operational guide
```

---

## 💼 The Zero-Capital Business Model (How to Monetize)

| Step | Action | Time Needed | Output |
| :--- | :--- | :--- | :--- |
| **1. Target** | Pick 20 B2B companies in a high-ticket niche (SaaS, FinTech, Cyber, MedTech) | 30 Mins | Target prospect list |
| **2. Audit** | Run their URL through OmniGEO | 15 Secs per audit | Executive report showing competitor SOV lead |
| **3. Outreach** | Record a 3-minute Loom video using the `01_COLD_OUTREACH_PLAYBOOK.md` script | 3 Mins per prospect | Sent via LinkedIn InMail or Cold Email |
| **4. Close** | Present findings on Zoom using `05_SALES_DECK_PITCH_FRAMEWORK.md` | 25 Mins | Signed SOW (`03_STATEMENT_OF_WORK_CONTRACT.md`) |
| **5. Collect** | Collect **$2,500 upfront** or **$5,000/mo retainer** | Immediate | Zero out-of-pocket overhead |
| **6. Fulfill** | Execute the deliverables using `04_30_DAY_FULFILLMENT_PLAYBOOK.md` | 4 Weeks | Client captured in LLM context windows |

---

## ⚙️ Configuration & Live API Connectors (Optional)

OmniGEO runs **100% locally out of the box with zero external API keys required** by utilizing intelligent multi-model heuristic simulations and live website scrapers.

If you wish to hook directly into live proprietary model APIs, set the following environment variables:

```bash
export OPENAI_API_KEY="sk-..."
export PERPLEXITY_API_KEY="pplx-..."
export GEMINI_API_KEY="AIza..."
export ANTHROPIC_API_KEY="sk-ant-..."
```
