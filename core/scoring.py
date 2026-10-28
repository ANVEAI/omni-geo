"""
GEO Scoring Algorithm & Revenue Impact Calculator
Synthesizes the 4 Core GEO Pillars into an executive score:
1. Generative Presence & Share of Voice (35%)
2. Citation Authority & Platform Graph (25%)
3. Technical AI Crawlability & Bot Whitelisting (20%)
4. Semantic Architecture & Knowledge Graph (20%)
"""

from typing import Dict, Any, List

def calculate_geo_score(
    presence_score: int,
    citation_score: int,
    technical_score: int,
    semantic_score: int,
    brand_sov: int,
    niche: str
) -> Dict[str, Any]:
    """Computes overall GEO score, grade, and business financial impact."""
    # 4-Pillar Weighted Score
    w_presence = 0.35
    w_citation = 0.25
    w_technical = 0.20
    w_semantic = 0.20

    composite = (
        (presence_score * w_presence) +
        (citation_score * w_citation) +
        (technical_score * w_technical) +
        (semantic_score * w_semantic)
    )
    final_score = round(max(5, min(99, composite)))

    # Determine Letter Grade
    if final_score >= 90:
        grade = "A+"
        grade_desc = "Generative Market Leader - Highly resilient to LLM search shifts"
        color = "#10B981"
    elif final_score >= 80:
        grade = "A"
        grade_desc = "Strong Visibility - Regularly cited across leading models"
        color = "#34D399"
    elif final_score >= 70:
        grade = "B"
        grade_desc = "Moderate Visibility - Vulnerable to aggressive competitor displacement"
        color = "#3B82F6"
    elif final_score >= 55:
        grade = "C"
        grade_desc = "Sub-Optimal - Frequently omitted in high-intent commercial prompts"
        color = "#F59E0B"
    elif final_score >= 40:
        grade = "D"
        grade_desc = "High Vulnerability - Minimal presence outside direct branded queries"
        color = "#EF4444"
    else:
        grade = "F"
        grade_desc = "Critical AI Blindspot - Near-total invisibility in LLM discovery"
        color = "#DC2626"

    # Financial / Pipeline Impact Estimation
    # Assume 3,500 monthly AI buying queries in mid-market niche, $2,400 ACV
    estimated_monthly_ai_queries = 4200
    competitor_leakage_pct = max(10, 100 - brand_sov)
    estimated_lost_prospects_per_mo = round(estimated_monthly_ai_queries * (competitor_leakage_pct / 100) * 0.035)
    estimated_annual_pipeline_leak = estimated_lost_prospects_per_mo * 2500 * 12

    return {
        "final_score": final_score,
        "grade": grade,
        "grade_description": grade_desc,
        "color_code": color,
        "pillars": [
            {
                "name": "Generative Share of Voice",
                "score": presence_score,
                "weight": "35%",
                "status": "Healthy" if presence_score >= 70 else ("Warning" if presence_score >= 45 else "Critical"),
                "summary": "Frequency and rank position when prospective buyers ask commercial decision prompts."
            },
            {
                "name": "Citation Graph Authority",
                "score": citation_score,
                "weight": "25%",
                "status": "Healthy" if citation_score >= 70 else ("Warning" if citation_score >= 45 else "Critical"),
                "summary": "Entity footprint across Reddit, Wikipedia, G2, and primary LLM ingestion networks."
            },
            {
                "name": "Technical Crawlability & llms.txt",
                "score": technical_score,
                "weight": "20%",
                "status": "Healthy" if technical_score >= 70 else ("Warning" if technical_score >= 45 else "Critical"),
                "summary": "AI bot access rules in robots.txt and adoption of clean markdown documentation standards."
            },
            {
                "name": "Semantic Architecture & Schema",
                "score": semantic_score,
                "weight": "20%",
                "status": "Healthy" if semantic_score >= 70 else ("Warning" if semantic_score >= 45 else "Critical"),
                "summary": "JSON-LD Knowledge Graph integration, sameAs identity resolution, and comparison tables."
            }
        ],
        "financial_impact": {
            "monthly_ai_queries_in_niche": estimated_monthly_ai_queries,
            "competitor_leakage_rate_pct": competitor_leakage_pct,
            "estimated_lost_qualified_prospects_monthly": estimated_lost_prospects_per_mo,
            "estimated_annual_pipeline_at_risk": f"${estimated_annual_pipeline_leak:,.0f}"
        }
    }
