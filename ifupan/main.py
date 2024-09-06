import asyncio

from flask import Flask, render_template

from app.routes.common_routes import common_bp
from app.routes.mind_map_routes import mind_map_bp
from app.routes.speech_to_text_routes import speech_to_text_bp
from app.routes.text_analysis_routes import text_analysis_bp

app = Flask(__name__, template_folder='app/views/templates')

# Register blueprints
app.register_blueprint(text_analysis_bp, url_prefix='/api/text-analysis')
app.register_blueprint(mind_map_bp, url_prefix='/api/mind-map')
app.register_blueprint(speech_to_text_bp, url_prefix='/api/speech-to-text')
app.register_blueprint(common_bp, url_prefix='/api/common')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    from hypercorn.asyncio import serve
    from hypercorn.config import Config
    config = Config()
    config.bind = ["localhost:5001"]
    asyncio.run(serve(app, config))
