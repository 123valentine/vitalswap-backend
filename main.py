from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx
import json
import html

app = FastAPI()

# ✅ Function to rename VitalBank → SwapForce
def rename_keys(obj):
    if isinstance(obj, dict):
        return { (k.replace("VitalBank", "SwapForce") if isinstance(k, str) else k): rename_keys(v) for k, v in obj.items() }
    elif isinstance(obj, list):
        return [rename_keys(i) for i in obj]
    else:
        return obj


# ✅ Endpoint: /fees (HTML view)
@app.get("/fees", response_class=HTMLResponse)
async def fees_preview():
    api_url = "https://2kbbumlxz3.execute-api.us-east-1.amazonaws.com/fee/"
    data = {}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(api_url)
            response.raise_for_status()
            data = response.json()
    except Exception as e:
        print(f"Error fetching organizer API: {e}")
        data = {"error": "Unable to fetch data from organizer API."}

    data = rename_keys(data)
    json_str = html.escape(json.dumps(data, indent=4))

    # ✅ HTML styling and clickable mockups
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>SwapForce Fees Preview</title>
        <style>
            body {{ background-color:#0d1117; color:#c9d1d9; font-family: monospace; padding:20px; }}
            h2 {{ color:#58a6ff; }}
            pre {{ background:#161b22; padding:20px; border-radius:10px; }}
            .key {{ color:#ff79c6; }}
            .string {{ color:#f1fa8c; }}
            .number {{ color:#8be9fd; }}
            .brace {{ color:#50fa7b; }}
            a {{ color:#58a6ff; text-decoration:none; }}
            a:hover {{ text-decoration:underline; }}
            .clickable-section {{ margin-top:30px; }}
            button {{
                background:#238636; color:white; border:none; border-radius:6px;
                padding:10px 15px; font-size:16px; cursor:pointer;
            }}
            button:hover {{ background:#2ea043; }}
            .tag {{ margin-top:30px; color:#8be9fd; font-style:italic; }}
        </style>
    </head>
    <body>
        <h2>SwapForce Fees (Live Preview)</h2>
        <p>Fetches data from: <a href="{api_url}" target="_blank">{api_url}</a></p>
        
        <pre id="json">{json_str}</pre>

        <div class="clickable-section">
            <h3>Clickable UI Mock (frontend integration)</h3>
            <p>Below are visual elements that would connect to this endpoint in the real site:</p>
            <button onclick="window.open('{api_url}', '_blank')">😊 Start Learning</button>
            <button onclick="window.open('{api_url}', '_blank')">☹️ Learn More</button>
            <button onclick="window.open('{api_url}', '_blank')">📊 Calculate Fees</button>
        </div>

        <p class="tag">Referral Tag: @Valley Mind AI</p>

        <script>
            const pre = document.getElementById('json');
            pre.innerHTML = pre.textContent
                .replace(/"(\\w+)":/g, '<span class="key">"$1"</span>:')
                .replace(/: "([^"]*)"/g, ': <span class="string">"$1"</span>')
                .replace(/: ([0-9\\.]+)(,?)/g, ': <span class="number">$1</span>$2')
                .replace(/([{{}}])/g, '<span class="brace">$1</span>');
        </script>
    </body>
    </html>
    """
    return html_content


# ✅ Root endpoint to show info
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>Welcome to SwapForce Backend 🌐</h2>
    <p>Visit <a href='http://127.0.0.1:8000/fees' target='_blank'>/fees</a> to view live data.</p>
    <p>Referral: @Valley Mind AI</p>
    """