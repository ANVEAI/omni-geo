"""
Sample Audits Generator & Benchmark Data
Provides pre-computed high-ticket GEO audits for demonstration and pitch portfolios.
"""

import json
import os
from typing import Dict, Any, List

def get_linear_audit() -> Dict[str, Any]:
    return {
        "id": "audit_linear_sample",
        "created_at": "2026-10-28T01:00:00Z",
        "brand_name": "Linear",
        "domain": "linear.app",
        "niche": "Modern Project Management & Issue Tracking",
        "competitors": ["Jira", "Asana", "Monday.com"],
        "scoring": {
            "final_score": 78,
            "grade": "B",
            "grade_description": "Strong Brand Affinity, but Vulnerable to Enterprise Incumbents in Multi-Model Prompts",
            "color_code": "#3B82F6",
            "pillars": [
                {
                    "name": "Generative Share of Voice",
                    "score": 74,
                    "weight": "35%",
                    "status": "Healthy",
                    "summary": "Consistently cited for startups and tech teams; omitted when users prompt for 'enterprise compliance & scale'."
                },
                {
                    "name": "Citation Graph Authority",
                    "score": 82,
                    "weight": "25%",
                    "status": "Healthy",
                    "summary": "Extremely high Reddit sentiment (r/reactjs, r/SaaS), but lagging Jira's 10,000+ legacy G2 reviews."
                },
                {
                    "name": "Technical Crawlability & llms.txt",
                    "score": 80,
                    "weight": "20%",
                    "status": "Healthy",
                    "summary": "Robots.txt allows AI bots; has rich markdown documentation, missing dedicated /llms.txt standard."
                },
                {
                    "name": "Semantic Architecture & Schema",
                    "score": 76,
                    "weight": "20%",
                    "status": "Healthy",
                    "summary": "Has Product and Organization schema, needs sameAs entity linkage to Wikidata entity Q105749211."
                }
            ],
            "financial_impact": {
                "monthly_ai_queries_in_niche": 6500,
                "competitor_leakage_rate_pct": 52,
                "estimated_lost_qualified_prospects_monthly": 118,
                "estimated_annual_pipeline_at_risk": "$1,416,000"
            }
        },
        "technical": {
            "url": "https://linear.app",
            "origin": "https://linear.app",
            "status": "success",
            "technical_score": 80,
            "response_metrics": {
                "status_code": 200,
                "response_time_ms": 142,
                "is_https": True
            },
            "robots_txt": {
                "exists": True,
                "bot_permissions": {
                    "GPTBot": {"status": "Allowed", "owner": "OpenAI", "role": "Search & Training"},
                    "ClaudeBot": {"status": "Allowed", "owner": "Anthropic", "role": "Search & Scraping"},
                    "PerplexityBot": {"status": "Allowed", "owner": "Perplexity AI", "role": "Live Citations"},
                    "Google-Extended": {"status": "Allowed", "owner": "Google", "role": "Gemini Ingestion"}
                }
            },
            "llms_txt": {
                "has_llms_txt": False,
                "status": "Missing",
                "llms_txt_url": "https://linear.app/llms.txt"
            },
            "schema_markup": {
                "has_organization": True,
                "has_product_or_software": True,
                "has_faq": False,
                "knowledge_graph_linked": False,
                "detected_types": ["Organization", "SoftwareApplication", "WebSite"]
            },
            "semantic_html": {
                "title": "Linear – A better way to build products",
                "meta_description": "Linear is a purpose-built tool for planning and building products. Streamline issues, projects, and product roadmaps.",
                "h1_count": 1,
                "has_comparison_structure": True,
                "direct_answer_signals": 3
            },
            "recommendations": [
                {
                    "priority": "HIGH",
                    "category": "Standards",
                    "title": "Deploy /llms.txt at root domain",
                    "impact": "Provides deterministic product capability feeds for SearchGPT."
                },
                {
                    "priority": "HIGH",
                    "category": "Knowledge Graph",
                    "title": "Link sameAs in JSON-LD to Wikidata Q105749211 and Crunchbase",
                    "impact": "Eliminates entity ambiguity between Linear software and linear mathematics concepts in Google Gemini."
                }
            ]
        },
        "citation": {
            "citation_score": 82,
            "wikidata": {
                "exists": True,
                "id": "Q105749211",
                "label": "Linear",
                "description": "Issue tracking tool"
            },
            "wikipedia": {
                "exists": False,
                "title": None,
                "snippet": "No dedicated Wikipedia article exists yet. Subject is covered in software roundups."
            },
            "reddit": {
                "estimated_threads": 45,
                "sentiment_overview": "Extremely Positive",
                "key_subreddits": ["r/programming", "r/startups", "r/SaaS", "r/webdev"]
            },
            "review_platforms": {
                "platforms_tracked": ["G2", "Capterra", "Product Hunt"],
                "estimated_profiles": 3,
                "status": "High ratings, review volume 10x lower than Jira"
            },
            "gaps": [
                {
                    "source": "G2 Review Volume Deficit",
                    "status": "Vulnerable",
                    "severity": "HIGH",
                    "impact": "Jira has 5,800+ reviews vs Linear's ~400, leading Perplexity to rank Jira #1 for enterprise prompts.",
                    "action": "Incentivize existing power users to publish verified enterprise reviews."
                }
            ]
        },
        "llm_eval": {
            "overall_presence_score": 74,
            "brand_share_of_voice_pct": 34,
            "competitor_share_of_voice": {
                "Jira": 48,
                "Asana": 12,
                "Monday.com": 6
            },
            "total_prompts_tested": 5,
            "brand_mentions_count": 14,
            "brand_citations_count": 11,
            "model_breakdown": [
                {
                    "id": "claude",
                    "name": "Anthropic Claude",
                    "icon": "claude",
                    "mentions": 5,
                    "total_prompts": 5,
                    "mention_rate_pct": 100,
                    "avg_rank": 1.2,
                    "status": "Dominant"
                },
                {
                    "id": "chatgpt",
                    "name": "OpenAI SearchGPT",
                    "icon": "openai",
                    "mentions": 4,
                    "total_prompts": 5,
                    "mention_rate_pct": 80,
                    "avg_rank": 2.1,
                    "status": "Dominant"
                },
                {
                    "id": "perplexity",
                    "name": "Perplexity AI",
                    "icon": "perplexity",
                    "mentions": 3,
                    "total_prompts": 5,
                    "mention_rate_pct": 60,
                    "avg_rank": 2.8,
                    "status": "Visible"
                },
                {
                    "id": "gemini",
                    "name": "Google Gemini & AI Overviews",
                    "icon": "gemini",
                    "mentions": 2,
                    "total_prompts": 5,
                    "mention_rate_pct": 40,
                    "avg_rank": 3.4,
                    "status": "Vulnerable"
                }
            ],
            "prompt_evaluations": [
                {
                    "query": "What are the best modern project management and issue tracking tools for engineering teams in 2026?",
                    "category": "Category Leadership",
                    "intent": "High Commercial Intent",
                    "model_responses": {
                        "chatgpt": {
                            "is_mentioned": True,
                            "rank": 1,
                            "sentiment": "Positive",
                            "has_direct_citation": True,
                            "snippet": "Linear is highly recommended as the fastest, developer-centric issue tracking platform with keyboard-first navigation.",
                            "competitors_mentioned": ["Jira", "Asana"]
                        },
                        "perplexity": {
                            "is_mentioned": True,
                            "rank": 2,
                            "sentiment": "Positive",
                            "has_direct_citation": True,
                            "snippet": "Jira leads in enterprise features, while Linear is cited by developers on Reddit as the top modern alternative.",
                            "competitors_mentioned": ["Jira"]
                        },
                        "gemini": {
                            "is_mentioned": False,
                            "rank": None,
                            "sentiment": "Neutral",
                            "has_direct_citation": False,
                            "snippet": "Google AI Overview recommended Jira and Asana, drawing primarily from legacy Capterra comparisons.",
                            "competitors_mentioned": ["Jira", "Asana", "Monday.com"]
                        },
                        "claude": {
                            "is_mentioned": True,
                            "rank": 1,
                            "sentiment": "Positive",
                            "has_direct_citation": True,
                            "snippet": "Linear represents the state-of-the-art for agile engineering teams with seamless GitHub and Slack integrations.",
                            "competitors_mentioned": ["Jira"]
                        }
                    }
                }
            ]
        },
        "remediation": {
            "total_weeks": 4,
            "quick_wins": [
                "Deploy /llms.txt with core API & feature manifests",
                "Link Wikidata entity Q105749211 to eliminate Gemini brand ambiguity",
                "Publish semantic comparison hub: 'Linear vs Jira for Scaling Startups'",
                "Deploy FAQPage schema covering enterprise SOC2 and migration tools"
            ],
            "weeks": [
                {
                    "week": "Week 1",
                    "phase": "Technical Crawlability & Machine-Readability",
                    "objective": "Unblock AI bots and deploy structured knowledge files for search engines.",
                    "deliverables": [
                        {
                            "title": "Deploy /llms.txt Specification",
                            "status": "Ready to Deploy",
                            "code_snippet": "# Linear\\n\\n> Purpose-built tool for modern software development and issue tracking.\\n\\n## Overview\\nLinear (https://linear.app) streamlines issues, sprints, and product roadmaps with sub-second speed.",
                            "instructions": "Upload to https://linear.app/llms.txt to provide SearchGPT and Claude with structured capability endpoints."
                        }
                    ]
                }
            ]
        }
    }

def init_sample_audits():
    """Initializes sample audits into the data directory."""
    os.makedirs("/Users/adarshkant/.gemini/antigravity/scratch/geo-audit-platform/data/audits", exist_ok=True)
    sample_file = "/Users/adarshkant/.gemini/antigravity/scratch/geo-audit-platform/data/sample_audits.json"
    linear_data = get_linear_audit()
    samples = {
        "audit_linear_sample": linear_data
    }
    with open(sample_file, "w", encoding="utf-8") as f:
        json.dump(samples, f, indent=2)

if __name__ == "__main__":
    init_sample_audits()
    print("Sample audits initialized successfully.")
