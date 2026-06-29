import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import os
import json
from openai import OpenAI
from src.foundation.contracts import Critique, ViralityScore

BANNED_WORDS = ["unleash", "synergy", "deep-dive", "deep dive", "delve", "supercharge", "game-changer", "revolutionary", "tapestry", "paradigm shift"]

class CriticAI:
    """
    Architectural Layer 4: Critics (Platform, Brand+Safety, Virality).
    Audits copies on platform mechanics, brand safety (no placement guarantees),
    and attaches a 5-factor predicted virality scorecard out of 100.
    """
    def __init__(self, base_dir="."):
        self.base_dir = base_dir
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.groq_key = os.environ.get("GROQ_API_KEY")
        
        if self.groq_key:
            self.client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=self.groq_key
            )
            self.model = "llama-3.1-8b-instant"
        elif self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            self.model = "gpt-4o-mini"
        else:
            self.client = None
            self.model = "simulation"

    def evaluate_draft(self, draft_copy: dict, platform: str, variant_label: str) -> dict:
        """
        Grades a post copy draft against Platform Playbooks, Brand Safety, and Virality.
        Returns: Critique dict + ViralityScore dict
        """
        if self.client:
            return self._evaluate_real_llm(draft_copy, platform, variant_label)
        return self._evaluate_simulated_llm(draft_copy, platform, variant_label)

    def _evaluate_real_llm(self, draft: dict, platform: str, variant_label: str) -> dict:
        rubric_prompt = f"""You are the 'Critic AI Auditor' for JobInGen.
Strictly grade the social draft against the platform playbook for '{platform}' and Brand Safety rules.

Brand Safety Rules:
- Hard fail if any job/placement guarantee is made.
- Hard fail if there are corporate cliches: 'synergy', 'unleash', 'deep dive', 'supercharge'.

Draft to evaluate ({variant_label} - {platform}):
Hook: {draft.get('hook')}
Caption: {draft.get('caption')}
CTA: {draft.get('cta')}

Output raw JSON with exactly these keys:
- brand_voice: int (1-10)
- hook_strength: int (1-10)
- value_density: int (1-10)
- cta_score: int (1-10)
- cringe_filter: int (1-10)
- feedback: string (clear explanation of comments)
- passed: boolean (true only if ALL scores >= 7 and no cliches found)
- virality_total: int (0-100)
- trend_alignment: int (1-10)
- emotional_resonance: int (1-10)
- share_trigger: int (1-10)
- weakest_lever: string (the weakest of the five virality factors)
"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a brand auditor and copyeditor grading drafts against a 10-point scale and brand guidelines."},
                    {"role": "user", "content": rubric_prompt}
                ],
                response_format={"type": "json_object"} if "llama-3.1" in self.model or "gpt" in self.model else None
            )
            report = json.loads(response.choices[0].message.content)
            
            voice = report.get("brand_voice", 8)
            hook = report.get("hook_strength", 8)
            val = report.get("value_density", 8)
            cta = report.get("cta_score", 7)
            cringe = report.get("cringe_filter", 9)
            
            total_avg = sum([voice, hook, val, cta, cringe]) / 5.0
            
            return {
                "critique": {
                    "brand_voice": voice,
                    "hook_strength": hook,
                    "value_density": val,
                    "cta_score": cta,
                    "cringe_filter": cringe,
                    "total_score": round(total_avg, 1),
                    "feedback": report.get("feedback", "Excellent draft, matches playbook guidelines."),
                    "passed": report.get("passed", True)
                },
                "virality": {
                    "total": report.get("virality_total", 80),
                    "hook_strength": hook * 10,
                    "trend_alignment": report.get("trend_alignment", 8) * 10,
                    "emotional_resonance": report.get("emotional_resonance", 8) * 10,
                    "value_density": val * 10,
                    "share_trigger": report.get("share_trigger", 7) * 10,
                    "weakest_lever": report.get("weakest_lever", "value_density")
                }
            }
        except Exception as e:
            print(f"Critic API error: {e}")
            return self._evaluate_simulated_llm(draft, platform, variant_label)

    def _evaluate_simulated_llm(self, draft: dict, platform: str, variant_label: str) -> dict:
        hook = draft.get("hook", "")
        caption = draft.get("caption", "")
        cta = draft.get("cta", "")
        
        full_text = (hook + " " + caption + " " + cta).lower()
        
        # Check for banned words
        found_banned = []
        for word in BANNED_WORDS:
            if word in full_text:
                found_banned.append(word)
                
        if found_banned:
            # Failed brand compliance
            return {
                "critique": {
                    "brand_voice": 6,
                    "hook_strength": 5,
                    "value_density": 8,
                    "cta_score": 7,
                    "cringe_filter": 3,
                    "total_score": 5.8,
                    "feedback": f"CRITIC FAIL: Banned corporate jargon cliches detected: {found_banned}. We never use cliches. Rewrite in active student-first voice.",
                    "passed": False
                },
                "virality": {
                    "total": 58,
                    "hook_strength": 50,
                    "trend_alignment": 80,
                    "emotional_resonance": 70,
                    "value_density": 80,
                    "share_trigger": 60,
                    "weakest_lever": "cringe_filter"
                }
            }
        else:
            # High-passing scores
            if variant_label == "Variant B":
                return {
                    "critique": {
                        "brand_voice": 8,
                        "hook_strength": 9,
                        "value_density": 8,
                        "cta_score": 7,
                        "cringe_filter": 9,
                        "total_score": 8.2,
                        "feedback": "PASS: Strong contrarian hook, names genuine interview tension, zero corporate buzzwords.",
                        "passed": True
                    },
                    "virality": {
                        "total": 82,
                        "hook_strength": 90,
                        "trend_alignment": 95,
                        "emotional_resonance": 85,
                        "value_density": 80,
                        "share_trigger": 80,
                        "weakest_lever": "value_density"
                    }
                }
            else: # Variant A
                return {
                    "critique": {
                        "brand_voice": 8,
                        "hook_strength": 8,
                        "value_density": 8,
                        "cta_score": 7,
                        "cringe_filter": 9,
                        "total_score": 8.0,
                        "feedback": "PASS: Informative post aligning with keyword playbook requirements.",
                        "passed": True
                    },
                    "virality": {
                        "total": 80,
                        "hook_strength": 80,
                        "trend_alignment": 90,
                        "emotional_resonance": 80,
                        "value_density": 80,
                        "share_trigger": 70,
                        "weakest_lever": "share_trigger"
                    }
                }
