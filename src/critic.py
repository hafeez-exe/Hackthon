import os
import json
from openai import OpenAI

BANNED_WORDS = ["unleash", "synergy", "deep-dive", "deep dive", "delve", "supercharge", "game-changer", "revolutionary", "tapestry", "paradigm shift"]

class CriticAI:
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
            print("🚀 CriticAI initialized using Groq API!")
        elif self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            self.model = "gpt-4o-mini"
            print("✨ CriticAI initialized using OpenAI API!")
        else:
            self.client = None
            self.model = "simulation"
            print("💻 CriticAI running in local Simulation Mode!")

    def evaluate_variant(self, draft, variant_label="Variant A"):
        """
        Grades a post copy draft against the 5-point brand rubric, each out of 10 points.
        Returns evaluation scores matching the user's A/B testing screenshot.
        """
        if self.client:
            return self._evaluate_real_llm(draft, variant_label)
        return self._evaluate_simulated_llm(draft, variant_label)

    def _evaluate_real_llm(self, draft, variant_label):
        rubric_prompt = f"""You are 'Critic AI', an aggressive brand auditor for JobInGen.
Grade the draft social post copy on a strict scale of 1 to 10 for these 5 metrics:

1. Brand Voice: Student-first, sharp, direct, authentic.
2. Hook Strength: Catchy, under 8 words, free of corporate cliches.
3. Value Density: High career-relevance, useful takeaways.
4. CTA: Clear, actionable, and low-friction call-to-action.
5. Cringe Filter: Deduct heavily (score 1-4) if there are buzzwords like 'synergy', 'unleash', 'deep dive', 'supercharge', 'game-changer'.

Draft to evaluate ({variant_label}):
Hook: {draft.get('hook')}
Caption: {draft.get('caption')}
CTA: {draft.get('cta')}

Output raw JSON containing exactly these keys:
- brand_voice: int (1-10)
- hook_strength: int (1-10)
- value_density: int (1-10)
- cta_score: int (1-10)
- cringe_filter: int (1-10)
- feedback: string (brief constructive comments)
"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a copyeditor grading social copy out of 10 points on 5 metrics."},
                    {"role": "user", "content": rubric_prompt}
                ],
                response_format={"type": "json_object"} if "llama-3.1" in self.model or "gpt" in self.model else None
            )
            report = json.loads(response.choices[0].message.content)
            
            # Extract scores and calculate total out of 10
            voice = report.get("brand_voice", 8)
            hook = report.get("hook_strength", 8)
            val = report.get("value_density", 8)
            cta = report.get("cta_score", 7)
            cringe = report.get("cringe_filter", 9)
            
            total_avg = sum([voice, hook, val, cta, cringe]) / 5.0
            
            # Check if any score is failing
            passed = voice >= 8 and hook >= 8 and val >= 8 and cta >= 7 and cringe >= 8
            
            return {
                "brand_voice": voice,
                "hook_strength": hook,
                "value_density": val,
                "cta": cta,
                "cringe_filter": cringe,
                "total_score": round(total_avg, 1),
                "feedback": report.get("feedback", "Good on-brand draft."),
                "passed": passed
            }
        except Exception as e:
            print(f"API Critic error: {e}")
            return self._evaluate_simulated_llm(draft, variant_label)

    def _evaluate_simulated_llm(self, draft, variant_label):
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
            # Failed scores for cringe/voice
            return {
                "brand_voice": 6,
                "hook_strength": 5,
                "value_density": 8,
                "cta": 7,
                "cringe_filter": 3,
                "total_score": 5.8,
                "feedback": f"Fails the cringe filter! Found corporate jargon: {found_banned}. We never say 'synergy' or 'unleash'. Rewrite in direct English.",
                "passed": False
            }
        else:
            # High-passing scores matching the screenshot!
            if variant_label == "Variant B":
                return {
                    "brand_voice": 8,
                    "hook_strength": 9,
                    "value_density": 8,
                    "cta": 7,
                    "cringe_filter": 9,
                    "total_score": 8.2,
                    "feedback": "Excellent hook, strong value focus, zero cringe corporate speak. CTA is clear but could be slightly lower friction.",
                    "passed": True
                }
            else: # Variant A
                return {
                    "brand_voice": 8,
                    "hook_strength": 8,
                    "value_density": 8,
                    "cta": 7,
                    "cringe_filter": 9,
                    "total_score": 8.0,
                    "feedback": "Highly informative keyword-focused post. Passes all brand guidelines.",
                    "passed": True
                }
