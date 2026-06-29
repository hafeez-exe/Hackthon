import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
import random
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from src.foundation.database import DatabaseStore
from src.foundation.contracts import SignalItem, Theme

class TrendScout:
    """
    Architectural Layer 1: Signal (Scout + Synthesizer + Scorer).
    Retrieves grounded signals from SQLite (prepopulated) AND scrapes live, real-time
    careers and tech placement news feeds via Google News RSS dynamically!
    Now also includes live Google Autocomplete Keyword Scraper (real-time Google Trends)
    and supports real News API / RSS queries!
    """
    def __init__(self, base_dir="."):
        self.base_dir = base_dir
        self.store = DatabaseStore(base_dir=base_dir)
        self.news_api_key = os.environ.get("NEWS_API_KEY")

    def pull_google_autocomplete(self, keyword="tech interviews") -> List[str]:
        """
        Mimics AnswerThePublic programmatically for FREE!
        Queries Google's public autocomplete API to find exactly what questions 
        people are actively searching for in real-time. Requires no API keys.
        """
        suggestions = []
        try:
            encoded_query = urllib.parse.quote(keyword)
            # Fetch Chrome autocomplete search suggestions
            url = f"https://suggestqueries.google.com/complete/search?client=chrome&q={encoded_query}"
            
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            with urllib.request.urlopen(req, timeout=4) as response:
                raw_data = response.read().decode('utf-8')
                
            # Autocomplete returns: [query, [suggestions], [descriptions], ...]
            parsed = json.loads(raw_data)
            if len(parsed) > 1:
                suggestions = parsed[1][:5] # Grab top 5 search questions
        except Exception as e:
            print(f"Skipped Google Autocomplete Scraper: {e}")
            
        return suggestions

    def pull_live_news_rss(self, query="tech hiring trends") -> List[SignalItem]:
        """
        Pulls real-time live signals from Google News RSS.
        If NEWS_API_KEY is available in .env, it upgrades to hit newsapi.org's official developer endpoint!
        """
        live_signals = []
        
        # Upgrade to NewsAPI if key is provided in .env
        if self.news_api_key:
            try:
                encoded_query = urllib.parse.quote(query)
                url = f"https://newsapi.org/v2/everything?q={encoded_query}&sortBy=publishedAt&pageSize=3&apiKey={self.news_api_key}"
                
                req = urllib.request.Request(url, headers={'User-Agent': 'JobInGen-BIP/3.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    
                if data.get("status") == "ok":
                    for article in data.get("articles", []):
                        live_signals.append(SignalItem(
                            source="news",
                            text=f"NewsAPI: {article.get('title')}",
                            score=0.90,
                            url=article.get("url")
                        ))
                    return live_signals
            except Exception as e:
                print(f"NewsAPI.org request failed, falling back to Google News RSS: {e}")

        # Standard Fallback: Google News RSS
        try:
            encoded_query = urllib.parse.quote(query)
            url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
            
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                xml_data = response.read()
                
            root = ET.fromstring(xml_data)
            for item in root.findall(".//item")[:3]:
                title = item.find("title").text
                link = item.find("link").text
                
                live_signals.append(SignalItem(
                    source="news",
                    text=f"Live News Signal: {title}",
                    score=0.85,
                    url=link
                ))
        except Exception as e:
            print(f"Skipped live RSS news harvesting: {e}")
            
        return live_signals

    def scout_and_synthesize(self) -> List[Theme]:
        """
        Pulls signals from SQLite database, harvests live real-time news, 
        and extracts real-world autocomplete queries.
        """
        raw_items = self.store.get_all_signals()
        signals = [SignalItem(**s) for s in raw_items]
        
        # 1. Harvest live Google News / NewsAPI
        live_news = self.pull_live_news_rss(query="tech placement hiring anxiety college placements")
        if live_news:
            signals.extend(live_news)
            
        # 2. Ingest live Google Autocomplete suggestions (Simulated AnswerThePublic)
        autocomplete_queries = self.pull_google_autocomplete(keyword="ats resume rejections")
        for query in autocomplete_queries:
            signals.append(SignalItem(
                source="trends",
                text=f"Google Autocomplete Search: '{query}'",
                score=0.88,
                url="https://trends.google.com"
            ))
            
        # Programmatic clustering
        themes = []
        
        # Theme 1: Interview Freezing
        evidence_1 = [s for s in signals if "freeze" in s.text.lower() or "interview" in s.text.lower() or "anxiety" in s.text.lower()]
        if evidence_1:
            themes.append(Theme(
                label="Bypassing 'Tell me about yourself' placement freezing",
                evidence=evidence_1,
                heat=0.92
            ))
            
        # Theme 2: ATS Resume Rejections
        evidence_2 = [s for s in signals if "ats" in s.text.lower() or "resume" in s.text.lower() or "autocomplete" in s.text.lower()]
        if evidence_2:
            themes.append(Theme(
                label="Programmatic ATS rejections due to multi-column resume grids",
                evidence=evidence_2,
                heat=0.88
            ))
            
        # Theme 3: Project portfolio driven hiring
        evidence_3 = [s for s in signals if "portfolio" in s.text.lower() or "hiring" in s.text.lower() or "trends" in s.text.lower() or "newsapi" in s.text.lower()]
        if evidence_3:
            themes.append(Theme(
                label="Credentialism shift to project-driven portfolios",
                evidence=evidence_3,
                heat=0.82
            ))
            
        return themes

    def score_themes(self, candidate_themes: List[Theme], w1=0.45, w2=0.30, w3=0.25) -> Dict[str, Any]:
        """
        Evaluates and ranks themes against the mathematical model in Section 7.1:
        score = w1 * relevance + w2 * velocity + w3 * brand_fit - penalty(risk)
        """
        scored_themes = []
        
        for theme in candidate_themes:
            if "freezing" in theme.label.lower():
                relevance = 0.95
                velocity = theme.heat
                brand_fit = 0.90
                penalty = 0.0
            elif "ats" in theme.label.lower():
                relevance = 0.90
                velocity = theme.heat
                brand_fit = 0.95
                penalty = 0.0
            else:
                relevance = 0.80
                velocity = theme.heat
                brand_fit = 0.85
                penalty = 0.0
                
            total_score = (w1 * relevance) + (w2 * velocity) + (w3 * brand_fit) - penalty
            
            scored_themes.append({
                "theme": theme,
                "score": round(total_score, 3),
                "metrics": {
                    "audience_relevance": relevance,
                    "trend_velocity": velocity,
                    "brand_fit": brand_fit,
                    "penalty": penalty
                }
            })
            
        # Sort by total score descending
        scored_themes.sort(key=lambda x: x["score"], reverse=True)
        
        winner = None
        if scored_themes and scored_themes[0]["score"] >= 0.62:
            winner = scored_themes[0]["theme"]
            
        return {
            "all_scores": scored_themes,
            "chosen_theme": winner
        }

if __name__ == "__main__":
    scout = TrendScout(base_dir="jobingen-engine")
    themes = scout.scout_and_synthesize()
    results = scout.score_themes(themes)
    print(f"Top scored theme: {results['chosen_theme'].label if results['chosen_theme'] else 'None'}")
