from db import SessionLocal, User

# Session aç
db = SessionLocal()

# Yeni kullanıcı ekle
new_user = User(name="Aytac")
db.add(new_user)
db.commit()
db.refresh(new_user)

print("Eklenen kullanıcı:", new_user.id, new_user.name)

# Tüm kullanıcıları çek
users = db.query(User).all()
print("Tüm kullanıcılar:", users)

db.close()
