import os
import json
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load the ATT&CK framework JSON data
with open('attack_framework.json') as f:
    attack_framework = json.load(f)

@app.route('/api/framework', methods=['GET'])
def get_framework():
    return jsonify(attack_framework)

@app.route('/api/update_technique', methods=['POST'])
def update_technique():
    data = request.json
    # Find the technique by id and update its control and color
    for tactic in attack_framework['tactics']:
        for technique in tactic['techniques']:
            if technique['id'] == data['id']:
                technique['control'] = data.get('control')
                technique['color'] = data.get('color')
                return jsonify({'status': 'success'})
            for subtech in technique.get('subtechniques', []):
                if subtech['id'] == data['id']:
                    subtech['control'] = data.get('control')
                    subtech['color'] = data.get('color')
                    return jsonify({'status': 'success'})
    return jsonify({'status': 'failure'})

@app.route('/api/upload_screenshot', methods=['POST'])
def upload_screenshot():
    file = request.files['screenshot']
    id = request.form['id']
    filename = f'{id}_{file.filename}'
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    url = f'/uploads/{filename}'
    # Update the framework with the screenshot URL (if needed)
    return jsonify({'status': 'success', 'url': url})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/export', methods=['GET'])
def export_json():
    return jsonify(attack_framework)

@app.route('/api/export_csv', methods=['GET'])
def export_csv():
    import csv
    from io import StringIO
    si = StringIO()
    cw = csv.writer(si)
    
    # Write CSV header
    cw.writerow(["Tactic", "Technique", "Subtechnique", "Control", "Color"])

    # Write CSV rows
    for tactic in attack_framework['tactics']:
        for technique in tactic['techniques']:
            cw.writerow([tactic['name'], technique['name'], "", technique.get('control', ""), technique.get('color', "")])
            for subtech in technique.get('subtechniques', []):
                cw.writerow([tactic['name'], technique['name'], subtech['name'], subtech.get('control', ""), subtech.get('color', "")])
    
    output = si.getvalue()
    return app.response_class(output, mimetype="text/csv")

if __name__ == '__main__':
    app.run(debug=True)
