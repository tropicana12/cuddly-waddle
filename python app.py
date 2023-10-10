pip install Flask Flask-SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sequences.db'  # Naziv baze podataka
db = SQLAlchemy(app)

class Sequence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    sequence_data = db.Column(db.Text, nullable=False)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
python app.py

<!DOCTYPE html>
<html>
<head>
    <title>Portal za analizu sekvenci</title>
</head>
<body>
    <h1>Dobrodošli na Portal za analizu sekvenci</h1>
    <form method="POST" action="/search">
        <div class="form-group">
            <label for="search_term">Unesite ime sekvence:</label>
            <input type="text" class="form-control" id="search_term" name="search_term" placeholder="Ime sekvence">
        </div>
        <button type="submit" class="btn btn-primary">Pretraži</button>
    </form>
</body>
</html>
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sequences.db'  # Putanja do baze podataka
db = SQLAlchemy(app)

class Sequence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    sequence_data = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search_term')
    sequences = Sequence.query.filter(Sequence.name.contains(search_term)).all()
    return render_template('results.html', sequences=sequences, search_term=search_term)

if __name__ == '__main__':
    app.run(debug=True)
<!DOCTYPE html>
<html>
<head>
    <title>Rezultati pretrage za "{{ search_term }}"</title>
</head>
<body>
    <h1>Rezultati pretrage za "{{ search_term }}"</h1>
    
    {% if sequences %}
        <ul>
            {% for sequence in sequences %}
                <li>
                    <h3>{{ sequence.name }}</h3>
                    <p>{{ sequence.sequence_data }}</p>
                </li>
            {% endfor %}
        </ul>
    {% else %}
        <p>Nema rezultata za "{{ search_term }}"</p>
    {% endif %}
</body>
</html>
@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        # Dohvati izabrane sekvence iz forme
        sequence1_id = int(request.form.get('sequence1'))
        sequence2_id = int(request.form.get('sequence2'))
        
        # Dohvati sekvence iz baze podataka
        sequence1 = Sequence.query.get(sequence1_id)
        sequence2 = Sequence.query.get(sequence2_id)
        
        # Izračunaj postotak sličnosti (primer: ovde koristimo jednostavan primer)
        similarity_percentage = calculate_similarity(sequence1.sequence_data, sequence2.sequence_data)
        
        return render_template('analysis_result.html', sequence1=sequence1, sequence2=sequence2, similarity_percentage=similarity_percentage)
    
    # Učitaj sve sekvence iz baze podataka za izbor u formi
    sequences = Sequence.query.all()
    return render_template('analysis.html', sequences=sequences)
<form method="POST" action="/analyze">
    <div class="form-group">
        <label for="sequence1">Izaberite prvu sekvencu:</label>
        <select class="form-control" id="sequence1" name="sequence1">
            {% for sequence in sequences %}
            <option value="{{ sequence.id }}">{{ sequence.name }}</option>
            {% endfor %}
        </select>
    </div>
    <div class="form-group">
        <label for="sequence2">Izaberite drugu sekvencu:</label>
        <select class="form-control" id="sequence2" name="sequence2">
            {% for sequence in sequences %}
            <option value="{{ sequence.id }}">{{ sequence.name }}</option>
            {% endfor %}
        </select>
    </div>
    <button type="submit" class="btn btn-primary">Analiziraj</button>
</form>
<!DOCTYPE html>
<html>
<head>
    <title>Rezultati analize</title>
</head>
<body>
    <h1>Rezultati analize</h1>
    <p>Postotak sličnosti između sekvenci:</p>
    <p>{{ similarity_percentage }}%</p>
    <p>Prva sekvenca:</p>
    <p>{{ sequence1.name }}</p>
    <p>{{ sequence1.sequence_data }}</p>
    <p>Druga sekvenca:</p>
    <p>{{ sequence2.name }}</p>
    <p>{{ sequence2.sequence_data }}</p>
</body>
</html>
def count_characters(sequence):
    character_counts = {}
    for character in sequence:
        if character in character_counts:
            character_counts[character] += 1
        else:
            character_counts[character] = 1
    return character_counts
@app.route('/count', methods=['GET', 'POST'])
def count():
    if request.method == 'POST':
        sequence = request.form.get('sequence')
        character_counts = count_characters(sequence)
        return render_template('character_count_result.html', character_counts=character_counts, sequence=sequence)
    return render_template('character_count.html')
<!DOCTYPE html>
<html>
<head>
    <title>Brojanje karaktera</title>
</head>
<body>
    <h1>Unesite sekvencu za brojanje karaktera:</h1>
    <form method="POST" action="/count">
        <div class="form-group">
            <label for="sequence">Sekvenca:</label>
            <input type="text" class="form-control" id="sequence" name="sequence" placeholder="Unesite sekvencu">
        </div>
        <button type="submit" class="btn btn-primary">Broj karaktera</button>
    </form>
</body>
</html>
def calculate_similarity(sequence1, sequence2):
    # Ovde se može implementirati svoj algoritam za izračunavanje sličnosti
    # Na primer, može se koristiti algoritam za poređenje sekvenci kao što je Needleman-Wunsch ili Smith-Waterman.

    # Jednostavan primer: Brojanje istih karaktera na istim pozicijama
    if len(sequence1) != len(sequence2):
        return 0  # Sekvence moraju biti iste dužine za ovaj primer

    similarity_count = 0
    total_length = len(sequence1)

    for i in range(total_length):
        if sequence1[i] == sequence2[i]:
            similarity_count += 1

    similarity_percentage = (similarity_count / total_length) * 100
    return similarity_percentage

# Onda idu definicije ruta za analizu sekvenci ispod ovog dela.

<!DOCTYPE html>
<html>
<head>
    <title>Rezultati brojanja karaktera</title>
</head>
<body>
    <h1>Rezultati brojanja karaktera za sekvencu:</h1>
    <p>{{ sequence }}</p>
    <table class="table table-bordered">
        <thead>
            <tr>
                <th>Karakter</th>
                <th>Broj</th>
            </tr>
        </thead>
        <tbody>
            {% for character, count in character_counts.items() %}
            <tr>
                <td>{{ character }}</td>
                <td>{{ count }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>

