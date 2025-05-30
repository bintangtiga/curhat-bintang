from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Inisialisasi database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS curhat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kategori TEXT NOT NULL,
            isi TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/curhat', methods=['POST'])
def tambah_curhat():
    data = request.get_json()
    kategori = data.get('kategori')
    isi = data.get('isi')

    if not kategori or not isi:
        return jsonify({'error': 'Data tidak lengkap'}), 400

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO curhat (kategori, isi) VALUES (?, ?)', (kategori, isi))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Curhat berhasil disimpan'}), 201

@app.route('/curhat', methods=['GET'])
def get_curhat():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT kategori, isi, created_at FROM curhat ORDER BY id DESC')
    data = c.fetchall()
    conn.close()

    hasil = [{'kategori': k, 'isi': i, 'waktu': t} for (k, i, t) in data]
    return jsonify(hasil)

if __name__ == '__main__':
    app.run(debug=True)