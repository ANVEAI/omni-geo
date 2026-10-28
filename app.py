"""
OmniGEO Application Server
FastAPI backend powering the Generative Engine Optimization & AI Search Audit Platform.
"""

import os
import json
import uuid
import logging
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from core.crawler import TechnicalCrawler
from core.citation_checker import CitationChecker
from core.llm_evaluator import LLMEvaluator
from core.scoring import calculate_geo_score
from core.remediation import RemediationGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OmniGEO")

app = FastAPI(
    title="OmniGEO - Generative Engine Optimization Platform",
    description="Full-stack AI Search Audit & Executive Reporting Engine",
    version="1.0.0"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
AUDITS_DIR = os.path.join(DATA_DIR, "audits")
os.makedirs(AUDITS_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Initialize Engines
crawler = TechnicalCrawler()
citation_checker = CitationChecker()
llm_evaluator = LLMEvaluator()
remediation_gen = RemediationGenerator()

class AuditRequest(BaseModel):
    brand_name: str
    domain: str
    niche: str
    competitors: List[str]
    custom_queries: Optional[List[str]] = None

def load_audit(audit_id: str) -> Optional[dict]:
    # Check data/audits/ first
    audit_path = os.path.join(AUDITS_DIR, f"{audit_id}.json")
    if os.path.exists(audit_path):
        with open(audit_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # Check sample_audits.json
    samples_path = os.path.join(DATA_DIR, "sample_audits.json")
    if os.path.exists(samples_path):
        with open(samples_path, "r", encoding="utf-8") as f:
            samples = json.load(f)
            if audit_id in samples:
                return samples[audit_id]

    return None

def save_audit(audit_data: dict):
    audit_id = audit_data["id"]
    audit_path = os.path.join(AUDITS_DIR, f"{audit_id}.json")
    with open(audit_path, "w", encoding="utf-8") as f:
        json.dump(audit_data, f, indent=2)

def list_all_audits() -> List[dict]:
    audits = []
    # Load samples
    samples_path = os.path.join(DATA_DIR, "sample_audits.json")
    if os.path.exists(samples_path):
        try:
            with open(samples_path, "r", encoding="utf-8") as f:
                samples = json.load(f)
                for k, v in samples.items():
                    audits.append({
                        "id": v.get("id", k),
                        "brand_name": v.get("brand_name"),
                        "domain": v.get("domain"),
                        "niche": v.get("niche"),
                        "score": v.get("scoring", {}).get("final_score", 0),
                        "grade": v.get("scoring", {}).get("grade", "N/A"),
                        "created_at": v.get("created_at"),
                        "is_sample": True
                    })
        except Exception as e:
            logger.error(f"Error loading sample audits: {e}")

    # Load real audits
    if os.path.exists(AUDITS_DIR):
        for fname in os.listdir(AUDITS_DIR):
            if fname.endswith(".json"):
                try:
                    with open(os.path.join(AUDITS_DIR, fname), "r", encoding="utf-8") as f:
                        data = json.load(f)
                        audits.append({
                            "id": data.get("id"),
                            "brand_name": data.get("brand_name"),
                            "domain": data.get("domain"),
                            "niche": data.get("niche"),
                            "score": data.get("scoring", {}).get("final_score", 0),
                            "grade": data.get("scoring", {}).get("grade", "N/A"),
                            "created_at": data.get("created_at"),
                            "is_sample": False
                        })
                except Exception as e:
                    logger.error(f"Error loading audit {fname}: {e}")

    # Sort newest first
    audits.sort(key=lambda x: str(x.get("created_at")), reverse=True)
    return audits

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    recent_audits = list_all_audits()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "recent_audits": recent_audits,
            "total_audits_count": len(recent_audits)
        }
    )

@app.post("/api/audit")
async def run_audit_api(req: AuditRequest):
    try:
        audit_id = f"audit_{uuid.uuid4().hex[:10]}"
        created_at = datetime.utcnow().isoformat() + "Z"

        brand = req.brand_name.strip()
        domain = req.domain.strip()
        niche = req.niche.strip()
        competitors = [c.strip() for c in req.competitors if c.strip()]

        # 1. Technical crawl
        technical_data = crawler.audit_url(domain)
        tech_score = technical_data.get("technical_score", 50)

        # 2. Citation analysis
        citation_data = citation_checker.analyze_citation_footprint(brand, domain, niche)
        citation_score = citation_data.get("citation_score", 50)

        # 3. LLM simulation & visibility evaluation
        llm_eval = llm_evaluator.evaluate_visibility(
            brand=brand,
            domain=domain,
            niche=niche,
            competitors=competitors,
            custom_queries=req.custom_queries,
            technical_score=tech_score,
            citation_score=citation_score
        )
        presence_score = llm_eval.get("overall_presence_score", 50)
        brand_sov = llm_eval.get("brand_share_of_voice_pct", 20)

        # 4. Semantic score calculation from technical data
        semantic_data = technical_data.get("semantic_html", {})
        schema_data = technical_data.get("schema_markup", {})
        semantic_score = 40
        if schema_data.get("has_organization"):
            semantic_score += 15
        if schema_data.get("has_product_or_software"):
            semantic_score += 15
        if schema_data.get("has_faq"):
            semantic_score += 10
        if semantic_data.get("has_comparison_structure"):
            semantic_score += 10
        if schema_data.get("knowledge_graph_linked"):
            semantic_score += 10
        semantic_score = min(100, semantic_score)

        # 5. Composite Scoring & Financial Impact
        scoring = calculate_geo_score(
            presence_score=presence_score,
            citation_score=citation_score,
            technical_score=tech_score,
            semantic_score=semantic_score,
            brand_sov=brand_sov,
            niche=niche
        )

        # 6. Remediation & Action Plan
        remediation = remediation_gen.generate_roadmap(
            brand=brand,
            domain=domain,
            niche=niche,
            competitors=competitors,
            technical_data=technical_data,
            citation_data=citation_data
        )

        # Compile final audit object
        audit_record = {
            "id": audit_id,
            "created_at": created_at,
            "brand_name": brand,
            "domain": domain,
            "niche": niche,
            "competitors": competitors,
            "scoring": scoring,
            "technical": technical_data,
            "citation": citation_data,
            "llm_eval": llm_eval,
            "remediation": remediation
        }

        save_audit(audit_record)

        return {
            "status": "success",
            "audit_id": audit_id,
            "redirect_url": f"/report/{audit_id}"
        }

    except Exception as e:
        logger.exception("Error executing audit")
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.get("/report/{audit_id}", response_class=HTMLResponse)
async def view_report(request: Request, audit_id: str):
    audit = load_audit(audit_id)
    if not audit:
        return HTMLResponse(content="<h1>Audit Report Not Found</h1><p><a href='/'>Return to Dashboard</a></p>", status_code=404)

    return templates.TemplateResponse(
        request=request,
        name="report.html",
        context={
            "audit": audit,
            "scoring": audit.get("scoring", {}),
            "technical": audit.get("technical", {}),
            "citation": audit.get("citation", {}),
            "llm_eval": audit.get("llm_eval", {}),
            "remediation": audit.get("remediation", {})
        }
    )

@app.get("/api/report/{audit_id}")
async def get_report_json(audit_id: str):
    audit = load_audit(audit_id)
    if not audit:
        return JSONResponse(status_code=404, content={"error": "Report not found"})
    return audit

@app.get("/api/reports")
async def get_all_reports():
    return list_all_audits()

class CheckRobotsRequest(BaseModel):
    url: str

@app.get("/dashboard", response_class=HTMLResponse)
async def workspace_dashboard(request: Request):
    recent_audits = list_all_audits()
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "recent_audits": recent_audits,
            "total_audits_count": len(recent_audits)
        }
    )

