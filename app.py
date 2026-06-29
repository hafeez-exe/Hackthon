import os
import sys
from flask import Flask, jsonify, request, send_from_directory, render_template_string
from flask_cors import CORS

# Add base_dir to path so src modules are accessible
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.append(base_dir)

from src.orchestrator import Orchestrator
from src.planner import ContentPlanner
from src.foundation.database import DatabaseStore
from src.intelligence.trend_scout import TrendScout

app = Flask(__name__)
CORS(app)

# Setup folders
renders_dir = os.path.join(base_dir, "data", "renders")
os.makedirs(renders_dir, exist_ok=True)

# Initialize Stores & Orchestrator
store = DatabaseStore(base_dir=base_dir)
orchestrator = Orchestrator(base_dir=base_dir)

@app.route("/")
def index():
    # Return the beautiful single-page dashboard HTML
    with open(os.path.join(base_dir, "web", "templates", "index.html"), "r", encoding="utf-8") as f:
        html = f.read()
    return render_template_string(html)

@app.route("/api/status", methods=["GET"])
def get_status():
    """
    Returns the current math analysis from the 30-day post database history,
    plus a list of all rendered posts.
    """
    try:
        planner = ContentPlanner(base_dir=base_dir)
        selected_pillar, math_details = planner.calculate_math()
        
        # Get list of rendered files in renders_dir
        files = os.listdir(renders_dir)
        pngs = sorted([f for f in files if f.endswith(".png")], reverse=True)
        txts = sorted([f for f in files if f.endswith(".txt")], reverse=True)
        
        return jsonify({
            "status": "success",
            "next_suggested_pillar": selected_pillar,
            "math_analysis": math_details,
            "renders": {
                "pngs": pngs,
                "txts": txts
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    """
    Exposes active job listings from the SQLite Knowledge Store!
    """
    try:
        jobs = store.get_all_jobs()
        return jsonify({
            "status": "success",
            "jobs": jobs
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/trends", methods=["GET"])
def get_trends():
    """
    Exposes active Google Trends and RSS news signals!
    """
    try:
        scout = TrendScout(base_dir=base_dir)
        themes = scout.scout_and_synthesize()
        results = scout.score_themes(themes)
        
        # Format the output for the UI
        trends_list = []
        for r in results["all_scores"]:
            trends_list.append({
                "label": r["theme"].label,
                "score": r["score"],
                "relevance": r["metrics"]["audience_relevance"] * 100,
                "velocity": r["metrics"]["trend_velocity"] * 100
            })
            
        return jsonify({
            "status": "success",
            "trends": trends_list
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/generate-today", methods=["POST"])
def generate_today():
    """
    Triggers a run of the Orchestrator for today, generating A/B Variants side-by-side.
    Supports dynamic brand colors customization and custom seed topics!
    """
    try:
        data = request.get_json() or {}
        force_pillar = data.get("pillar")
        p_color = data.get("primary_color")
        d_color = data.get("dark_color")
        l_color = data.get("light_color")
        seed_topic = data.get("seed_topic")
        
        report = orchestrator.run_pipeline_for_date(
            force_pillar=force_pillar,
            primary_color=p_color,
            dark_color=d_color,
            light_color=l_color,
            seed_topic=seed_topic
        )
        return jsonify({
            "status": "success",
            "report": report
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/generate-runway", methods=["POST"])
def generate_runway():
    """
    Triggers a sequential run of the Orchestrator for the next 14 days.
    """
    try:
        reports = orchestrator.generate_runway(days=14)
        return jsonify({
            "status": "success",
            "reports": reports
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/approve", methods=["POST"])
def approve_variant():
    """
    Human-in-the-loop review approval queue. Updates DB history and schedules publishing!
    """
    try:
        data = request.get_json() or {}
        date_str = data.get("date")
        pillar = data.get("pillar")
        template = data.get("template")
        topic_title = data.get("topic_title")
        approved_variant = data.get("approved_variant") # "Variant A" or "Variant B"
        copy_data = data.get("copy_data")
        
        res_data = orchestrator.approve_variant(
            date_str=date_str,
            pillar=pillar,
            template=template,
            topic_title=topic_title,
            approved_variant=approved_variant,
            copy_data=copy_data
        )
        return jsonify(res_data)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/render-html", methods=["POST"])
def render_html_endpoint():
    try:
        data = request.get_json() or {}
        plan = data.get("plan", {})
        variant = data.get("variant", "B")
        copy_data = data.get(f"variant_{variant.lower()}", {})
        colors = data.get("colors", {})
        
        from src.rendering.renderer import DesignRenderer
        renderer = DesignRenderer(base_dir=os.path.dirname(os.path.abspath(__file__)))
        
        template_name = plan.get("selected_template")
            
        context = {
            "pillar": plan.get("selected_pillar"),
            "hook": copy_data.get("hook", ""),
            "caption": copy_data.get("caption", ""),
            "primary_color": colors.get("primary_color", "#1B4DFF"),
            "dark_color": colors.get("dark_color", "#0A1F44"),
            "light_color": colors.get("light_color", "#EAF1FF")
        }
        
        topic_data = plan.get("topic_data", {})
        if template_name == "T3":
            context.update({
                "company": topic_data.get("company", "Figma"),
                "title": topic_data.get("title", "Growth Marketing Intern"),
                "location": topic_data.get("location", "Hybrid"),
                "salary": topic_data.get("salary", "$45 - $55 / hour"),
                "perks": topic_data.get("perks", "Catered lunches"),
                "requirements": topic_data.get("requirements", "Relevant experience")
            })
        elif template_name == "T4":
            context.update({"title": topic_data.get("topic", "The Paradigm Shift")})
        elif template_name in ["T5", "T6"]:
            context.update({
                "student_name": topic_data.get("student_name", "Sarah Jenkins"),
                "university": topic_data.get("university", "UT Austin"),
                "hired_role": topic_data.get("hired_role", "Engineering Intern"),
                "company": topic_data.get("company", "Supabase"),
                "testimonial": topic_data.get("testimonial", copy_data.get("caption", "Incredible matching platform!")),
                "metrics": topic_data.get("metrics", "Matched in 2 weeks")
            })
        elif template_name == "T7":
            context.update({"top_text": copy_data.get("hook", "Me applying vs 1-tap match")})
            
        html_content = renderer.jinja_env.get_template(f"{template_name}.html").render(context)
        injection = """
        <script>
            document.querySelectorAll('div, span, p, h1, h2, h3, li').forEach(el => {
                if (el.className.includes('hook-') || el.className.includes('-text') || el.className.includes('slide-') || el.className.includes('col-title') || ['P', 'H1', 'H2', 'H3', 'SPAN'].includes(el.tagName)) {
                    el.setAttribute('contenteditable', 'true');
                }
            });
        </script>
        <style>[contenteditable='true']:hover { outline: 2px dashed #1B4DFF; cursor: text; border-radius: 4px; }</style>
        </body>
        """
        html_content = html_content.replace("</body>", injection)
        
        return jsonify({"status": "success", "html": html_content})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/render-raw-html", methods=["POST"])
def render_raw_html():
    try:
        data = request.get_json() or {}
        plan = data.get("plan", {})
        variant = data.get("variant", "A") # "A" or "B"
        raw_html = data.get("html", "")
        
        from src.rendering.renderer import DesignRenderer
        renderer = DesignRenderer(base_dir=os.path.dirname(os.path.abspath(__file__)))
        
        # Save raw HTML to temp
        temp_html_path = os.path.join(renderer.base_dir, "templates", f"temp_raw_{variant}.html")
        with open(temp_html_path, "w", encoding="utf-8") as f:
            f.write(raw_html)
            
        import traceback
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
                page.goto(f"file://{os.path.abspath(temp_html_path)}")
                page.wait_for_timeout(500)
                
                # Determine exact output path to overwrite
                pillar = plan.get("selected_pillar", "Educate")
                template_name = plan.get("selected_template", "T1")
                date = plan.get("date", "2026-01-01")
                
                out_filename = f"{date}_{pillar}_{template_name}_variant_{'b' if variant == 'B' else 'a'}.png"
                output_dir = os.path.join(renderer.base_dir, "data", "renders")
                os.makedirs(output_dir, exist_ok=True)
                out_path = os.path.join(output_dir, out_filename)
                
                page.screenshot(path=out_path)
                browser.close()
        except Exception as e:
            print("Playwright Raw Render failed:", e)
            
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)
            
        return jsonify({"status": "success"})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/update-render-colors", methods=["POST"])
def update_render_colors():
    try:
        data = request.get_json() or {}
        plan = data.get("plan", {})
        colors = data.get("colors", {})
        
        from src.rendering.renderer import DesignRenderer
        renderer = DesignRenderer(base_dir=os.path.dirname(os.path.abspath(__file__)))
        
        # Render Variant A
        renders_a = renderer.render_post(
            plan, 
            data.get("variant_a", {}), 
            output_dir=None,
            primary_color=colors.get("primary_color"),
            dark_color=colors.get("dark_color"),
            light_color=colors.get("light_color")
        )
        new_paths = []
        import os
        for p in renders_a:
            d_n = os.path.dirname(p)
            b_n = os.path.basename(p)
            n_p = os.path.join(d_n, b_n.replace(".png", "_variant_a.png"))
            if os.path.exists(p):
                os.replace(p, n_p)
            new_paths.append(n_p)
            
        # Render Variant B
        renders_b = renderer.render_post(
            plan, 
            data.get("variant_b", {}), 
            output_dir=None,
            primary_color=colors.get("primary_color"),
            dark_color=colors.get("dark_color"),
            light_color=colors.get("light_color")
        )
        for p in renders_b:
            d_n = os.path.dirname(p)
            b_n = os.path.basename(p)
            n_p = os.path.join(d_n, b_n.replace(".png", "_variant_b.png"))
            if os.path.exists(p):
                os.replace(p, n_p)
            new_paths.append(n_p)
            
        return jsonify({"status": "success", "render_paths": new_paths})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/renders/<path:filename>")
def serve_render(filename):
    """
    Serves generated images and copy text files so they are visible on the dashboard.
    """
    return send_from_directory(renders_dir, filename)

if __name__ == "__main__":
    print("*" * 60)
    print("   JOBINGEN CONTENT CREATION ENGINE - WEB CONTROL ROOM")
    print("   Dashboard running at: http://127.0.0.1:8000")
    print("*" * 60)
    app.run(host="0.0.0.0", port=8000, debug=True, use_reloader=False)

