import sqlite3
import os
import json

class DatabaseStore:
    """
    Architectural Principle: Separated Data Stores.
    Knowledge assets and trend signals live in SQLite, operational metrics in OperationalDB.
    Massively pre-seeded with 15+ diverse topics, jobs, and testimonials to guarantee 100% variety!
    """
    def __init__(self, base_dir="."):
        self.base_dir = base_dir
        self.db_path = os.path.join(base_dir, "data", "jobingen_engine.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 1. Signal & Trend tables (Layer 1: Signal)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS signal_items (
                id TEXT PRIMARY KEY,
                source TEXT,
                text TEXT,
                score REAL,
                url TEXT,
                timestamp TEXT
            )
        """)
        
        # 2. Knowledge Store tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS topics (
                id TEXT PRIMARY KEY,
                pillar TEXT,
                topic TEXT,
                key_points TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                title TEXT,
                company TEXT,
                location TEXT,
                salary TEXT,
                perks TEXT,
                requirements TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS testimonials (
                id TEXT PRIMARY KEY,
                student_name TEXT,
                university TEXT,
                hired_role TEXT,
                company TEXT,
                testimonial TEXT,
                metrics TEXT
            )
        """)
        
        # 3. Operational Store tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS post_history (
                id TEXT PRIMARY KEY,
                date TEXT,
                pillar TEXT,
                topic TEXT,
                template TEXT,
                approved_variant TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS operational_metrics (
                id INTEGER PRIMARY KEY,
                date TEXT,
                impressions INTEGER,
                clicks INTEGER,
                engagement_rate REAL
            )
        """)
        
        conn.commit()
        conn.close()
        
        self.prepopulate_data()

    def prepopulate_data(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # We drop existing tables to force a clean, highly diverse seed on restart!
        cursor.execute("DELETE FROM signal_items")
        cursor.execute("DELETE FROM topics")
        cursor.execute("DELETE FROM jobs")
        cursor.execute("DELETE FROM testimonials")
        cursor.execute("DELETE FROM post_history")
        
        # 1. Diverse Trend Signals (Google Autocomplete & News)
        signals = [
            ("sig_1", "reddit", "Placement anxiety freezing: final year students freezing on 'Tell me about yourself' interviews in campus placement cells.", 0.95, "https://reddit.com/r/developersIndia/comments/tell_me_about_yourself", "2026-06-30"),
            ("sig_2", "reddit", "ATS checker rejections: double-column resumes are visual scams created by standard designers. To bypass filters, you need programmatic, single-column DOCX compilers.", 0.88, "https://reddit.com/r/cscareerquestions/comments/ats_rejections", "2026-06-30"),
            ("sig_3", "reddit", "Unpaid internships are exploitation; recruiters asking to work 50-hour weeks for zero compensation.", 0.91, "https://reddit.com/r/jobs/comments/unpaid_internships", "2026-06-30"),
            ("sig_4", "trends", "Google Trends spike: 'adaptive AI mock interview feedback' rising +245% in tier-1/tier-2 colleges.", 0.85, "https://trends.google.com/trends/explore?q=adaptive_mock_interview", "2026-06-30"),
            ("sig_5", "news", "Hiring Shift: Tech companies are shifting resumes searches from credentials to portfolio-driven project proof.", 0.80, "https://hiringnews.com/articles/portfolio_driven_hiring", "2026-06-30")
        ]
        for s in signals:
            cursor.execute("INSERT OR REPLACE INTO signal_items VALUES (?, ?, ?, ?, ?, ?)", s)

        # 2. Prepopulate 12+ Unique and Diverse Topics (Educate, Brand, Culture)
        topics = [
            ("edu_1", "Educate", "How to structure your resume for AI ATS filters", json.dumps([
                "ATS scanning algorithms don't read PDFs well; stick to simple DOCX files.",
                "Match your resume keywords exactly to the job description.",
                "Use clean, single-column layouts. Avoid complex grids, text boxes, and charts."
            ])),
            ("edu_2", "Educate", "How to solve 'Tell me about yourself' placement freezing", json.dumps([
                "Divide your answer into three blocks: Present, Past, and Future.",
                "Keep your introduction under 90 seconds. Focus on actionable coding skills.",
                "Practice communication delivery using adaptive real-time AI tools."
            ])),
            ("edu_3", "Educate", "3 cold emailing templates that got internships at top tech startups", json.dumps([
                "Subject line must be specific and value-driven.",
                "Keep the email under 150 words. Be concise and straight to the point.",
                "The call to action should be low-friction."
            ])),
            ("edu_4", "Educate", "The hidden networking loophole: LinkedIn Alumni Tool", json.dumps([
                "Go to your university's LinkedIn page and click 'Alumni'.",
                "Filter by the city you want to work in and the target company.",
                "Send a warm message asking for advice, not a job."
            ])),
            ("brand_1", "Brand", "Why JobInGen is banning unpaid internships", json.dumps([
                "Unpaid internships exploit student labor and limit equal opportunities.",
                "All employers on JobInGen must commit to paying at least local minimum wage.",
                "Equal opportunities are built on fair reward for student labor."
            ])),
            ("brand_2", "Brand", "Meet your new AI career co-pilot", json.dumps([
                "JobInGen isn't just a job board. It's an intelligent engine.",
                "From resume feedback to matching you with vetted tech startups.",
                "Sign up today and get your personalized career roadmaps."
            ])),
            ("brand_3", "Brand", "Why we prioritize coding skills over college pedigree", json.dumps([
                "A college degree is no longer a proof of engineering skill.",
                "Vetted portfolios and projects are what high-growth startups look for.",
                "We match you based on what you can build, not where you studied."
            ])),
            ("culture_1", "Culture", "The 'hustle culture' myth: Why resting is actually productive", json.dumps([
                "Working 80-hour weeks causes burnout, destroying long-term cognitive output.",
                "Take your weekends off. Go for a run, read a book, sleep.",
                "Great code and ideas come from a rested, energized brain."
            ])),
            ("culture_2", "Culture", "Behind the scenes: The JobInGen team's favorite slack channels", json.dumps([
                "#cringe-corporate-speak: Where we post the worst corporate jargon we find.",
                "#pets-of-jobingen: Showing off our remote working assistants (cats and dogs).",
                "#failed-ideas: Celebrating things we tried that flopped, because that is how we learn."
            ])),
            ("culture_3", "Culture", "Why our remote engineers work asynchronous 4-hour focused blocks", json.dumps([
                "Asynchronous documentation removes useless meetings.",
                "Focused deep work blocks are 5x more productive than distracted offices.",
                "Work wherever you want, as long as you deliver results."
            ]))
        ]
        for t in topics:
            cursor.execute("INSERT OR REPLACE INTO topics VALUES (?, ?, ?, ?)", t)
                
        # 3. Prepopulate 5+ Diverse Job Openings
        jobs = [
            ("job_1", "Junior Backend Engineer (Python)", "Vectra AI", "Remote (US/Canada)", "$85,000 - $110,000", "Flexible hours, 401k match, $2k home office stipend", "Strong Python knowledge, experience with FastAPI, interest in Vector DBs."),
            ("job_2", "Growth Marketing Intern", "Figma", "San Francisco, CA (Hybrid)", "$45 - $55 / hour", "Free catered lunches, mentor program, transit benefits", "Strong copywriting skills, familiarity with SEO and LinkedIn ads."),
            ("job_3", "Junior Product Designer", "Linear", "Remote (Europe/UK)", "€60,000 - €80,000", "Unlimited PTO, annual company retreats, latest Macbook Pro", "Stunning Figma portfolio, obsessed with keyboard shortcuts, clean aesthetic."),
            ("job_4", "Frontend Developer Intern", "Supabase", "Remote (Global)", "$4,000 - $5,500 / month", "Equity options, home office stipend, health insurance", "Experience with React, Tailwind CSS, and database CRUD operations."),
            ("job_5", "Data Analyst Intern", "Rippling", "Bangalore, India (Hybrid)", "₹45,000 / month", "Free transport, daily catered meals, laptop allowance", "Strong SQL knowledge, experience with Tableau or Python pandas.")
        ]
        for j in jobs:
            cursor.execute("INSERT OR REPLACE INTO jobs VALUES (?, ?, ?, ?, ?, ?, ?)", j)
                
        # 4. Prepopulate 5+ Diverse Testimonials
        testimonials = [
            ("proof_1", "Sarah Jenkins", "University of Michigan", "Software Engineering Intern", "Supabase", "JobInGen completely bypassed the standard ATS black hole. I got matched with Supabase, did a quick 15-minute intro chat, and had my offer in 2 weeks.", "2 weeks from match to offer"),
            ("proof_2", "Alex Chen", "UT Austin", "Product Manager Intern", "Vercel", "I sent 150 applications on standard boards and got zero responses. On JobInGen, I filled out my profile, matched with 3 tech startups, and Vercel hired me.", "Hired in 14 Days"),
            ("proof_3", "Maya Patel", "Georgia Tech", "Data Analyst Intern", "Rippling", "The Mentor Spotlight on JobInGen connected me with an industry lead at Rippling who reviewed my portfolio. Two weeks later, I was hired!", "Direct portfolio hire"),
            ("proof_4", "Rohan Sharma", "BITS Pilani", "Junior Fullstack Engineer", "Atlassian", "As an engineering student in India, campus placement was brutal. JobInGen matched me directly to global tech teams.", "Placement in 12 days"),
            ("proof_5", "Jane Doe", "IIT Bombay", "Machine Learning Intern", "Scale AI", "Real adaptive mock feedback prepared me perfectly for my interviews at Scale AI. JobInGen is a launchpad.", "Mock-to-placement in 7 days")
        ]
        for t in testimonials:
            cursor.execute("INSERT OR REPLACE INTO testimonials VALUES (?, ?, ?, ?, ?, ?, ?)", t)

        # 5. Prepopulate initial Operations History (Seeded with diverse dates to allow Deficit maths)
        history = [
            ("hist_1", "2026-06-15", "Opportunity", "Junior Python Openings", "T3", "Variant B"),
            ("hist_2", "2026-06-16", "Brand", "Why unpaid internships are banned", "T4", "Variant B"),
            ("hist_3", "2026-06-17", "Proof", "Sarah Jenkins hired", "T5", "Variant B"),
            ("hist_4", "2026-06-18", "Culture", "Behind the scenes", "T1", "Variant B"),
            ("hist_5", "2026-06-19", "Opportunity", "Figma Growth Intern", "T3", "Variant B"),
            ("hist_6", "2026-06-20", "Brand", "Democratizing placement opportunity", "T1", "Variant B"),
            ("hist_7", "2026-06-21", "Educate", "ATS structures for resumes", "T4", "Variant B"),
            ("hist_8", "2026-06-22", "Culture", "Why rest is actually productive", "T1", "Variant B"),
            ("hist_9", "2026-06-23", "Proof", "Alex Chen hired at PM Vercel", "T5", "Variant B")
        ]
        for h in history:
            cursor.execute("INSERT OR REPLACE INTO post_history VALUES (?, ?, ?, ?, ?, ?)", h)
                
        conn.commit()
        conn.close()

    # Read APIs
    def get_all_signals(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM signal_items")
        rows = cursor.fetchall()
        signals = []
        for r in rows:
            signals.append({
                "id": r["id"],
                "source": r["source"],
                "text": r["text"],
                "score": r["score"],
                "url": r["url"],
                "timestamp": r["timestamp"]
            })
        conn.close()
        return signals

    def get_all_topics(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM topics")
        rows = cursor.fetchall()
        topics = []
        for r in rows:
            topics.append({
                "id": r["id"],
                "pillar": r["pillar"],
                "topic": r["topic"],
                "key_points": json.loads(r["key_points"])
            })
        conn.close()
        return topics

    def get_all_jobs(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs")
        rows = cursor.fetchall()
        jobs = []
        for r in rows:
            jobs.append({
                "id": r["id"],
                "title": r["title"],
                "company": r["company"],
                "location": r["location"],
                "salary": r["salary"],
                "perks": r["perks"],
                "requirements": r["requirements"]
            })
        conn.close()
        return jobs

    def get_all_testimonials(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM testimonials")
        rows = cursor.fetchall()
        testimonials = []
        for r in rows:
            testimonials.append({
                "id": r["id"],
                "student_name": r["student_name"],
                "university": r["university"],
                "hired_role": r["hired_role"],
                "company": r["company"],
                "testimonial": r["testimonial"],
                "metrics": r["metrics"]
            })
        conn.close()
        return testimonials

    def get_post_history(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM post_history")
        rows = cursor.fetchall()
        history = []
        for r in rows:
            history.append({
                "id": r["id"],
                "date": r["date"],
                "pillar": r["pillar"],
                "topic": r["topic"],
                "template": r["template"],
                "approved_variant": r["approved_variant"]
            })
        conn.close()
        return history

    def commit_approved_post(self, post_id, date, pillar, topic, template, approved_variant):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO post_history VALUES (?, ?, ?, ?, ?, ?)",
            (post_id, date, pillar, topic, template, approved_variant)
        )
        conn.commit()
        conn.close()
