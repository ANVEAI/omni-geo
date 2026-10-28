"""
LLM Visibility & Share of Voice Evaluator
Simulates and analyzes visibility across the 4 major generative AI engines:
1. OpenAI ChatGPT / SearchGPT
2. Perplexity AI
3. Google Gemini & AI Overviews
4. Anthropic Claude
"""

import os
import re
import random
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

MODELS_TRACKED = [
    {"id": "chatgpt", "name": "OpenAI ChatGPT / SearchGPT", "icon": "openai", "weight": 0.35},
    {"id": "perplexity", "name": "Perplexity AI", "icon": "perplexity", "weight": 0.25},
    {"id": "gemini", "name": "Google Gemini & AI Overviews", "icon": "gemini", "weight": 0.25},
    {"id": "claude", "name": "Anthropic Claude", "icon": "claude", "weight": 0.15}
]

class LLMEvaluator:
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.perplexity_key = os.getenv("PERPLEXITY_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    def generate_buying_queries(self, brand: str, niche: str, competitors: List[str]) -> List[Dict[str, str]]:
        """Generates high-intent buying prompts commonly asked to LLMs."""
        comp_str = competitors[0] if competitors else "market leaders"
        second_comp = competitors[1] if len(competitors) > 1 else "alternatives"

        queries = [
            {
                "id": "q1",
                "category": "Category Leadership / Best In Class",
                "prompt": f"What are the best {niche} tools and software platforms for modern teams in 2026?",
                "intent": "High Commercial Intent"
            },
            {
                "id": "q2",
                "category": "Direct Competitor Comparison",
                "prompt": f"Compare {brand} vs {comp_str} vs {second_comp}. Which one is recommended for scaling companies?",
                "intent": "Evaluation / Decision Stage"
            },
            {
                "id": "q3",
                "category": "Competitor Alternative Search",
                "prompt": f"Top modern alternatives to {comp_str} that are faster, better designed, and more cost-effective?",
                "intent": "Churn / Switcher Intent"
            },
            {
                "id": "q4",
                "category": "Technical & Feature Breakdown",
                "prompt": f"Which {niche} solution has the best API, ease of integration, and customer reviews?",
                "intent": "Technical Decision Maker"
            },
            {
                "id": "q5",
                "category": "ROI & Pricing Inquiry",
                "prompt": f"What is the most cost-effective {niche} platform for startups and growing businesses?",
                "intent": "Budget / CFO Intent"
            }
        ]
        return queries

    def evaluate_visibility(
        self,
        brand: str,
        domain: str,
        niche: str,
        competitors: List[str],
        custom_queries: List[str] = None,
        technical_score: int = 50,
        citation_score: int = 50
    ) -> Dict[str, Any]:
        """
        Evaluates brand visibility across all 4 major LLMs.
        Returns Share of Voice (SOV), mention rates, rank distribution, and prompt evaluations.
        """
        brand_clean = brand.strip()
        comps_clean = [c.strip() for c in competitors if c.strip()]
        if not comps_clean:
            comps_clean = ["Industry Leader A", "Incumbent B"]

        queries = self.generate_buying_queries(brand_clean, niche, comps_clean)
        if custom_queries:
            for idx, q_text in enumerate(custom_queries):
                if q_text.strip():
                    queries.append({
                        "id": f"custom_{idx}",
                        "category": "Custom Target Prompt",
                        "prompt": q_text.strip(),
                        "intent": "User Defined"
                    })

        # Calculate base visibility probability based on tech score & citation score
        composite_readiness = (technical_score * 0.45) + (citation_score * 0.55)

        # Simulation / heuristic modeling for models
        model_results = {}
        prompt_evaluations = []

        total_brand_mentions = 0
        total_brand_citations = 0
        competitor_mentions = {c: 0 for c in comps_clean}
        total_evaluations = len(queries) * len(MODELS_TRACKED)

        for q in queries:
            q_eval = {
                "query": q["prompt"],
                "category": q["category"],
                "intent": q["intent"],
                "model_responses": {}
            }

            for model in MODELS_TRACKED:
                m_id = model["id"]
                # Determine presence based on model biases
                # Perplexity requires high citations (Reddit/G2)
                # ChatGPT requires high authority & general crawler access
                # Gemini prefers Schema & Knowledge Graph
                # Claude prefers long-form documentation & clarity

                factor = composite_readiness / 100.0
                if m_id == "perplexity":
                    factor *= (citation_score / 100.0) * 1.1
                elif m_id == "gemini":
                    factor *= (technical_score / 100.0) * 1.1
                elif m_id == "chatgpt":
                    factor *= ((technical_score + citation_score) / 200.0)
                elif m_id == "claude":
                    factor *= 0.85  # Claude is generally more conservative with brand listings

                # Determine if mentioned
                is_mentioned = random.random() < factor
                rank_pos = None
                sentiment = "Neutral"
                has_citation = False

                if is_mentioned:
                    total_brand_mentions += 1
                    rank_pos = random.choice([1, 2, 2, 3, 3, 4]) if factor > 0.6 else random.choice([3, 4, 5])
                    sentiment = "Positive" if rank_pos <= 2 else "Neutral"
                    has_citation = is_mentioned and (citation_score > 40)
                    if has_citation:
                        total_brand_citations += 1

                # Competitor presence simulation (usually incumbents have higher legacy citations)
                comp_mentions_in_q = []
                for comp in comps_clean:
                    comp_prob = min(0.92, 0.65 + (0.1 * comps_clean.index(comp)))
                    if random.random() < comp_prob:
                        competitor_mentions[comp] += 1
                        comp_mentions_in_q.append(comp)

                # Snippet synthesis
                if is_mentioned:
                    snippet = f"Recommended as a top {niche} solution alongside {', '.join(comp_mentions_in_q[:2])}. Highlighted for modern workflow and ease of use."
                else:
                    snippet = f"Brand was omitted from recommendations. {', '.join(comp_mentions_in_q[:2])} dominated the response citing G2 reviews and Reddit discussions."

                response_data = {
                    "is_mentioned": is_mentioned,
                    "rank": rank_pos,
                    "sentiment": sentiment,
                    "has_direct_citation": has_citation,
                    "snippet": snippet,
                    "competitors_mentioned": comp_mentions_in_q
                }

                q_eval["model_responses"][m_id] = response_data

                if m_id not in model_results:
                    model_results[m_id] = {
                        "name": model["name"],
                        "mentions": 0,
                        "citations": 0,
                        "ranks": []
                    }
                if is_mentioned:
                    model_results[m_id]["mentions"] += 1
                    if has_citation:
                        model_results[m_id]["citations"] += 1
                    if rank_pos:
                        model_results[m_id]["ranks"].append(rank_pos)

            prompt_evaluations.append(q_eval)

        # Aggregate Model Stats
        model_breakdown = []
        for model in MODELS_TRACKED:
            m_id = model["id"]
            m_data = model_results.get(m_id, {})
            mentions = m_data.get("mentions", 0)
            mention_rate = round((mentions / len(queries)) * 100) if queries else 0
            ranks = m_data.get("ranks", [])
            avg_rank = round(sum(ranks) / len(ranks), 1) if ranks else None

            model_breakdown.append({
                "id": m_id,
                "name": model["name"],
                "icon": model["icon"],
                "mentions": mentions,
                "total_prompts": len(queries),
                "mention_rate_pct": mention_rate,
                "avg_rank": avg_rank,
                "status": "Dominant" if mention_rate >= 75 else ("Visible" if mention_rate >= 40 else "Vulnerable" if mention_rate >= 15 else "Invisible")
            })

        # Calculate Share of Voice (SOV)
        all_mentions_pool = total_brand_mentions + sum(competitor_mentions.values())
        if all_mentions_pool > 0:
            brand_sov = round((total_brand_mentions / all_mentions_pool) * 100)
            competitor_sov = {c: round((competitor_mentions[c] / all_mentions_pool) * 100) for c in comps_clean}
        else:
            brand_sov = 15
            competitor_sov = {c: round(85 / len(comps_clean)) for c in comps_clean}

        # Overall Presence Score (0-100)
        overall_presence_score = round(
            (total_brand_mentions / max(1, total_evaluations)) * 60 +
            (total_brand_citations / max(1, total_evaluations)) * 40
        )
        overall_presence_score = min(100, max(5, overall_presence_score))

        return {
            "overall_presence_score": overall_presence_score,
            "brand_share_of_voice_pct": brand_sov,
            "competitor_share_of_voice": competitor_sov,
            "total_prompts_tested": len(queries),
            "brand_mentions_count": total_brand_mentions,
            "brand_citations_count": total_brand_citations,
            "model_breakdown": model_breakdown,
            "prompt_evaluations": prompt_evaluations
        }
