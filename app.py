from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = 'data/subjects_symbols.json'

def read_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({"subjects": [], "symbols": []}, f)
    with open(DATA_FILE) as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/view', methods=['GET', 'POST'])
def view_option():
    data = read_data()
    subjects = [s['name'] for s in data['subjects']]
    symbols = [s['name'] for s in data['symbols']]
    results = []  # Initialize results to an empty list

    if request.method == 'POST':
        selected_option = request.form.get('view_input')
        selected_category = request.form.get('view_category')

        if selected_category == 'subject':
            results = [s for s in data['subjects'] if s['name'] == selected_option]
        elif selected_category == 'symbol':
            results = [s for s in data['symbols'] if s['name'] == selected_option]

    return render_template('view_option.html', subjects=subjects, symbols=symbols, results=results)



@app.route('/add/subject', methods=['GET', 'POST'])
def add_subject():
    data = read_data()
    if request.method == 'POST':
        subject_type = request.form.get('subject_type')
        subject = {
            "type": subject_type,
            "name": request.form.get('new_subject') if subject_type == 'new' else request.form.get('existing_subject'),
            "surah_name": request.form.get('surah_name'),
            "from_verse": request.form.get('from_verse'),
            "to_verse": request.form.get('to_verse')
        }
        data['subjects'].append(subject)
        write_data(data)
        return "Subject added successfully!"
    return render_template('add_subject.html', existing_subjects=[s['name'] for s in data['subjects']])

@app.route('/add/symbol', methods=['GET', 'POST'])
def add_symbol():
    data = read_data()
    if request.method == 'POST':
        symbol_type = request.form.get('symbol_type')
        symbol = {
            "type": symbol_type,
            "name": request.form.get('new_symbol') if symbol_type == 'new' else request.form.get('existing_symbol') if symbol_type == 'existing' else request.form.get('search_symbol'),
            "surah_name": request.form.get('surah_name'),
            "from_verse": request.form.get('from_verse'),
            "to_verse": request.form.get('to_verse')
        }
        data['symbols'].append(symbol)
        write_data(data)
        return "Symbol added successfully!"
    return render_template('add_symbol.html', existing_symbols=[s['name'] for s in data['symbols']])

@app.route('/api/search', methods=['POST'])
def api_search():
    query = request.json.get('query')
    data = read_data()
    results = [s['name'] for s in data['symbols'] if query.lower() in s['name'].lower()]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