@app.get("/tools/llms-txt-generator", response_class=HTMLResponse)
async def tools_llms_txt(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="tools_llms_txt.html",
        context={}
    )

@app.get("/tools/robots-txt-tester", response_class=HTMLResponse)
async def tools_robots_txt(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="tools_robots_txt.html",
        context={}
    )

@app.post("/api/tools/check-robots")
async def api_check_robots(req: CheckRobotsRequest):
    try:
        data = crawler.audit_robots_only(req.url)
        return data
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/pricing", response_class=HTMLResponse)
async def view_pricing(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pricing.html",
        context={}
    )

@app.get("/gtm-kit", response_class=HTMLResponse)
async def view_gtm_kit(request: Request):
    # Load all markdown files from gtm_kit/
    gtm_dir = os.path.join(BASE_DIR, "gtm_kit")
    files_data = []
    if os.path.exists(gtm_dir):
        for fname in sorted(os.listdir(gtm_dir)):
            if fname.endswith(".md"):
                fpath = os.path.join(gtm_dir, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                files_data.append({
                    "filename": fname,
                    "title": fname.replace(".md", "").replace("_", " ").title(),
                    "content": content
                })

    return templates.TemplateResponse(
        request=request,
        name="gtm_kit.html",
        context={
            "files": files_data
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
