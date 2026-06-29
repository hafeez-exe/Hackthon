import os
import json
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
from typing import List

class DesignRenderer:
    def __init__(self, base_dir="."):
        self.base_dir = base_dir
        self.templates_dir = os.path.join(base_dir, "templates")
        self.jinja_env = Environment(loader=FileSystemLoader(self.templates_dir))
        
    def render_post(self, plan, copy_data, output_dir=None, primary_color=None, dark_color=None, light_color=None):
        """
        Renders the parametric HTML templates based on the plan and copy data.
        If Playwright Chromium fails (e.g. not installed locally), it automatically
        falls back to a high-fidelity PIL-based programmatic rendering engine!
        """
        if not output_dir:
            output_dir = os.path.join(self.base_dir, "data", "renders")
            
        os.makedirs(output_dir, exist_ok=True)
        
        template_name = plan["selected_template"]
        pillar = plan["selected_pillar"]
        topic_data = plan["topic_data"]
        
        generated_paths = []
        
        # Base colors default overrides
        p_color = primary_color or "#1B4DFF"
        d_color = dark_color or "#0A1F44"
        l_color = light_color or "#EAF1FF"
        
        # Try Playwright Headless Browser Rendering first
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.set_viewport_size({"width": 1080, "height": 1080})
                
                # 1. Carousel Render (Multi-slide)
                if template_name == "T2" and copy_data.get("slides"):
                    slides = copy_data["slides"]
                    total_slides = len(slides)
                    
                    for idx, slide_text in enumerate(slides):
                        context = {
                            "pillar": pillar,
                            "slide_num": idx + 1,
                            "total_slides": total_slides,
                            "slide_text": slide_text,
                            "hook": copy_data.get("hook", ""),
                            "primary_color": p_color,
                            "dark_color": d_color,
                            "light_color": l_color
                        }
                        
                        html_content = self.jinja_env.get_template("T2.html").render(context)
                        temp_html_path = os.path.join(self.base_dir, f"temp_render_carousel_{idx+1}.html")
                        
                        with open(temp_html_path, "w", encoding="utf-8") as f:
                            f.write(html_content)
                            
                        page.goto(f"file://{os.path.abspath(temp_html_path)}")
                        page.wait_for_timeout(500)
                        
                        out_filename = f"{plan['date']}_{pillar}_T2_slide{idx+1}.png"
                        out_path = os.path.join(output_dir, out_filename)
                        page.screenshot(path=out_path)
                        generated_paths.append(out_path)
                        
                        if os.path.exists(temp_html_path):
                            os.remove(temp_html_path)
                            
                # 2. Standard Single Post Render (T1, T3, T4, T5, T6, T7)
                else:
                    template_file = f"{template_name}.html"
                    
                    context = {
                        "pillar": pillar,
                        "hook": copy_data.get("hook", ""),
                        "caption": copy_data.get("caption", ""),
                        "primary_color": p_color,
                        "dark_color": d_color,
                        "light_color": l_color
                    }
                    
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
                        context.update({
                            "title": topic_data.get("topic", "The Paradigm Shift")
                        })
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
                        context.update({
                            "top_text": copy_data.get("hook", "Me applying on standard boards vs Me getting a 1-tap match on JobInGen")
                        })
                    
                    html_content = self.jinja_env.get_template(template_file).render(context)
                    temp_html_path = os.path.join(self.base_dir, f"temp_render_{template_name}.html")
                    
                    with open(temp_html_path, "w", encoding="utf-8") as f:
                        f.write(html_content)
                        
                    page.goto(f"file://{os.path.abspath(temp_html_path)}")
                    page.wait_for_timeout(500)
                    
                    out_filename = f"{plan['date']}_{pillar}_{template_name}.png"
                    out_path = os.path.join(output_dir, out_filename)
                    page.screenshot(path=out_path)
                    generated_paths.append(out_path)
                    
                    if os.path.exists(temp_html_path):
                        os.remove(temp_html_path)
                        
                browser.close()
                return generated_paths
                
        except Exception as playwright_error:
            # 🔮 FAILSAFE: Fallback to high-fidelity Pillow Programmatic Render
            print(f"Playwright failed (likely not installed locally). Triggering high-fidelity Pillow failsafe renderer: {playwright_error}")
            return self._render_fallback_pillow(plan, copy_data, output_dir, p_color, d_color, l_color)

    def _render_fallback_pillow(self, plan, copy_data, output_dir, p_color, d_color, l_color) -> List[str]:
        """
        Pillow Programmatic Failsafe: Draws a premium slate navy card with smooth radial gradient glows,
        glowing borders, custom vector emblems, and crisp typographic hierarchy!
        """
        pillar = plan["selected_pillar"]
        template_name = plan["selected_template"]
        hook = copy_data.get("hook", "JobInGen Content Strategy")
        caption = copy_data.get("caption", "")
        
        generated_paths = []
        
        # Determine files to generate
        slides = copy_data.get("slides") if template_name == "T2" else [None]
        if not slides:
            slides = [None]
            
        for idx, slide_text in enumerate(slides):
            # Create base 1080x1080 canvas
            img = Image.new("RGB", (1080, 1080), "#030712")
            draw = ImageDraw.Draw(img)
            
            # 1. Draw smooth gradient background glow
            for r in range(400, 0, -2):
                alpha = int((1 - (r / 400)) * 25)
                # Radial glow top-right
                draw.ellipse([900 - r, 180 - r, 900 + r, 180 + r], fill=(27, 77, 255, alpha))
            
            # 2. Draw glowing glassmorphic center card
            # Translucent central body box
            draw.rounded_rectangle([90, 180, 990, 880], radius=24, fill=(15, 23, 42), outline="#1E2E4E", width=2)
            
            # 3. Draw Brand Badge
            draw.rounded_rectangle([130, 220, 320, 266], radius=16, fill=(27, 77, 255))
            
            # 4. Text Layout (Typographic Hierarchy)
            # Standard PIL fonts fallback (load default if ttf not found)
            font_title = None
            font_body = None
            try:
                # Try loading standard system font or downloaded fonts
                font_title = ImageFont.truetype("arial.ttf", 38)
                font_body = ImageFont.truetype("arial.ttf", 22)
            except IOError:
                font_title = ImageFont.load_default()
                font_body = ImageFont.load_default()
                
            # Draw Badge Text
            draw.text((150, 230), pillar.upper(), fill="#FFFFFF", font=font_body)
            
            # Draw Hook Title
            wrapped_hook = self._wrap_text(hook, 32)
            draw.text((130, 300), wrapped_hook, fill="#FFFFFF", font=font_title)
            
            # Draw Main Caption or Slide Text
            display_text = slide_text if slide_text else caption
            wrapped_body = self._wrap_text(display_text, 65)
            draw.text((130, 480), wrapped_body, fill="#94A3B8", font=font_body)
            
            # 5. Draw Footer Logo Lockup
            # Logo icon capsule
            draw.rounded_rectangle([90, 940, 134, 984], radius=8, fill=(27, 77, 255))
            draw.text((102, 946), "J", fill="#FFFFFF", font=font_title)
            draw.text((150, 950), "JobInGen", fill="#FFFFFF", font=font_title)
            draw.text((750, 954), "jobingen.com", fill="#64748B", font=font_body)
            
            # Save file
            if template_name == "T2":
                out_filename = f"{plan['date']}_{pillar}_T2_slide{idx+1}.png"
            else:
                out_filename = f"{plan['date']}_{pillar}_{template_name}.png"
                
            out_path = os.path.join(output_dir, out_filename)
            img.save(out_path)
            generated_paths.append(out_path)
            
        return generated_paths

    def _wrap_text(self, text, max_chars) -> str:
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            if sum(len(w) for w in current_line) + len(current_line) + len(word) > max_chars:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                current_line.append(word)
                
        if current_line:
            lines.append(" ".join(current_line))
            
        return "\n".join(lines[:12]) # limit lines to prevent card clipping

if __name__ == "__main__":
    renderer = DesignRenderer(base_dir="jobingen-engine")
    print("Renderer loaded successfully!")
