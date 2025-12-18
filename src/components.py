import streamlit.components.v1 as components
import html

def render_emoji_grid(results, columns=3):
    """
    Renders a responsive grid of emoji cards with hover details and copy-to-clipboard functionality.
    """
    cards_html = ""
    for res in results:
        char = res['metadata'].get('character', '❓')
        # Escape the document text to prevent HTML injection issues and handle special chars
        desc = html.escape(res['document'])
        score = 1 - res['distance']
        
        cards_html += f"""
        <div class="card" onclick="copyToClipboard('{char}')">
            <div class="char">{char}</div>
            <div class="score">Match: {score:.4f}</div>
            <div class="details">
                <p>{desc}</p>
                <span class="hint">Click to Copy</span>
            </div>
        </div>
        """
        
    # Complete HTML Component
    component_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {{
            background-color: transparent;
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 10px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat({columns}, 1fr);
            gap: 15px;
        }}
        .card {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            aspect-ratio: 1;
            color: #ffffff;
            backdrop-filter: blur(10px);
        }}
        .card:hover {{
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        }}
        .char {{
            font-size: 56px;
            margin-bottom: 8px;
        }}
        .score {{
            font-size: 12px;
            color: #787878;
        }}
        .details {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(15, 15, 15, 0.95);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            opacity: 0;
            transition: opacity 0.2s ease;
            padding: 15px;
            box-sizing: border-box;
            text-align: center;
        }}
        .card:hover .details {{
            opacity: 1;
        }}
        .details p {{
            font-size: 13px;
            line-height: 1.4;
            color: #e0e0e0;
            margin: 0 0 10px 0;
            display: -webkit-box;
            -webkit-line-clamp: 5;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        .hint {{
            font-size: 11px;
            color: #4CAF50;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        /* Toast Notification */
        .toast {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4CAF50;
            color: white;
            padding: 12px 24px;
            border-radius: 50px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            font-size: 14px;
            font-weight: 600;
            transform: translateX(200%);
            transition: transform 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            display: flex;
            align-items: center;
            gap: 8px;
            z-index: 1000;
        }}
        .toast.show {{
            transform: translateX(0);
        }}
    </style>
    </head>
    <body>
        
        <div id="notification" class="toast">
            <span>✅ Copied to clipboard!</span>
        </div>

        <div class="grid">
            {cards_html}
        </div>

        <script>
            function copyToClipboard(text) {{
                navigator.clipboard.writeText(text).then(function() {{
                    showToast();
                }}, function(err) {{
                    console.error('Async: Could not copy text: ', err);
                }});
            }}

            function showToast() {{
                const toast = document.getElementById('notification');
                toast.classList.add('show');
                setTimeout(() => {{
                    toast.classList.remove('show');
                }}, 2000);
            }}
        </script>
    </body>
    </html>
    """
    
    # Calculate height based on rows (approx 200px per row + gap)
    rows = (len(results) + columns - 1) // columns
    height = rows * 220 + 20 
    
    components.html(component_code, height=height)
