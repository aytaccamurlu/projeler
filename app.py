# from flask import Flask, request, jsonify, make_response
# from flask_cors import CORS
# import g4f

# app = Flask(__name__)
# # Tüm kaynaklara ve tüm metodlara izin ver
# CORS(app, resources={r"/*": {"origins": "*"}})

# @app.route('/chat', methods=['POST', 'OPTIONS'])
# def chat():
#     # CORS Ön Kontrolü (Browser önce bunu sorar)
#     if request.method == "OPTIONS":
#         response = make_response()
#         response.headers.add("Access-Control-Allow-Origin", "*")
#         response.headers.add("Access-Control-Allow-Headers", "*")
#         response.headers.add("Access-Control-Allow-Methods", "*")
#         return response

#     try:
#         data = request.json
#         user_message = data.get("message")
        
#         # AI Yanıtı
#         response_ai = g4f.ChatCompletion.create(
#             model=g4f.models.default,
#             messages=[{"role": "user", "content": user_message}],
#         )
        
#         res = jsonify({"reply": str(response_ai)})
#         # Yanıta manuel başlık ekle (Güvenlik duvarını aşmak için)
#         res.headers.add("Access-Control-Allow-Origin", "*")
#         return res
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)
from flask import make_response
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import certifi

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

# MongoDB Bağlantısı
MONGO_URI = "mongodb+srv://aytaccamurlu26_db_user:3HwWLyyOSY1Stvaj@cluster0.vg96nxd.mongodb.net/?appName=Cluster0"
ca = certifi.where()
client = MongoClient(MONGO_URI, tlsCAFile=ca)
db = client["crm_sistemi"]
customers_col = db["musteriler"]

# Tüm Müşterileri Listele
@app.route('/customers', methods=['GET'])
def get_customers():
    try:
        customers = []
        for doc in customers_col.find():
            customers.append({
                "id": str(doc["_id"]),
                "name": doc.get("name", ""),
                "email": doc.get("email", ""),
                "phone": doc.get("phone", ""),
                "status": doc.get("status", "Potansiyel")
            })
        
        # Yanıtı manuel olarak oluşturup CORS başlıklarını zorla ekliyoruz
        response = make_response(jsonify(customers))
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Yeni Müşteri Ekle
@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    # Beklenen veri: { "name": "...", "email": "...", "phone": "...", "status": "..." }
    result = customers_col.insert_one(data)
    return jsonify({"message": "Müşteri başarıyla eklendi", "id": str(result.inserted_id)})

# Müşteri Sil
@app.route('/customers/<id>', methods=['DELETE'])
def delete_customer(id):
    customers_col.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Müşteri silindi"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)