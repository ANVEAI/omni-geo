"""
Technical Web Crawler & AI Readiness Inspector
Audits websites for Generative Engine Optimization (GEO):
- AI Bot accessibility in robots.txt (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc.)
- llms.txt and llms-full.txt compliance
- JSON-LD structured data and Schema.org entity graphs
- Semantic HTML and answer-first layout
"""

import re
import json
import logging
from typing import Dict, Any, List, Optional
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

KNOWN_AI_BOTS = [
    {"name": "GPTBot", "owner": "OpenAI", "role": "Search & Model Training"},
    {"name": "ChatGPT-User", "role": "Real-time Web Browsing", "owner": "OpenAI"},
    {"name": "ClaudeBot", "role": "Anthropic Search & Scraping", "owner": "Anthropic"},
    {"name": "anthropic-ai", "role": "Anthropic Model Ingestion", "owner": "Anthropic"},
    {"name": "PerplexityBot", "role": "Real-time Live Citations", "owner": "Perplexity AI"},
    {"name": "Google-Extended", "role": "Gemini & Vertex AI Ingestion", "owner": "Google"},
    {"name": "CCBot", "role": "Common Crawl (Foundation Data)", "owner": "Common Crawl"},
    {"name": "cohere-ai", "role": "Enterprise AI Models", "owner": "Cohere"},
    {"name": "Bytespider", "role": "ByteDance / TikTok AI", "owner": "ByteDance"}
]

