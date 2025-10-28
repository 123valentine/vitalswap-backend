from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx
import json
import html

app = FastAPI()

def rename_keys(obj):
    if isinstance(obj, dict):
        return { (k.replace("VitalBank", "SwapForce") if isinstance(k, str) else k): rename_keys(v) for k, v in obj.items() }
    elif isinstance(obj, list):
        return [rename_keys(i) for i in obj]
    else:
        return obj

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

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>SwapForce Fees Preview</title>
        <style>
            body {{ background-color:#1e1e2f; color:#c5c8c6; font-family: monospace; padding:20px; }}
            .key {{ color:#ff79c6; }}
            .string {{ color:#f1fa8c; }}
            .number {{ color:#8be9fd; }}
            .brace {{ color:#50fa7b; }}
            pre {{ white-space: pre-wrap; word-wrap: break-word; }}
            a {{ color: #8be9fd; text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h2>SwapForce Fees (Live Preview)</h2>
        <p>Click to open the organizer API directly: <a href="{api_url}" target="_blank">{api_url}</a></p>
        <pre id="json">{json_str}</pre>
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