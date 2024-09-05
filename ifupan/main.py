from flask import Flask, render_template, request, jsonify, send_file
import os
import text_analysis
import mind_map_generator
import speech_to_text

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    prompt_type = data.get('promptType', 'diary')  # Default to diary if not specified
    result = text_analysis.analyze(text, prompt_type)
    return jsonify({'result': result})

@app.route('/generate_mind_map', methods=['POST'])
def generate_mind_map():
    data = request.json
    text = data.get('text', '')
    prompt_type = data.get('promptType', 'diary')
    mind_map, pdf = mind_map_generator.generate(text, prompt_type)
    return jsonify({
        'mind_map': os.path.basename(mind_map),
        'pdf': os.path.basename(pdf)
    })

@app.route('/speech_to_text', methods=['POST'])
def speech_to_text_route():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    prompt_type = request.form.get('promptType', 'diary')
    text = speech_to_text.transcribe(audio_file)
    result = text_analysis.analyze(text, prompt_type)
    return jsonify({'result': result})

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join('files', filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
