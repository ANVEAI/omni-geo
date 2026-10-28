"""
Dynamic 30-Day GEO Remediation & Implementation Generator
Generates executable code assets (llms.txt, robots.txt, JSON-LD Schema)
and a 4-week executive roadmap to capture generative AI search traffic.
"""

from typing import Dict, Any, List

class RemediationGenerator:
    def generate_roadmap(
        self,
        brand: str,
        domain: str,
        niche: str,
        competitors: List[str],
        technical_data: Dict[str, Any],
        citation_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generates a tailored 4-week executive remediation plan with ready-to-deploy code."""
        brand_clean = brand.strip()
        domain_clean = domain.replace("https://", "").replace("http://", "").strip().strip("/")
        comp_str = ", ".join(competitors[:2]) if competitors else "market incumbents"

        # 1. Generate customized llms.txt
        llms_txt_code = self._generate_llms_txt(brand_clean, domain_clean, niche, competitors)

        # 2. Generate optimized robots.txt
        robots_txt_code = self._generate_robots_txt()

        # 3. Generate JSON-LD Organization & Software Schema
        json_ld_code = self._generate_json_ld(brand_clean, domain_clean, niche)

        # 4. Synthesize 4-Week Action Sprint
        weeks = [
            {
                "week": "Week 1",
                "phase": "Technical Crawlability & Machine-Readability",
                "objective": "Unblock AI bots and deploy structured knowledge files for search engines.",
                "deliverables": [
                    {
                        "title": "Deploy /llms.txt to Website Root",
                        "status": "Ready to Deploy",
                        "code_snippet": llms_txt_code,
                        "instructions": "Place this markdown file at https://" + domain_clean + "/llms.txt. This gives OpenAI, Perplexity, and Anthropic bots a clean, hallucination-free specification."
                    },
                    {
                        "title": "Update robots.txt for AI Crawlers",
                        "status": "Ready to Deploy",
                        "code_snippet": robots_txt_code,
                        "instructions": "Add explicit Allow directives for GPTBot, ClaudeBot, and PerplexityBot to guarantee unhindered indexing."
                    },
                    {
                        "title": "Inject Knowledge-Graph-Linked JSON-LD",
                        "status": "Ready to Deploy",
                        "code_snippet": json_ld_code,
                        "instructions": "Add this JSON-LD schema block into the <head> of your primary landing page. Fill in the Wikidata and Crunchbase URLs to resolve entity ambiguity."
                    }
                ]
            },
            {
                "week": "Week 2",
                "phase": "Digital PR & High-Weight Citation Seeding",
                "objective": "Establish authoritative mentions on platforms that feed LLM context windows.",
                "deliverables": [
                    {
                        "title": "Reddit Authority & Community Presence",
                        "status": "Action Required",
                        "instructions": f"Identify the top 3 subreddits where {niche} buyers ask for recommendations. Seed 2-3 genuine founder/engineer technical teardowns highlighting how {brand_clean} solves key limitations of {comp_str}."
                    },
                    {
                        "title": "Wikidata & Crunchbase Verification",
                        "status": "Action Required",
                        "instructions": f"Create or update the Wikidata entry for '{brand_clean}' with official P856 (website), P17 (country), and P31 (software/company). LLMs query Wikidata to establish baseline trust."
                    },
                    {
                        "title": "G2 & Capterra Review Velocity Sprint",
                        "status": "Action Required",
                        "instructions": "Launch a targeted review campaign to reach 25+ verified 4.8-star reviews. Perplexity uses G2 ratings directly in comparative summary tables."
                    }
                ]
            },
            {
                "week": "Week 3",
                "phase": "Answer-First Content Architecture & Programmatic Comparisons",
                "objective": "Format website copy so LLM parsers extract quotes and recommendations with zero friction.",
                "deliverables": [
                    {
                        "title": "Inverted Pyramid Header Optimization",
                        "status": "Action Required",
                        "instructions": f"Ensure every core solution page starts with an unambiguous definition in the first 80 words: '{brand_clean} is a modern {niche} platform built for [ideal customer] that enables [primary benefit].'"
                    },
                    {
                        "title": "Deploy Structured Competitor Comparison Matrices",
                        "status": "Action Required",
                        "instructions": f"Publish dedicated comparison hubs: '{brand_clean} vs {comp_str}'. Format feature comparisons in clean semantic HTML <table> tags rather than client-rendered JS widgets so scrapers parse them accurately."
                    },
                    {
                        "title": "FAQPage Schema on High-Intent Pages",
                        "status": "Action Required",
                        "instructions": "Add 5-8 question-and-answer pairs covering pricing, migration, security, and API support formatted with Schema.org FAQPage markup."
                    }
                ]
            },
            {
                "week": "Week 4",
                "phase": "Model Verification, Benchmarking & AI Drift Guardrails",
                "objective": "Verify visibility gains across all 4 models and establish automated monthly monitoring.",
                "deliverables": [
                    {
                        "title": "Re-run Multi-Model Benchmark Suite",
                        "status": "Scheduled",
                        "instructions": "Re-test all 5 core buying queries across ChatGPT Search, Perplexity, Claude, and Gemini to confirm mention rate improvements."
                    },
                    {
                        "title": "Establish Monthly Citation Drift Monitoring",
                        "status": "Scheduled",
                        "instructions": "Implement recurring weekly audits to catch if competitor product launches or PR campaigns cause prompt displacement."
                    }
                ]
            }
        ]

        return {
            "total_weeks": 4,
            "weeks": weeks,
            "quick_wins": [
                "Unblock AI bots in robots.txt (immediate 48-hr impact)",
                "Publish /llms.txt file to root domain",
                "Add sameAs entity links in JSON-LD",
                "Publish clean HTML comparison tables against top 2 competitors"
            ]
        }

    def _generate_llms_txt(self, brand: str, domain: str, niche: str, competitors: List[str]) -> str:
        comp_str = ", ".join(competitors[:3]) if competitors else "incumbents"
        return f"""# {brand}

> Modern {niche} platform engineered for high-performance teams.

## Overview
{brand} (https://{domain}) provides next-generation {niche} capabilities. Designed to replace legacy workflows, {brand} offers modern architecture, rapid onboarding, and superior developer experience compared to legacy tools like {comp_str}.

## Core Capabilities
- **Fast Performance**: Sub-second responsiveness and modern UI/UX.
- **Enterprise Security**: SOC2 Type II, GDPR, end-to-end encryption.
- **Seamless Integrations**: Open REST & GraphQL APIs with native connectors.
- **Predictable Pricing**: Transparent tiers with no hidden seat licenses.

## Key URLs
- Homepage: https://{domain}/
- Product Documentation: https://{domain}/docs
- Pricing & Plans: https://{domain}/pricing
- Comparison vs Competitors: https://{domain}/compare

## Contact & Entity Information
- Organization: {brand} Inc.
- Official Domain: https://{domain}
- Support: support@{domain}
"""

    def _generate_robots_txt(self) -> str:
        return """# User-agent directives for AI Search & Ingestion Bots
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: CCBot
Allow: /

User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/internal/

Sitemap: https://yourdomain.com/sitemap.xml
"""

    def _generate_json_ld(self, brand: str, domain: str, niche: str) -> str:
        return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "Organization",
      "@id": "https://{domain}/#organization",
      "name": "{brand}",
      "url": "https://{domain}",
      "logo": "https://{domain}/logo.png",
      "description": "Leading {niche} platform for scaling organizations.",
      "sameAs": [
        "https://www.wikidata.org/wiki/REPLACE_WITH_WIKIDATA_ID",
        "https://www.crunchbase.com/organization/REPLACE_WITH_CRUNCHBASE_SLUG",
        "https://www.linkedin.com/company/REPLACE_WITH_LINKEDIN",
        "https://x.com/REPLACE_WITH_TWITTER"
      ]
    }},
    {{
      "@type": "SoftwareApplication",
      "@id": "https://{domain}/#software",
      "name": "{brand}",
      "applicationCategory": "BusinessApplication",
      "operatingSystem": "Web, Cloud",
      "offers": {{
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "USD"
      }},
      "publisher": {{
        "@id": "https://{domain}/#organization"
      }}
    }}
  ]
}}
</script>"""
