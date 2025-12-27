import sys
from pymongo import MongoClient
import g4f  # Ücretsiz AI motoru
import certifi

# MongoDB Bilgilerin
MONGO_URI = "mongodb+srv://aytaccamurlu26_db_user:3HwWLyyOSY1Stvaj@cluster0.vg96nxd.mongodb.net/?appName=Cluster0"

def main():
    try:
        # MongoDB Bağlantısı (SSL hatasını çözen certifi ile)
        ca = certifi.where()
        mongo_client = MongoClient(MONGO_URI, tlsCAFile=ca, tlsAllowInvalidCertificates=True)
        
        db = mongo_client["ucretsiz_ai_veritabani"]
        collection = db["mesajlar"]
        
        # Bağlantı Testi
        mongo_client.admin.command('ping')
        print("✅ MongoDB Bağlantısı Başarılı!")
        print("🤖 ÜCRETSİZ AI AKTİF! Soru sorabilirsiniz (Çıkmak için 'exit' yazın).")

        while True:
            user_input = input("\nSiz: ")
            if user_input.lower() == 'exit':
                print("Görüşürüz!")
                break

            print("⏳ Yapay zeka cevap veriyor...")

            try:
                # Model ismini gpt-3.5-turbo yerine "default" yaptık
                # Böylece o an çalışan en iyi ücretsiz modeli kendi seçer
                response = g4f.ChatCompletion.create(
                    model=g4f.models.default, 
                    messages=[{"role": "user", "content": user_input}],
                )
                
                # Bazen cevap çok uzun veya liste şeklinde gelebilir, temizliyoruz
                if isinstance(response, str):
                    ai_cevap = response
                else:
                    ai_cevap = str(response)

                print(f"\nAI: {ai_cevap}")

                # Veritabanına Kaydet
                collection.insert_one({
                    "kullanici": user_input,
                    "yapay_zeka": ai_cevap,
                    "yontem": "Ucretsiz_G4F_Otomatik"
                })
                print("💾 Konuşma MongoDB'ye kaydedildi.")

            except Exception as ai_hata:
                print(f"🔴 AI Cevap Hatası: {ai_hata}")

    except Exception as e:
        print(f"🔴 BAĞLANTI HATASI: {e}")

if __name__ == "__main__":
    main()