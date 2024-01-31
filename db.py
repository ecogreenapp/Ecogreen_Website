from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), index=True ,unique=True)
    email = db.Column(db.String(100), index=True ,unique=True)
    password = db.Column(db.String(50), index=True ,unique=True)
    role = db.Column(db.String(50), index=True ,default='user')
    date = db.Column(db.DateTime, default=datetime.utcnow)  # Kolom untuk menyimpan tanggal registrasi
    foto_profil = db.Column(db.String(255))
  
class Sampah(db.Model):
    __tablename__ = "sampah"
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(11))
    nama = db.Column(db.String(50))
    jenis = db.Column(db.String(50))
    satuan = db.Column(db.String(20))
    harga = db.Column(db.Float)
    
class Banksampah(db.Model):
    __tablename__ = "banksampah"
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50))
    alamat = db.Column(db.String(250))
    pj = db.Column(db.String(50))
    no_hp = db.Column(db.String(15))
    
class TPS(db.Model):
    __tablename__ = "tps"
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    alamat = db.Column(db.String(200))
    kabupaten_kota = db.Column(db.String(50))
    kecamatan = db.Column(db.String(50))
    desa = db.Column(db.String(50))
    
class Input_Review(db.Model):
    __tablename__ = "input_review"
    id_review = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(255), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    review = db.Column(db.Text, nullable=False)
    
def insert_data_to_mysql(data):
    try:
        # Modify the SQL statement to include id_review as auto-increment
        db.create_all()  # Ini akan membuat tabel jika belum ada
        new_review = Input_Review(nama=data['nama'], tanggal=data['tanggal'], review=data['review'])
        db.session.add(new_review)
        db.session.commit()
        print("Data inserted successfully!")
    except Exception as e:
        print(f"Error: {e}")
        
class HistoryDeteksi(db.Model):
    __tablename__ = "history_deteksi"
    id = db.Column(db.Integer, primary_key=True)
    tanggal_deteksi = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    file_path = db.Column(db.String(255))
    hasil_deteksi = db.Column(db.String(50))
    
    user = db.relationship('Users', backref='history_deteksi')

class Artikel(db.Model):
    __tablename__ = "artikel"
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(255))
    gambar = db.Column(db.String(255))
    isi_artikel = db.Column(db.String(225))
    kategori = db.Column(db.String(100))
    tanggal = db.Column(db.DateTime, default=datetime.utcnow)


class Produk(db.Model):
    __tablename__ = "produk"
    id = db.Column(db.Integer, primary_key=True)
    nama_produk = db.Column(db.String(200))
    gambar_produk = db.Column(db.String(100))
    link_video = db.Column(db.String(100))

class Hasil_model(db.Model):
    __tablename__ = "hasil_model"
    id_hasil_model = db.Column(db.Integer, primary_key=True)
    id_review = db.Column(db.Integer)
    nama = db.Column(db.String(255))
    tanggal = db.Column(db.DateTime)
    review = db.Column(db.String(255))
    label = db.Column(db.Integer)
    



    