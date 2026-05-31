from flask import render_template, request, render_template_string
import markdown
import os

def register_routes(app):
    @app.route('/')
    def index():
        # Get dynamic info
        host = request.host
        
        # Check X-Forwarded-Proto header for the original protocol from the gateway
        proto = request.headers.get('X-Forwarded-Proto', request.scheme)
        protocol = 'wss' if proto == 'https' else 'ws'
        
        # Read README.md from the root directory
        root_path = os.path.dirname(app.root_path)
        readme_path = os.path.join(root_path, 'README.md')
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
            
        # 1. First render the markdown string as a Jinja2 template to resolve {{ host }} etc.
        resolved_md = render_template_string(md_content, host=host, protocol=protocol)
        
        # 2. Convert the resolved markdown to HTML
        html_content = markdown.markdown(resolved_md, extensions=['fenced_code', 'tables'])
        
        return render_template('index.html', content=html_content)
