from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
# Database initialization
def init_db():
    conn = sqlite3.connect('info_in.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS competitions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jenis_lomba TEXT NOT NULL,
        instansi_pembuat TEXT NOT NULL,
        tahap TEXT NOT NULL,
        tanggal DATE NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

@app.route('/save_competition_data', methods=['POST'])
def save_competition_data():
    data = request.json
    jenis_lomba = data['jenisLomba']
    instansi_pembuat = data['instansiPembuat']
    tahap = data['tahap']
    tanggal = data['tanggal']

    conn = sqlite3.connect('info_in.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO competitions (jenis_lomba, instansi_pembuat, tahap, tanggal)
    VALUES (?, ?, ?, ?)
    ''', (jenis_lomba, instansi_pembuat, tahap, tanggal))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 200

@app.route('/get_competition_stats', methods=['GET'])
def get_competition_stats():
    conn = sqlite3.connect('info_in.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT strftime('%Y', tanggal) as year, jenis_lomba, COUNT(*) as count
    FROM competitions
    GROUP BY year, jenis_lomba
    ''')
    rows = cursor.fetchall()
    conn.close()

    stats = {}
    for row in rows:
        year, jenis_lomba, count = row
        if year not in stats:
            stats[year] = {"Lomba Desain Produk": 0, "Lomba Bussines Plan Competition": 0, "Lomba Essay": 0, "Lomba LKTI":0, "Lomba Publish Paper":0}
        stats[year][jenis_lomba] = count

    years = sorted(stats.keys())
    data = {
        "years": years,
        "lomba Desain Produk": [stats[year]["Lomba Desain Produk"] for year in years],
        "lomba Bussines Plan Competition": [stats[year]["Lomba Bussines Plan Competition"] for year in years],
        "lomba Essay": [stats[year]["Lomba Essay"] for year in years],
        "lomba LKTI": [stats[year]["lomba LKTI"] for year in years],
        "lomba Publish Paper": [stats[year]["lomba Publish Paper"] for year in years]
    }
    return jsonify(data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
