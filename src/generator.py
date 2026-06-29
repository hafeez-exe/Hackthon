import os
import json
import random
from openai import OpenAI

class CopyGenerator:
    def __init__(self, base_dir="."):
        self.base_dir = base_dir
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.groq_key = os.environ.get("GROQ_API_KEY")
        
        # Groq is prioritized if key is present (unbelievable speeds for live demos!)
        if self.groq_key:
            self.client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=self.groq_key
            )
            self.model = "llama-3.1-8b-instant"
            print("🚀 CopyGenerator initialized using Groq API (high-speed Llama-3.1-8b)!")
        elif self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            self.model = "gpt-4o-mini"
            print("✨ CopyGenerator initialized using OpenAI API!")
        else:
            self.client = None
            self.model = "simulation"
            print("💻 CopyGenerator running in local Simulation Mode!")

    def generate_variants(self, plan, attempt=1, feedback=None):
        """
        Generates both Variant A and Variant B copies for A/B testing
        """
        if self.client:
            return self._generate_real_variants_llm(plan, attempt, feedback)
        return self._generate_simulated_variants_llm(plan, attempt, feedback)

    def _generate_real_variants_llm(self, plan, attempt, feedback):
        system_prompt = """You are 'Gen', the premium Brand Persona for JobInGen (strategist + creative director). 
Your tone is student-first, sharp, direct, value-dense, and completely free of corporate jargon or cliches. 
You write high-converting social media posts (LinkedIn/Instagram) that deliver actual career value to students.

Never use: 'synergy', 'unleash', 'deep dive', 'delve', 'supercharge', 'tapestry', 'revolutionary', or 'game-changer'. 
Always write in clean, active English."""

        user_prompt = f"""Generate TWO distinct social media post variants (Variant A and Variant B) for the following topic:
Pillar: {plan['selected_pillar']}
Template: {plan['selected_template']}
Topic details: {json.dumps(plan['topic_data'])}

Angles to explore:
- Variant A: Focus on keyword-driven resume visibility ("With keywords" vs "Without keywords").
- Variant B: Focus on resume relevance and bypass tactics over keyword stuffing ("ATS bots" vs "Hiring Managers").

Output raw JSON containing exactly this structure:
{{
  "variant_a": {{
     "hook": "High impact headline (max 8 words)",
     "caption": "Compelling LinkedIn body text (short paragraphs, bullet points)",
     "hashtags": ["hashtag1", "hashtag2", "hashtag3", "hashtag4", "hashtag5"],
     "cta": "Actionable call to action",
     "alt_text": "Accessibility description for the graphic"
  }},
  "variant_b": {{
     "hook": "High impact headline (max 8 words)",
     "caption": "Compelling LinkedIn body text (different angle, short paragraphs, bullet points)",
     "hashtags": ["hashtag1", "hashtag2", "hashtag3", "hashtag4", "hashtag5"],
     "cta": "Actionable call to action",
     "alt_text": "Accessibility description for the graphic"
  }}
}}

Current Attempt: {attempt}
"""
        if feedback:
            user_prompt += f"\nPrevious attempt failed. Critic Feedback:\n{feedback}\nPlease self-correct and ensure both variants comply with brand guidelines."

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"} if "llama-3.1" in self.model or "gpt" in self.model else None
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"API Variant Error, falling back to simulation: {e}")
            return self._generate_simulated_variants_llm(plan, attempt, feedback)

    def _generate_simulated_variants_llm(self, plan, attempt, feedback):
        # Local simulation that returns exact visual matching to user's screenshot
        if attempt == 1 and not feedback:
            # First try has some corporate jargon to trigger Critic AI self-correct live demo!
            return {
                "variant_a": {
                    "hook": "Unleash Resume Synergy with Keywords! 🚀",
                    "caption": "Hey connection sphere! Are you ready to deep-dive into the game-changing paradigm shift of using target keywords to supercharge your application visibility and bypass the ATS filters? \n\nLet's unpack how to leverage keywords to synergize your professional path!",
                    "hashtags": ["#JobInGen", "#ATSTips", "#ResumeHacks", "#JobSearch", "#CareerAdvice"],
                    "cta": "Save this post to supercharge your application!",
                    "alt_text": "Split screen layout showing keyword-optimized resume parameters."
                },
                "variant_b": {
                    "hook": "Beat the ATS Bot in 5 Steps",
                    "caption": "Want to know the secret to getting past applicant tracking systems? It's not about keywords, it's about relevance. Save this to optimize your resume for your dream job",
                    "hashtags": ["#JobInGen", "#ResumeTips", "#ATS", "#CareerAdvice", "#JobSearch"],
                    "cta": "Click apply on JobInGen to skip the ATS completely.",
                    "alt_text": "Split screen layout showing ATS bot bypass tactics."
                }
            }
        
        # Perfect passed version matching the user's screenshot
        return {
            "variant_b": {
                "hook": "Beat the ATS Bot in 5 Steps",
                "caption": "Want to know the secret to getting past applicant tracking systems? It's not about keywords, it's about relevance. Save this to optimize your resume for your dream job",
                "hashtags": ["#JobInGen", "#ResumeTips", "#ATS", "#CareerAdvice", "#JobSearch"],
                "cta": "Join JobInGen to send your resume directly to vetted hiring manager dashboards.",
                "alt_text": "Get Past ATS Bots vs Get Noticed by Hiring Managers comparison grid."
            },
            "variant_a": {
                "hook": "Beat the ATS bots in 5 steps",
                "caption": "Want to get past the ATS and in front of a human? Use keywords from the job description to increase your resume's visibility, save this post for your next application",
                "hashtags": ["#JobInGen", "#ATSTips", "#ResumeHacks", "#JobSearch", "#CareerAdvice"],
                "cta": "Check your resume keyword density using JobInGen's scanner.",
                "alt_text": "Without keywords vs With keywords resume comparison layout."
            }
        }
