# Import library yang dibutuhkan
from flask import Flask, request, jsonify
from pymongo import MongoClient
import threading
import time
import random

# Inisialisasi Flask
app = Flask(__name__)

# Koneksi ke MongoDB Atlas
client = MongoClient("mongodb+srv://neng_ega:ega123@clstr1.uvizl.mongodb.net/?retryWrites=true&w=majority&appName=clstr1")
db = client.iot_sensor  # Nama database
collection = db.data123  # Nama koleksi

# Fungsi untuk menghasilkan data dummy sensor
def generate_dummy_data():
    sensor_data = {
        "sensor_gas": random.uniform(0.1, 5.0),  # Nilai random untuk gas
        "temperature": random.uniform(20.0, 30.0),  # Nilai random untuk suhu
        "humidity": random.uniform(30.0, 70.0),  # Nilai random untuk kelembaban
        "timestamp": time.time()  # Timestamp sekarang
    }
    return sensor_data

# Fungsi untuk menyimpan data ke database setiap 5 detik
def store_sensor_data():
    while True:
        data = generate_dummy_data()
        collection.insert_one(data)
        print(f"Data inserted: {data}")
        time.sleep(5)  # Interval 5 detik

# Endpoint untuk mendapatkan data dari database
@app.route('/get_data', methods=['GET'])
def get_data():
    limit = int(request.args.get('limit', 10))  # Jumlah data untuk ditampilkan
    data = list(collection.find().sort("timestamp", -1).limit(limit))
    for record in data:
        record["_id"] = str(record["_id"])  # Ubah ObjectId menjadi string
    return jsonify(data)

# Endpoint untuk menambahkan data dummy secara manual
@app.route('/add_dummy', methods=['POST'])
def add_dummy():
    data = generate_dummy_data()
    collection.insert_one(data)
    return jsonify({"message": "Data inserted", "data": data})

if __name__ == "__main__":
    # Menjalankan thread untuk menyimpan data secara otomatis
    data_thread = threading.Thread(target=store_sensor_data)
    data_thread.daemon = True
    data_thread.start()

    # Jalankan server Flask
    app.run(debug=True, host="0.0.0.0", port=5000)
