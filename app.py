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
    if request.method == 'POST':
        category = request.form['view_category']
        selected_option = request.form['view_input']
        print("here3", category,selected_option)
        results = []
        if category == 'target_meaning' and selected_option in data['target_meaning']:
            results = data['target_meaning'][selected_option]
        elif category == 'common_words' and selected_option in data['common_words']:
            results = data['common_words'][selected_option]

        return render_template('view_option.html', results=results, target_meaning=list(data['target_meaning'].keys()), common_words=list(data['common_words'].keys()))
    l = list(data['target_meaning'].keys())
    l2 = list(data['common_words'].keys())
    print("here2", l , l2, type(l), type(l2), l[0], type(l[0]))
    return render_template('view_option.html', target_meaning=list(data['target_meaning'].keys()), common_words=list(data['common_words'].keys()))

@app.route('/add', methods=['GET'])
def add_option():
    return render_template('add_options.html')

@app.route('/add/subject', methods=['GET', 'POST'])
def add_subject():
    data = read_data()
    if request.method == 'POST':
        meaning_type = request.form['subject_type']
        surah_name = request.form['surah_name']
        from_verse = request.form['from_verse']
        to_verse = request.form['to_verse']

        if meaning_type == 'new':
            new_meaning = request.form['new_subject']
            data['target_meaning'][new_meaning] = [{
                'surah_name': surah_name,
                'from_verse': from_verse,
                'to_verse': to_verse
            }]
        elif meaning_type == 'existing':
            existing_meaning = request.form['existing_subject']
            if existing_meaning in data['target_meaning']:
                data['target_meaning'][existing_meaning].append({
                    'surah_name': surah_name,
                    'from_verse': from_verse,
                    'to_verse': to_verse
                })

        write_data(data)
        return "Subject added successfully!"

    existing_meanings = list(data['target_meaning'].keys())
    return render_template('add_target_meaning.html', existing_subjects=existing_meanings)

@app.route('/add/symbol', methods=['GET', 'POST'])
def add_symbol():
    data = read_data()
    if request.method == 'POST':
        word_type = request.form['symbol_type']
        surah_name = request.form['surah_name']
        from_verse = request.form['from_verse']
        to_verse = request.form['to_verse']

        if word_type == 'new':
            new_word = request.form['new_symbol']
            data['common_words'][new_word] = [{
                'surah_name': surah_name,
                'from_verse': from_verse,
                'to_verse': to_verse
            }]
        elif word_type == 'existing':
            existing_word = request.form['existing_symbol']
            if existing_word in data['common_words']:
                data['common_words'][existing_word].append({
                    'surah_name': surah_name,
                    'from_verse': from_verse,
                    'to_verse': to_verse
                })
        write_data(data)
        return "Symbol added successfully!"
    existing_word = list(data['common_words'].keys())
    return render_template('add_symbol.html', existing_symbols=existing_word)

@app.route('/api/search', methods=['POST'])
def api_search():
    query = request.json.get('query')
    data = read_data()
    results = [s['name'] for s in data['symbols'] if query.lower() in s['name'].lower()]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