class TechnicalCrawler:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 (Compatible; OmniGEO-Engine/1.0)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

    def normalize_url(self, url: str) -> str:
        url = url.strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        return url

    def audit_robots_only(self, url: str) -> Dict[str, Any]:
        """Fast path for dedicated robots.txt validator tool."""
        url = self.normalize_url(url)
        parsed = urlparse(url)
        base_origin = f"{parsed.scheme}://{parsed.netloc}"
        return self._check_robots_txt(base_origin)

    def audit_url(self, url: str) -> Dict[str, Any]:
        """Performs a comprehensive technical GEO inspection on a target URL."""
        url = self.normalize_url(url)
        parsed = urlparse(url)
        base_origin = f"{parsed.scheme}://{parsed.netloc}"

        result: Dict[str, Any] = {
            "url": url,
            "origin": base_origin,
            "status": "success",
            "error": None,
            "robots_txt": {},
            "llms_txt": {},
            "schema_markup": {},
            "semantic_html": {},
            "response_metrics": {},
            "technical_score": 0,
            "recommendations": []
        }

        # 1. Fetch Homepage HTML
        try:
            resp = requests.get(url, headers=self.headers, timeout=self.timeout, allow_redirects=True)
            result["response_metrics"] = {
                "status_code": resp.status_code,
                "response_time_ms": int(resp.elapsed.total_seconds() * 1000),
                "content_length_bytes": len(resp.content),
                "final_url": resp.url,
                "is_https": resp.url.startswith("https://")
            }
            html_text = resp.text
            soup = BeautifulSoup(html_text, "html.parser")
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            result["status"] = "partial_error"
            result["error"] = str(e)
            html_text = ""
            soup = BeautifulSoup("", "html.parser")

        # 2. Check robots.txt
        result["robots_txt"] = self._check_robots_txt(base_origin)

        # 3. Check llms.txt and llms-full.txt
        result["llms_txt"] = self._check_llms_txt(base_origin)

        # 4. Extract and analyze Schema.org / JSON-LD
        result["schema_markup"] = self._analyze_schema_markup(soup)

        # 5. Analyze Semantic HTML & Answer-First structure
        result["semantic_html"] = self._analyze_semantic_html(soup, html_text)

        # 6. Compute Technical GEO Score & Recommendations
        self._calculate_technical_score(result)

        return result

    def _check_robots_txt(self, base_origin: str) -> Dict[str, Any]:
        robots_url = urljoin(base_origin, "/robots.txt")
        info = {
            "url": robots_url,
            "exists": False,
            "status_code": None,
            "bot_permissions": {},
            "wildcard_disallowed": False,
            "sitemaps": []
        }

        try:
            r = requests.get(robots_url, headers=self.headers, timeout=self.timeout)
            info["status_code"] = r.status_code
            if r.status_code == 200:
                info["exists"] = True
                content = r.text
                lines = content.splitlines()

                current_user_agents = []
                sitemaps = []
                rules = {}

                for line in lines:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if ":" in line:
                        key, val = [p.strip() for p in line.split(":", 1)]
                        key_lower = key.lower()
                        if key_lower == "user-agent":
                            current_user_agents.append(val)
                        elif key_lower == "sitemap":
                            sitemaps.append(val)
                        elif key_lower in ("disallow", "allow"):
                            for ua in current_user_agents:
                                if ua not in rules:
                                    rules[ua] = []
                                rules[ua].append({"type": key_lower, "path": val})
                    else:
                        current_user_agents = []

                info["sitemaps"] = sitemaps

                # Check wildcard rule
                wildcard_disallowed = False
                if "*" in rules:
                    for rule in rules["*"]:
                        if rule["type"] == "disallow" and rule["path"] in ("/", "/*"):
                            wildcard_disallowed = True
                info["wildcard_disallowed"] = wildcard_disallowed

                # Evaluate known AI bots
                bot_status = {}
                for bot in KNOWN_AI_BOTS:
                    bot_name = bot["name"]
                    status = "Allowed"
                    rule_matched = None

                    if bot_name in rules:
                        # Direct rule exists
                        disallows = [r["path"] for r in rules[bot_name] if r["type"] == "disallow"]
                        allows = [r["path"] for r in rules[bot_name] if r["type"] == "allow"]
                        if "/" in disallows or "/*" in disallows:
                            status = "Disallowed"
                            rule_matched = "Explicitly blocked in robots.txt"
                        elif disallows:
                            status = "Restricted"
                            rule_matched = f"Disallowed paths: {', '.join(disallows[:3])}"
                        else:
                            status = "Allowed"
                            rule_matched = "Explicitly permitted"
                    else:
                        # Follows wildcard
                        if wildcard_disallowed:
                            status = "Disallowed"
                            rule_matched = "Inherited Disallow from User-agent: *"
                        else:
                            status = "Allowed (Default)"
                            rule_matched = "No restrictions found"

                    bot_status[bot_name] = {
                        "owner": bot["owner"],
                        "role": bot["role"],
                        "status": status,
                        "details": rule_matched
                    }

                info["bot_permissions"] = bot_status

        except Exception as e:
            logger.debug(f"robots.txt check failed: {e}")
            info["error"] = str(e)

        return info

    def _check_llms_txt(self, base_origin: str) -> Dict[str, Any]:
        """Checks for llms.txt standard (https://llmstxt.org) adopted by AI crawlers."""
        llms_url = urljoin(base_origin, "/llms.txt")
        llms_full_url = urljoin(base_origin, "/llms-full.txt")

        result = {
            "has_llms_txt": False,
            "has_llms_full_txt": False,
            "llms_txt_url": llms_url,
            "llms_full_url": llms_full_url,
            "content_preview": None,
            "size_bytes": 0,
            "status": "Missing"
        }

        try:
            r = requests.get(llms_url, headers=self.headers, timeout=self.timeout)
            if r.status_code == 200 and len(r.text.strip()) > 20:
                result["has_llms_txt"] = True
                result["size_bytes"] = len(r.content)
                result["content_preview"] = r.text[:300]
                result["status"] = "Implemented"
        except Exception:
            pass

        try:
            r_full = requests.get(llms_full_url, headers=self.headers, timeout=self.timeout)
            if r_full.status_code == 200 and len(r_full.text.strip()) > 20:
                result["has_llms_full_txt"] = True
        except Exception:
            pass

        return result

    def _analyze_schema_markup(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extracts JSON-LD and checks for entity graphs, Organization, Product, FAQ, sameAs."""
        scripts = soup.find_all("script", type="application/ld+json")
        schemas = []
        schema_types = set()
        same_as_links = []
        has_organization = False
        has_product_or_software = False
        has_faq = False
        has_author_or_founder = False

        for s in scripts:
            try:
                if not s.string:
                    continue
                data = json.loads(s.string)
                schemas.append(data)
                
                # Traverse dict or graph
                items = []
                if isinstance(data, dict):
                    if "@graph" in data and isinstance(data["@graph"], list):
                        items.extend(data["@graph"])
                    else:
                        items.append(data)
                elif isinstance(data, list):
                    items.extend(data)

                for item in items:
                    if isinstance(item, dict):
                        stype = item.get("@type")
                        if isinstance(stype, list):
                            for t in stype:
                                schema_types.add(str(t))
                        elif stype:
                            schema_types.add(str(stype))

                        # Check sameAs entity links
                        same_as = item.get("sameAs")
                        if isinstance(same_as, list):
                            same_as_links.extend([str(x) for x in same_as])
                        elif isinstance(same_as, str):
                            same_as_links.append(same_as)

                        # Check critical GEO schemas
                        t_lower = str(stype).lower()
                        if any(k in t_lower for k in ["organization", "corporation"]):
                            has_organization = True
                        if any(k in t_lower for k in ["product", "softwareapplication", "webapp"]):
                            has_product_or_software = True
                        if "faqpage" in t_lower:
                            has_faq = True
                        if any(k in t_lower for k in ["person", "founder", "author"]):
                            has_author_or_founder = True
            except Exception:
                continue

        # Classify sameAs targets (Wikidata, Crunchbase, Wikipedia, LinkedIn)
        recognized_entities = {
            "wikidata": any("wikidata.org" in link for link in same_as_links),
            "wikipedia": any("wikipedia.org" in link for link in same_as_links),
            "crunchbase": any("crunchbase.com" in link for link in same_as_links),
            "linkedin": any("linkedin.com" in link for link in same_as_links),
            "twitter_x": any("twitter.com" in link or "x.com" in link for link in same_as_links),
            "github": any("github.com" in link for link in same_as_links)
        }

        return {
            "total_json_ld_blocks": len(schemas),
            "detected_types": list(schema_types),
            "has_organization": has_organization,
            "has_product_or_software": has_product_or_software,
            "has_faq": has_faq,
            "has_author_or_founder": has_author_or_founder,
            "same_as_links": same_as_links,
            "recognized_entities": recognized_entities,
            "knowledge_graph_linked": recognized_entities["wikidata"] or recognized_entities["wikipedia"] or recognized_entities["crunchbase"]
        }

    def _analyze_semantic_html(self, soup: BeautifulSoup, raw_html: str) -> Dict[str, Any]:
        """Analyzes readability, headings hierarchy, answer formatting, and tables."""
        title = soup.find("title").get_text(strip=True) if soup.find("title") else ""
        meta_desc = ""
        meta_desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        if meta_desc_tag:
            meta_desc = meta_desc_tag.get("content", "").strip()

        h1s = [h.get_text(strip=True) for h in soup.find_all("h1")]
        h2s = [h.get_text(strip=True) for h in soup.find_all("h2")]
        h3s = [h.get_text(strip=True) for h in soup.find_all("h3")]

        tables = soup.find_all("table")
        lists = soup.find_all(["ul", "ol"])

        # Detect direct answer patterns (inverted pyramid style favored by LLMs)
        body_text = soup.get_text(separator=" ", strip=True) if soup else ""
        words = body_text.split()
        word_count = len(words)

        answer_patterns = [
            r"\b[A-Z][a-zA-Z\s]+ is a [a-z\s]+ that\b",
            r"\bWhat is [a-zA-Z\s]+\?\b",
            r"\bHow does [a-zA-Z\s]+ work\b",
            r"\bKey benefits of\b",
            r"\bPricing for\b",
            r"\bCompared to\b"
        ]

        direct_answer_matches = 0
        for pat in answer_patterns:
            if re.search(pat, body_text, re.IGNORECASE):
                direct_answer_matches += 1

        has_comparison_table = len(tables) > 0 or ("vs" in body_text.lower() and len(lists) > 2)

        return {
            "title": title,
            "meta_description": meta_desc,
            "h1_count": len(h1s),
            "h1_list": h1s[:3],
            "h2_count": len(h2s),
            "h3_count": len(h3s),
            "total_word_count": word_count,
            "has_tables": len(tables) > 0,
            "has_lists": len(lists) > 0,
            "has_comparison_structure": has_comparison_table,
            "direct_answer_signals": direct_answer_matches,
            "has_semantic_main": bool(soup.find("main")),
            "has_article_tags": bool(soup.find("article")),
            "open_graph_complete": bool(soup.find("meta", property="og:title") and soup.find("meta", property="og:description"))
        }

    def _calculate_technical_score(self, result: Dict[str, Any]):
        """Scores technical readiness out of 100 and builds immediate recommendations."""
        score = 0
        recs = []

        # 1. Robots.txt & Bot Accessibility (Max 35 pts)
        rinfo = result.get("robots_txt", {})
        if rinfo.get("exists", False):
            score += 5
            bots = rinfo.get("bot_permissions", {})
            blocked_critical = []
            for bname in ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended"]:
                bdata = bots.get(bname, {})
                if bdata.get("status") in ["Allowed", "Allowed (Default)"]:
                    score += 7.5
                else:
                    blocked_critical.append(bname)

            if blocked_critical:
                recs.append({
                    "priority": "CRITICAL",
                    "category": "Crawlability",
                    "title": f"Unblock AI Bots in robots.txt: {', '.join(blocked_critical)}",
                    "impact": "High-ticket AI search engines cannot access or index your real-time content."
                })
        else:
            # No robots.txt means default allow
            score += 25
            recs.append({
                "priority": "MEDIUM",
                "category": "Crawlability",
                "title": "Create an explicit robots.txt with dedicated AI crawler directives",
                "impact": "Define explicit Allow directives for GPTBot, ClaudeBot, and PerplexityBot to ensure priority indexing."
            })

        # 2. llms.txt standard (Max 20 pts)
        llms_info = result.get("llms_txt", {})
        if llms_info.get("has_llms_txt"):
            score += 15
            if llms_info.get("has_llms_full_txt"):
                score += 5
        else:
            recs.append({
                "priority": "HIGH",
                "category": "LLM Standards",
                "title": "Deploy /llms.txt and /llms-full.txt file",
                "impact": "Provides a clean, markdown-formatted source of truth that LLM web search scrapers prioritize over noisy HTML."
            })

        # 3. Schema.org & JSON-LD Entity Graph (Max 25 pts)
        schema = result.get("schema_markup", {})
        if schema.get("has_organization"):
            score += 7
        else:
            recs.append({
                "priority": "HIGH",
                "category": "Entity Schema",
                "title": "Implement Organization JSON-LD Schema",
                "impact": "Required for LLMs to definitively establish your brand identity, founders, and headquarters."
            })

        if schema.get("has_product_or_software"):
            score += 6
        else:
            recs.append({
                "priority": "MEDIUM",
                "category": "Entity Schema",
                "title": "Add SoftwareApplication or Product JSON-LD Schema",
                "impact": "Enables LLMs to identify feature sets, pricing models, and categorization when answering comparative queries."
            })

        if schema.get("has_faq"):
            score += 6
        else:
            recs.append({
                "priority": "MEDIUM",
                "category": "Entity Schema",
                "title": "Add FAQPage Schema to core landing and pricing pages",
                "impact": "FAQ markup maps directly to prompt-and-response ingestion pipelines in SearchGPT and Perplexity."
            })

        if schema.get("knowledge_graph_linked"):
            score += 6
        else:
            recs.append({
                "priority": "HIGH",
                "category": "Knowledge Graph",
                "title": "Connect sameAs entity links in JSON-LD (Wikidata, Crunchbase, LinkedIn)",
                "impact": "LLMs rely on Wikidata and Crunchbase to resolve brand disambiguation and authority weighting."
            })

        # 4. Semantic Structure & Answer Readiness (Max 20 pts)
        semantic = result.get("semantic_html", {})
        if semantic.get("h1_count") == 1:
            score += 5
        if semantic.get("has_comparison_structure"):
            score += 5
        else:
            recs.append({
                "priority": "MEDIUM",
                "category": "Content Architecture",
                "title": "Add structured feature & competitor comparison matrices",
                "impact": "LLMs extract tables with 3x higher fidelity when generating buyer recommendations."
            })

        if semantic.get("direct_answer_signals", 0) >= 2:
            score += 5
        else:
            recs.append({
                "priority": "LOW",
                "category": "Content Architecture",
                "title": "Adopt 'Answer-First' inverted pyramid copywriting",
                "impact": "Place direct definitions (e.g. 'Brand X is an AI-powered Y that...') within the first 100 words of each page."
            })

        if semantic.get("open_graph_complete"):
            score += 5

        result["technical_score"] = min(100, round(score))
        result["recommendations"] = recs
