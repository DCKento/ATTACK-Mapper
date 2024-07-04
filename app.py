from flask import Flask, render_template, request, jsonify, send_file
import json
import csv
import io
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Load MITRE ATT&CK framework data
with open('attack_framework.json', 'r') as f:
    attack_data = json.load(f)

# In-memory storage for user data (replace with database in production)
user_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/framework', methods=['GET'])
def get_framework():
    return jsonify(attack_data)

@app.route('/api/update_technique', methods=['POST'])
def update_technique():
    data = request.json
    technique_id = data['id']
    control = data['control']
    color = data['color']
    
    user_data[technique_id] = {'control': control, 'color': color}
    
    return jsonify({"status": "success"})

@app.route('/api/upload_screenshot', methods=['POST'])
def upload_screenshot():
    if 'screenshot' not in request.files:
        return jsonify({"status": "error", "message": "No file part"})
    
    file = request.files['screenshot']
    technique_id = request.form['id']
    
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"})
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{technique_id}_{filename}")
        file.save(filepath)
        user_data[technique_id]['screenshot'] = filepath
        return jsonify({"status": "success", "url": filepath})

@app.route('/api/export', methods=['GET'])
def export_data():
    export_data = {
        "framework": attack_data,
        "user_data": user_data
    }
    return jsonify(export_data)

@app.route('/api/export_csv', methods=['GET'])
def export_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Tactic', 'Technique', 'Subtechnique', 'Control', 'Effectiveness'])
    
    for tactic in attack_data['tactics']:
        for technique in tactic['techniques']:
            tech_data = user_data.get(technique['id'], {})
            writer.writerow([
                tactic['name'],
                technique['name'],
                '',
                tech_data.get('control', ''),
                tech_data.get('color', '')
            ])
            
            for subtechnique in technique['subtechniques']:
                subtech_data = user_data.get(subtechnique['id'], {})
                writer.writerow([
                    tactic['name'],
                    technique['name'],
                    subtechnique['name'],
                    subtech_data.get('control', ''),
                    subtech_data.get('color', '')
                ])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        attachment_filename='attack_mapper_export.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)