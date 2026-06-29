import os
from typing import Dict, Any, Literal
from src.foundation.contracts import Angle, PlatformBrief, Theme

class AudienceModeler:
    """
    Audience Modeler ("The Empath").
    Turns a trending topic into an emotional human truth. Names the anxiety, tension, or fear.
    """
    def model_tension(self, theme: Theme) -> str:
        label = theme.label.lower()
        if "freezing" in label:
            return "Placement anxiety and severe impostor syndrome when asked a simple open-ended question like 'Tell me about yourself' on the spot."
        elif "ats" in label:
            return "Extreme frustration and feeling like your efforts are being thrown into a black hole because programmatic resumes checkers reject beautiful designs."
        else:
            return "Feeling of being left behind by recruiters who prioritize pedigree over hard coding skills and projects."

class AngleSelector:
    """
    Angle Selector ("The Strategist").
    Applies the Differentiation Filter (Section 9) to reject generic advice and find the JobInGen take.
    """
    def select_angle(self, theme: Theme, tension: str) -> Angle:
        label = theme.label.lower()
        if "freezing" in label:
            return Angle(
                take="Practice is useless if you do not get instant, objective, adaptive feedback on your specific interview communication slips.",
                product_tie="Adaptive AI Mock Interviewer (real-time communication scoring)",
                why_only_jobingen="JobInGen's AI doesn't just show a questions list; its voice-analytic engines grade vocal pacing, confidence blocks, and filler words."
            )
        elif "ats" in label:
            return Angle(
                take="Double-column resumes are visual scams created by standard designers. To bypass filters, you need programmatic, single-column DOCX compilers.",
                product_tie="ATS-Optimized resume builder",
                why_only_jobingen="JobInGen's resume compiler runs real ATS-simulation parsers on your document before you ever send it."
            )
        else:
            return Angle(
                take="Unpaid internships are design flaws. The only way to prove skill without pedigree is through vetted, portfolio-driven matched projects.",
                product_tie="Curated placements and bootcamps",
                why_only_jobingen="All companies on JobInGen must commit to paying at least local minimum wage."
            )

class PlatformStrategist:
    """
    Platform Strategist ("The Native Speaker").
    Translates the same creative angle into genuinely different briefs for LinkedIn vs Instagram.
    """
    def create_briefs(self, angle: Angle) -> Dict[str, PlatformBrief]:
        briefs = {}
        
        # LinkedIn Brief Playbook
        briefs["linkedin"] = PlatformBrief(
            platform="linkedin",
            format="Text post / Document slide pack",
            hook_style="A contrarian insight or numeric industry truth",
            length_rule="Mini-essay with rich value density",
            cta_type="Drive reach: Comment / repost / follow",
            tone="Professional, authoritative, yet student-first peer"
        )
        
        # Instagram Brief Playbook
        briefs["instagram"] = PlatformBrief(
            platform="instagram",
            format="One bold relatable visual graphic + 1 slide",
            hook_style="POV / emotionally-resonant text on image itself",
            length_rule="Punchy, front-loaded caption",
            cta_type="Drive engagement: Save this / send to a friend",
            tone="Casual, highly peer-to-peer, raw and empathetic"
        )
        
        return briefs
