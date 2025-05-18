import os
from pathlib import Path
from flask import Flask, render_template_string, send_file

# 1. Create absolute paths
BASE_DIR = Path(__file__).parent.absolute()
TEMPLATE_DIR = BASE_DIR / "templates"

# 2. Create template if missing
if not (TEMPLATE_DIR / "index.html").exists():
    TEMPLATE_DIR.mkdir(exist_ok=True)
    (TEMPLATE_DIR / "index.html").write_text("""
    <!DOCTYPE html>
    <html>
    <head><title>TEST</title><style>body{background:red;}</style></head>
    <body><h1>WORKING!</h1></body>
    </html>
    """)

# 3. Initialize Flask with explicit paths
app = Flask(__name__, template_folder=str(TEMPLATE_DIR))

# 4. Debug route to verify paths
@app.route('/debug')
def debug():
    return {
        "template_dir": str(TEMPLATE_DIR),
        "files": os.listdir(TEMPLATE_DIR),
        "cwd": os.getcwd(),
        "template_exists": os.path.exists(TEMPLATE_DIR / "index.html")
    }

# 5. Main route with fallback
@app.route('/')
def home():
    try:
        return render_template_string("""
            {% extends 'index.html' %}
            {% block content %}<h2>Extended Template</h2>{% endblock %}
        """)
    except Exception as e:
        # Ultimate fallback - return direct HTML
        return """
        <!DOCTYPE html>
        <html>
        <head><title>FALLBACK</title><style>body{background:lightblue;}</style></head>
        <body>
            <h1>Direct HTML Response</h1>
            <p>Template system failed. Debug info:</p>
            <pre>{{ error }}</pre>
        </body>
        </html>
        """.replace("{{ error }}", str(e))

if __name__ == '__main__':
    print(f"Template directory: {TEMPLATE_DIR}")
    print(f"Files in template dir: {os.listdir(TEMPLATE_DIR)}")
    app.run(host='0.0.0.0', port=5000, debug=True)