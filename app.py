from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "database.db"

def get_db():
    return sqlite3.connect(DB_NAME)

# Buat tabel otomatis
with get_db() as conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS mahasiswa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nim TEXT,
        nama TEXT,
        jurusan TEXT,
        angkatan INTEGER
    )
    """)

@app.route("/")
def home():
    return jsonify({"message": "API Mahasiswa Berjalan"})

@app.route("/mahasiswa", methods=["POST"])
def tambah_mahasiswa():
    data = request.json
    with get_db() as conn:
        conn.execute(
            "INSERT INTO mahasiswa (nim, nama, jurusan, angkatan) VALUES (?, ?, ?, ?)",
            (data["nim"], data["nama"], data["jurusan"], data["angkatan"])
        )
    return jsonify({"message": "Data mahasiswa berhasil ditambahkan"})

@app.route("/mahasiswa", methods=["GET"])
def get_mahasiswa():
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM mahasiswa")
        data = [
            {
                "id": row[0],
                "nim": row[1],
                "nama": row[2],
                "jurusan": row[3],
                "angkatan": row[4]
            }
            for row in cursor.fetchall()
        ]
    return jsonify(data)

@app.route("/mahasiswa/<int:id>", methods=["GET"])
def get_mahasiswa_by_id(id):
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM mahasiswa WHERE id=?", (id,))
        row = cursor.fetchone()
    if row:
        return jsonify({
            "id": row[0],
            "nim": row[1],
            "nama": row[2],
            "jurusan": row[3],
            "angkatan": row[4]
        })
    return jsonify({"message": "Data tidak ditemukan"}), 404

@app.route("/mahasiswa/<int:id>", methods=["PUT"])
def update_mahasiswa(id):
    data = request.json
    with get_db() as conn:
        conn.execute(
            "UPDATE mahasiswa SET nama=?, jurusan=? WHERE id=?",
            (data["nama"], data["jurusan"], id)
        )
    return jsonify({"message": "Data berhasil diupdate"})

@app.route("/mahasiswa/<int:id>", methods=["DELETE"])
def delete_mahasiswa(id):
    with get_db() as conn:
        conn.execute("DELETE FROM mahasiswa WHERE id=?", (id,))
    return jsonify({"message": "Data berhasil dihapus"})

if __name__ == "__main__":
    app.run(debug=True)
@app.route("/mahasiswa/<int:id>", methods=["PUT"])
def update_mahasiswa(id):
    data = request.json

    with get_db() as conn:
        conn.execute(
            "UPDATE mahasiswa SET nama=?, jurusan=?, angkatan=? WHERE id=?",
            (data["nama"], data["jurusan"], data["angkatan"], id)
        )

    return jsonify({"message": "Data berhasil diedit"})
