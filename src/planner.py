import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import os
from datetime import datetime
from src.foundation.database import DatabaseStore

PILLARS_TARGETS = {
    "Educate": 0.40,
    "Opportunity": 0.25,
    "Proof": 0.15,
    "Brand": 0.10,
    "Culture": 0.10
}

TEMPLATE_MAPPING = {
    "Educate": ["T1", "T2", "T4"],
    "Opportunity": ["T3"],
    "Proof": ["T5", "T6"],
    "Brand": ["T1", "T4"],
    "Culture": ["T7", "T1"]
}

class ContentPlanner:
    def __init__(self, base_dir="."):
        self.base_dir = base_dir
        self.store = DatabaseStore(base_dir=base_dir)

    def calculate_math(self):
        """
        1. The Math: Reads the 30-day database history from SQLite,
        mathematically calculates actual distribution and identifies the pillar with the largest deficit.
        """
        history = self.store.get_post_history()
        
        # Take last 30 posts
        recent_history = history[-30:] if len(history) > 30 else history
        total_recent = len(recent_history)
        
        counts = {p: 0 for p in PILLARS_TARGETS.keys()}
        for post in recent_history:
            p = post.get("pillar")
            if p in counts:
                counts[p] += 1
                
        math_details = {}
        for pillar, target in PILLARS_TARGETS.items():
            actual_pct = (counts[pillar] / total_recent) if total_recent > 0 else 0
            deficit = target - actual_pct
            math_details[pillar] = {
                "target": target,
                "count": counts[pillar],
                "actual": actual_pct,
                "deficit": deficit
            }
            
        selected_pillar = max(math_details.keys(), key=lambda p: math_details[p]["deficit"])
        
        return selected_pillar, math_details

    def plan_content(self, date_str=None):
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
            
        selected_pillar, math_details = self.calculate_math()
        
        topic_data = {}
        template = "T1"
        
        if selected_pillar == "Opportunity":
            jobs = self.store.get_all_jobs()
            if jobs:
                job = random.choice(jobs)
                topic_data = {
                    "id": job["id"],
                    "title": job["title"],
                    "company": job["company"],
                    "location": job["location"],
                    "salary": job["salary"],
                    "perks": job["perks"],
                    "requirements": job["requirements"]
                }
                template = "T3"
            else:
                topic_data = {"id": "default", "title": "Junior Developer Openings"}
                template = "T3"
                
        elif selected_pillar == "Proof":
            testimonials = self.store.get_all_testimonials()
            if testimonials:
                t = random.choice(testimonials)
                topic_data = {
                    "id": t["id"],
                    "student_name": t["student_name"],
                    "university": t["university"],
                    "hired_role": t["hired_role"],
                    "company": t["company"],
                    "testimonial": t["testimonial"],
                    "metrics": t["metrics"]
                }
                template = random.choice(["T5", "T6"])
            else:
                topic_data = {"id": "default", "student_name": "Sarah J.", "company": "Tech Corp"}
                template = "T5"
                
        else: # Educate, Brand, Culture
            topics = self.store.get_all_topics()
            filtered_topics = [t for t in topics if t.get("pillar") == selected_pillar]
            
            if filtered_topics:
                t = random.choice(filtered_topics)
                topic_data = {
                    "id": t["id"],
                    "topic": t["topic"],
                    "key_points": t.get("key_points", [])
                }
            else:
                topic_data = {"id": "default", "topic": f"Default topic for {selected_pillar}"}
                
            templates = TEMPLATE_MAPPING.get(selected_pillar, ["T1"])
            template = templates[hash(date_str) % len(templates)]

        plan = {
            "date": date_str,
            "selected_pillar": selected_pillar,
            "selected_template": template,
            "topic_data": topic_data,
            "math_analysis": math_details
        }
        return plan

if __name__ == "__main__":
    planner = ContentPlanner(base_dir="jobingen-engine")
    plan = planner.plan_content()
    print("Planner initialized with SQLite database successfully!")
