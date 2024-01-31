import re
from PIL import Image
from flask import Flask, render_template, request, send_from_directory, session, url_for, redirect, jsonify, flash
from db import db, Users, Sampah, Banksampah, TPS, insert_data_to_mysql, Input_Review, HistoryDeteksi, Artikel, Produk, Hasil_model
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from chatbot import chatbot_response, predict_class, getResponse
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from functools import wraps
from keras.models import load_model
import os
import pickle
import json
import numpy as np
from werkzeug.utils import secure_filename
from classifier import model_predict
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mwd2023'
# ... (Konfigurasi database dan definisi rute)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/ecogreendb'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
# Initialize the Flask-JWT-Extended extension
jwt = JWTManager(app)

@app.route('/')
def index():
    tps = TPS.query.all()
    data_artikel = Artikel.query.all()
    return render_template('index.html',tps=tps,data_artikel=data_artikel,page='home')

@app.route('/register', methods =['GET','POST'])
def register():
    if request.method == 'POST':
        # Logika pendaftaran untuk metode POST
        nama = request.form.get('nama')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_exists = Users.query.filter_by(email=email).first() is not None

        if user_exists:
            return jsonify({'message': 'Email sudah terdaftar!'})
        elif not nama or not password or not email:
            return jsonify({'message': 'Isi formulir dengan benar!'})
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return jsonify({'message': 'Alamat email tidak valid!'})
        elif len(password) < 8:
            return jsonify({'message': 'Password harus memiliki setidaknya 8 karakter.'})

        # Menggunakan generate_password_hash untuk menghash password sebelum disimpan
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = Users(nama=nama, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

            # Buat respons sukses
        return jsonify({'message': 'Registrasi anda berhasil, silahkan login!'})

    # Logika pendaftaran untuk metode GET
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''  # Inisialisasi string kosong untuk menyimpan pesan

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        if email == '' or password == '':
            message = 'Masukkan email dan password'
        else:
            user = Users.query.filter_by(email=email).first()

            if user is None:
                message = 'Masukkan email dan password yang benar!'
            else:
                # Tetapkan variabel sesi setelah login berhasil
                session['loggedin'] = True
                session['userid'] = user.user_id
                session['foto_profil'] = user.foto_profil
                session['nama'] = user.nama
                session['email'] = user.email
                message = 'Login berhasil!'

                # Redirect berdasarkan peran pengguna
                if user.role == 'admin':
                    return redirect(url_for('dashboard'))
                else:
                    return redirect(url_for('index'))

    # Render template login dengan pesan
    return render_template('login.html', message=message)
@app.route('/loginmob', methods=['GET', 'POST'])
def loginmob():
    mesage = ''
    if request.method == 'POST' and 'email' in request.json and 'password' in request.json:
        email = request.json['email']
        password = request.json['password']

        if email == '' or password == '':
            mesage = 'Masukan email dan password'
        else:
            user = Users.query.filter_by(email=email).first()
            print(user)
            if user is None:
                mesage = 'false'
            else:
                session['loggedin'] = True
                session['userid'] = user.user_id
                session['nama'] = user.nama
                session['email'] = user.email
                session['token'] = create_access_token(identity=user.user_id)
                mesage = 'true'
    return jsonify({"success": mesage, "data": session})

#  route untuk mendapatkan respons dari bot
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')  
    # Ambil teks yang dikirim oleh pengguna melalui parameter 'msg'
    return chatbot_response(userText)  
# Panggil fungsi chatbot_response dengan teks pengguna sebagai argumen

#  route untuk halaman chatbot
@app.route('/chatbot')
def chatbot():
    waktu_sekarang = datetime.now().strftime("%H:%M")  
    # Dapatkan waktu saat ini dalam format jam:menit
    return render_template('chatbot.html', waktu=waktu_sekarang)  
# Render template chatbot.html dengan waktu sebagai konteks

# Fungsi dekorator untuk memastikan bahwa hanya admin yang dapat mengakses halaman tertentu
def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session or session['loggedin'] is False:
            return redirect(url_for('login'))
        user = Users.query.filter_by(user_id=session['userid']).first()
        if user is None or user.role != 'admin':
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Fungsi dekorator untuk memastikan bahwa hanya pengguna yang sudah login yang dapat mengakses halaman tertentu
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session or session['loggedin'] is False:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Tentukan route untuk deteksi gambar dengan metode GET dan POST
@app.route('/deteksi', methods=['GET', 'POST'])
@login_required  # Memastikan bahwa pengguna harus login untuk mengakses halaman ini
def deteksi():
    if request.method == 'POST':
        # Dapatkan file dari permintaan POST
        f = request.files['file']

        # Simpan file ke ./static/uploads/deteksi
        filename = secure_filename(f.filename)
        file_path = os.path.join('static', 'uploads', 'deteksi', filename)
        f.save(file_path)

        # Lakukan prediksi
        img = Image.open(file_path)
        img = img.resize((224, 224), Image.NEAREST)
        pred_label, pred_accuracy = model_predict(img)
        
        # Simpan path relatif hasil deteksi ke dalam database
        user_id = session['userid']  # Anggap pengguna sudah login
        relative_path = os.path.join('uploads', 'deteksi', filename)
        new_deteksi = HistoryDeteksi(user_id=user_id, file_path=relative_path, hasil_deteksi=pred_label)
        db.session.add(new_deteksi)
        db.session.commit()

        # Kembalikan hasil prediksi dan akurasi sebagai JSON
        return jsonify({'prediction': pred_label, 'accuracy': pred_accuracy})

    # Render template deteksi.html jika metodenya GET
    return render_template('deteksi.html', page='deteksi')
#Android Test Route
@app.route('/uploadFileAndroid', methods=['POST'])
def uploadFileAndroid():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'


    filename = secure_filename(file.filename)
    file_path = os.path.join('static', 'uploads', 'deteksi', filename)
    file.save(file_path)

    return 'File uploaded successfully'

@app.route('/receive_json', methods=['POST'])
def receive_json():
    try:
        data = request.get_json()
        received_text = data.get('text', '')
        uploads = 'static/android/images/'
        userid = request.json.get('userid')
        
        fileName = received_text
        path = os.path.join('static', 'uploads', 'deteksi', fileName)
        relative_path = os.path.join('uploads', 'deteksi', fileName)
        # Lakukan sesuatu dengan data JSON yang diterima di server Flask
        print('JSON yang diterima:', data)
        
        # facecropAndroid(path)
        # img = preprocess_img(path)
        # pred = predict_resultForAndroid(img)
        img = Image.open(path)
        img = img.resize((224, 224), Image.NEAREST)
        pred_label, pred_accuracy = model_predict(img)
        new_deteksi = HistoryDeteksi(user_id=userid, file_path=relative_path, hasil_deteksi=pred_label)
        db.session.add(new_deteksi)
        db.session.commit()
        return jsonify({"result": pred_label, "accuracy": pred_accuracy})
    except Exception as e:
        print(f'Error in receive_json: {e}')
        return jsonify({'message': 'Internal Server Error'}), 500

##list sampah mobile
@app.route('/sampahua', methods=['GET', 'POST'])
def sampahua():
    if request.method == 'GET':
        try:
            # Querying all data from the Sampah model
            data = Sampah.query.all()
            
            # Converting the SQLAlchemy objects to a list of dictionaries
            data = [{"id": row.id, "kode": row.kode, "nama": row.nama, "jenis": row.jenis, "satuan": row.satuan, "harga": row.harga} for row in data]

            # Returning the data as JSON
            return jsonify({"sampah": data})
        except Exception as e:
            return jsonify({"error": str(e)})
    
    elif request.method == 'POST':
        try:
            # Extracting data from the JSON request
            id = request.json['id']
            kode = request.json['kode']
            nama = request.json['nama']
            jenis = request.json['jenis']
            satuan = request.json['satuan']
            harga = request.json['harga']
            image = request.json['image']
            
            # Creating a new Sampah object
            new_sampah = Sampah(id=id, kode=kode, nama=nama, jenis=jenis, satuan=satuan, harga=harga, image=image)
            
            # Adding the new Sampah object to the database session
            db.session.add(new_sampah)
            
            # Committing the changes to the database
            db.session.commit()
            
            # Returning a success message
            return jsonify({'message': 'data berhasil ditambahkan'})
        except Exception as e:
            return jsonify({"error": str(e)})
        
@app.route('/historymob/<int:userid>', methods=['GET', 'POST'])
def historymob(userid):
    if request.method == 'GET':
        try:
            # Querying all data from the Sampah model
            data = HistoryDeteksi.query.filter_by(user_id=userid).order_by(HistoryDeteksi.tanggal_deteksi.desc()).all()
            
            # Converting the SQLAlchemy objects to a list of dictionaries
            data = [{"id": row.id, "hasil": row.hasil_deteksi, "tanggal": row.tanggal_deteksi} for row in data]

            # Returning the data as JSON
            return jsonify({"history_mobile": data})
        except Exception as e:
            return jsonify({"error": str(e)})
    
    elif request.method == 'POST':
        try:
            # Extracting data from the JSON request
            id = request.json['id']
            hasil = request.json['hasil']
            tanggal = request.json['tanggal']
            
            # Creating a new Sampah object
            new_historymob = Sampah(id=id, hasil=hasil, tanggal=tanggal)
            
            # Adding the new Sampah object to the database session
            db.session.add(new_historymob)
            
            # Committing the changes to the database
            db.session.commit()
            
            # Returning a success message
            return jsonify({'message': 'data berhasil ditambahkan'})
        except Exception as e:
            return jsonify({"error": str(e)})  



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Enable CORS for all routes
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

app.after_request(add_cors_headers)

# Rute untuk menangani halaman feedback dengan mengharuskan pengguna untuk login
@app.route('/feedback')
@login_required
def feedback():
    return render_template('feedback.html', page='feedback')

# Rute untuk menangani pengiriman formulir
@app.route('/submit', methods=['POST', 'OPTIONS'])
def submit_form():
    # Dapatkan data formulir dalam format JSON dari permintaan
    data_to_insert = request.get_json()

    # Panggil fungsi untuk memasukkan data ke MySQL
    insert_data_to_mysql(data_to_insert)

    # Kembalikan respons JSON yang menunjukkan keberhasilan
    return jsonify({'status': 'success'})

@app.route('/statistik')
def statistik():
    return render_template('statistik.html',page='statistik')

@app.route('/jenissampah')
def jenis():
    return render_template('jenis.html',page='jenis')

@app.route('/hargasampah')
def harga():
    data_sampah = Sampah.query.all()
    return render_template('harga.html',  data_sampah=data_sampah, page='harga')

@app.route('/produk')
def produk():
    produk = Produk.query.all()
    return render_template('produk.html',produk=produk,page='produk')

@app.route('/banksampah', methods=['GET', 'POST'])
def banksampah():
    if request.method == 'POST':
        search_term = request.form.get('q')
        banksampah = Banksampah.query.filter(
            (Banksampah.nama.ilike(f"%{search_term}%")) | (Banksampah.alamat.ilike(f"%{search_term}%"))
        ).all()
    else:
        banksampah = Banksampah.query.all()

    return render_template('banksampah.html', page='bank', banksampah=banksampah)

@app.route('/mawarbiru')
def mawarbiru():
    return render_template('mawarbiru.html')

@app.route('/artikel', methods=['GET', 'POST'])
def artikel():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Adjust the number of articles per page as needed

    if request.method == 'POST':
        search_term = request.form.get('q')
        artikel_pagination = Artikel.query.filter(
            (Artikel.judul.ilike(f"%{search_term}%")) | (Artikel.kategori.ilike(f"%{search_term}%"))
        ).paginate(page=page, per_page=per_page)
    else:
        artikel_pagination = Artikel.query.paginate(page=page, per_page=per_page)

    return render_template('artikel.html', page='artikel', artikel=artikel_pagination)

from flask import render_template

@app.route('/artikeldetails/<int:id>')
def artikeldetails(id):
    # Assuming you have a model named 'Artikel' for articles
    article = Artikel.query.get(id)

    if not article:
        flash('Artikel tidak ditemukan', 'danger')
        return redirect(url_for('artikel'))

    return render_template('artikel-detail.html', page='artikeldetails', article=article)


@app.route('/tps',methods=['GET', 'POST'])
def tps():
    if request.method == 'POST':
        search_term = request.form.get('a')
        tps = TPS.query.filter(
            (tps.nama.ilike(f"%{search_term}%")) | (TPS.alamat.ilike(f"%{search_term}%"))
        ).all()
    else:
        tps = TPS.query.all()
    return render_template('tps.html',page='tps',tps=tps)


from werkzeug.utils import secure_filename

@app.route('/settingprofile/<int:user_id>', methods=['GET', 'POST'])
def setting_profile(user_id):
    user = Users.query.get(user_id)

    if request.method == 'POST':
        # Update fields
        user.nama = request.form['nama']
        user.email = request.form['email']
        user.password = request.form['password']
        new_foto_profil = request.files['foto_profil']

        if not user.nama or not user.email or not user.password:
            flash('Mohon lengkapi semua kolom.', 'danger')
        else:
            # Check if a new profile picture is uploaded
            if new_foto_profil:
                # Delete the existing profile picture before saving the new one
                if user.foto_profil:
                    existing_path = os.path.join('static', user.foto_profil)
                    if os.path.exists(existing_path):
                        os.remove(existing_path)

                # Save the new profile picture
                filename = secure_filename(new_foto_profil.filename)
                profil_path = os.path.join('uploads', 'foto_profil', filename)
                new_foto_profil.save(os.path.join('static', profil_path))
                user.foto_profil = profil_path

            # Commit changes to the database
            db.session.commit()

            flash('Data user berhasil diperbarui', 'success')
            return redirect(url_for('setting_profile', user_id=user.user_id))

    # Check if user.foto_profil is not None before creating the path
    existing_profil_path = os.path.join('static', user.foto_profil) if user.foto_profil else None

    return render_template('profile.html', user=user, existing_profil_path=existing_profil_path)

@app.route('/aktivitaskamu')
@login_required
def aktivitas():
# Ambil riwayat deteksi untuk pengguna yang sedang login
    user_id = session['userid']
    history_deteksi = (
        db.session.query(HistoryDeteksi, Users.nama)
        .join(Users)
        .filter(HistoryDeteksi.user_id == user_id)
        .all()
    )
    return render_template('aktivitas.html', history_deteksi=history_deteksi)



#route admin
@app.route('/dashboard',methods=['GET','POST'])
@admin_login_required
def dashboard():
    total_users = Users.query.count()
    total_tps = TPS.query.count()
    total_bank = Banksampah.query.count()
    total_produk = Produk.query.count()
    total_sampah = Sampah.query.count()
    total_artikel = Artikel.query.count()
    total_history = HistoryDeteksi.query.count()
    total_hasil = Hasil_model.query.count()
    
    return render_template('dashboard.html',total_users=total_users,
                           total_tps=total_tps,total_bank=total_bank,
                           total_produk=total_produk,total_sampah= total_sampah,
                           total_artikel= total_artikel, total_hasil= total_hasil, total_history=total_history,
                           page='dashboard')

# ##route data user
@app.route('/datauser', methods=['GET', 'POST'])
def datauser():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        

        foto_profil = request.files['foto_profil']
        if profil:
            filename = secure_filename(profil.filename)
            profil_path = os.path.join('uploads', 'foto_profil', filename)  # Use os.path.join for path construction
            profil.save(os.path.join('static', profil_path))

        if not nama or not email or not password:
            flash('Mohon lengkapi semua kolom.', 'danger')
        else:
            # Disini Anda dapat menyimpan data pengguna baru ke database
            # Misalnya, menggunakan SQLAlchemy atau metode penyimpanan data yang Anda pilih
            user = Users(
                nama=nama, email=email, password=password, role=role, foto_profil=profil_path)
            db.session.add(user)
            db.session.commit()
            flash('Data user berhasil ditambahkan', 'success')

    # Dapatkan data pengguna dari database (sesuaikan dengan model dan database Anda)
    user = Users.query.all()

    return render_template('datauser.html', users=user, page=datauser)


from werkzeug.utils import secure_filename

@app.route('/edituser/<int:user_id>', methods=['GET', 'POST'])
def edituser(user_id):
    user = Users.query.get(user_id)

    if request.method == 'POST':
        user.nama = request.form['nama']
        user.email = request.form['email']
        user.password = request.form['password']
        user.role = request.form['role']
        new_foto_profil = request.files['foto_profil']

        if not user.nama or not user.email or not user.password:
            flash('Mohon lengkapi semua kolom.', 'danger')
        else:
            # Check if a new profile picture is uploaded
            if new_foto_profil:
                # Delete the existing profile picture before saving the new one
                if user.foto_profil:
                    existing_path = os.path.join('static', user.foto_profil)
                    if os.path.exists(existing_path):
                        os.remove(existing_path)

                # Save the new profile picture
                filename = secure_filename(new_foto_profil.filename)
                profil_path = os.path.join('uploads', 'foto_profil', filename)
                new_foto_profil.save(os.path.join('static', profil_path))
                user.foto_profil = profil_path

            db.session.commit()
            flash('Data user berhasil diperbarui', 'success')
            return redirect(url_for('datauser'))

    return render_template('edituser.html', user=user)



@app.route('/deleteuser/<int:user_id>', methods=['GET'])
def deleteuser(user_id):
    user = Users.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        flash('Data user berhasil dihapus', 'success')
    else:
        flash('Data user tidak ditemukan', 'danger')

    return redirect(url_for('datauser'))

###route data sampah
@app.route('/sampah', methods=['GET', 'POST'])
def sampah():
    if request.method == 'POST':
        kode = request.form['kode']
        nama = request.form['nama']
        jenis = request.form['jenis']
        satuan = request.form['satuan']
        harga = request.form['harga']
        
        if not kode or not nama or not jenis or not satuan or not harga:
            flash('Mohon lengkapi semua kolom.', 'danger')
            
        sampah = Sampah(
            kode=kode,
            nama=nama,
            jenis=jenis,
            satuan=satuan,
            harga=harga
        )
        db.session.add(sampah)
        db.session.commit()
        flash("Data berhasil dinputkan")

    # Set the pagination configuration
    # page = request.args.get('page', 1, type=int)
    sampah = Sampah.query.all()
    return render_template('datasampah.html', sampah=sampah, page='datasampah')

@app.route('/editsampah/<int:sampah_id>', methods=['GET', 'POST'])
def edit_sampah(sampah_id):
    sampah = Sampah.query.get(sampah_id)

    if sampah is None:
        flash('Data Sampah tidak ditemukan', 'danger')
        return redirect(url_for('sampah'))

    if request.method == 'POST':
        sampah.kode = request.form['kode']
        sampah.nama = request.form['nama']
        sampah.jenis = request.form['jenis']
        sampah.satuan = request.form['satuan']
        sampah.harga = request.form['harga']

        try:
            db.session.commit()
            flash('Data Sampah berhasil diperbarui', 'success')
            return redirect(url_for('sampah'))
        except:
            flash('Terjadi kesalahan. Data Sampah gagal diperbarui', 'danger')

    return render_template('edit_sampah.html', sampah=sampah)

@app.route('/delete/<int:sampah_id>', methods=['GET'])
def delete_sampah(sampah_id):
    sampah = Sampah.query.get(sampah_id)

    if sampah:
        db.session.delete(sampah)
        db.session.commit()
        flash('Data Sampah berhasil dihapus', 'success')
    else:
        flash('Data Sampah tidak ditemukan', 'danger')

    return redirect(url_for('sampah'))

###route databanksampah
@app.route('/databanksampah', methods=['GET', 'POST'])
def databanksampah():
    if request.method == 'POST':
        nama = request.form['nama']
        alamat = request.form['alamat']
        pj = request.form['pj']
        no_hp = request.form['no_hp']
        
        if not nama or not alamat or not pj or not no_hp:
            flash('Mohon lengkapi semua kolom.', 'danger')
            
        data_banksampah = Banksampah(
            nama=nama,
            alamat=alamat,
            pj=pj,
            no_hp=no_hp
        )
        db.session.add(data_banksampah)
        db.session.commit()
        flash("Data berhasil dinputkan")

    # Set the pagination configuration
    # page = request.args.get('page', 1, type=int)
    data_banksampah = Banksampah.query.all()
    return render_template('databank.html', data_banksampah=data_banksampah, page='databanksampah')

@app.route('/editbanksampah/<int:id>', methods=['GET', 'POST'])
def edit_banksampah(id):
    data_banksampah = Banksampah.query.get(id)

    if request.method == 'POST':
        data_banksampah.nama = request.form['nama']
        data_banksampah.alamat = request.form['alamat']
        data_banksampah.pj = request.form['pj']
        data_banksampah.no_hp = request.form['no_hp']

        if not data_banksampah.nama or not data_banksampah.alamat or not data_banksampah.pj or not data_banksampah.no_hp:
            flash('Mohon lengkapi semua kolom.', 'danger')
        else:
            db.session.commit()
            flash('Data banksampah berhasil diperbarui', 'success')
            return redirect(url_for('databanksampah'))

    return render_template('editbank.html', data_banksampah=data_banksampah, page='databanksampah')

@app.route('/delete_banksampah/<int:banksampah_id>', methods=['GET'])
def delete_banksampah(banksampah_id):
    banksampah = Banksampah.query.get(banksampah_id)

    if banksampah:
        db.session.delete(banksampah)
        db.session.commit()
        flash('Data banksampah berhasil dihapus', 'success')
    else:
        flash('Data banksampah tidak ditemukan', 'danger')

    return redirect(url_for('databanksampah'))
    

###route datatps
@app.route('/datatps', methods=['GET','POST'])
def datatps():
    if request.method == 'POST':
        nama = request.form['nama']
        alamat = request.form['alamat']
        kabupaten_kota = request.form['kabupaten_kota']
        kecamatan = request.form['kecamatan']
        desa = request.form['desa']
        
        if not nama or not alamat or not kabupaten_kota or not kecamatan or not desa:
            flash('Mohon lengkapi semua kolom.', 'danger')
            
        data_tps = TPS(
            nama=nama,
            alamat=alamat,
            kabupaten_kota=kabupaten_kota,
            kecamatan=kecamatan,
            desa=desa
        )
        db.session.add(data_tps)
        db.session.commit()
        flash("Data berhasil dinputkan")
    
    data_tps = TPS.query.all()
    return render_template('datatps.html', data_tps=data_tps ,page='datatps')

@app.route('/edittps/<int:id>', methods=['GET', 'POST'])
def edit_tps(id):
    data_tps = TPS.query.get(id)

    if request.method == 'POST':
        data_tps.nama = request.form['nama']
        data_tps.alamat = request.form['alamat']
        data_tps.kabupaten_kota = request.form['kabupaten_kota']
        data_tps.kecamatan = request.form['kecamatan']
        data_tps.desa = request.form['desa']

        if not data_tps.nama or not data_tps.alamat or not data_tps.kabupaten_kota or not data_tps.kecamatan or not data_tps.desa:
            flash('Mohon lengkapi semua kolom.', 'danger')
        else:
            db.session.commit()
            flash('Data TPS berhasil diperbarui', 'success')
            return redirect(url_for('datatps'))

    return render_template('edittps.html', data_tps=data_tps, page='datatps')

@app.route('/deletetps/<int:id>', methods=['GET'])
def delete_tps(id):
    data_tps = TPS.query.get(id)

    if data_tps:
        db.session.delete(data_tps)
        db.session.commit()
        flash('Data TPS berhasil dihapus', 'success')
    else:
        flash('Data TPS tidak ditemukan', 'danger')

    return redirect(url_for('datatps'))


### route data history

@app.route('/datahistory')
@login_required
def history_deteksi():
    # Mengganti query dengan query yang memanfaatkan relasi dan menampilkan nama pengguna
    history_deteksi = (
        db.session.query(
            HistoryDeteksi,
            Users.nama.label('username')
        )
        .join(Users)
        .all()
    )

    return render_template('datahistory.html', history_deteksi=history_deteksi, page='datahistory')

@app.route('/delete_history_deteksi/<int:id>', methods=['GET', 'POST'])
def delete_history_deteksi(id):
    # Ambil data history_deteksi berdasarkan ID
    history_deteksi = HistoryDeteksi.query.get(id)

    if history_deteksi:
        # Hapus entri dari basis data
        db.session.delete(history_deteksi)
        db.session.commit()

        flash('Data deteksi berhasil dihapus', 'success')
    else:
        flash('Data deteksi tidak ditemukan', 'danger')

    return redirect(url_for('history_deteksi'))

# app.config['UPLOAD_FOLDER'] = 'static/uploads'
###route dataartikel
@app.route('/datartikel', methods=['GET', 'POST'])
def datartikel():
    if request.method == 'POST':
        judul = request.form.get('judul')
        isi_artikel = request.form.get('isi_artikel')
        kategori = request.form.get('kategori')

        gambar = request.files['gambar']
        if gambar:
            filename = secure_filename(gambar.filename)
            gambar_path = os.path.join('uploads', 'artikel', filename)  # Use os.path.join for path construction
            gambar.save(os.path.join('static', gambar_path))

        if not judul or not gambar or not isi_artikel or not kategori:
            flash('Mohon lengkapi semua kolom.', 'danger')
            # Handle validation error, e.g., redirect or render_template with an error message

        data_artikel = Artikel(
            judul=judul,
            gambar=gambar_path,
            isi_artikel=isi_artikel,
            kategori=kategori
        )
        db.session.add(data_artikel)
        db.session.commit()
        flash('Artikel berhasil ditambahkan!', 'success')

    data_artikel = Artikel.query.all()
    return render_template('datartikel.html', data_artikel=data_artikel, page='datartikel')


from werkzeug.utils import secure_filename

@app.route('/editartikel/<int:id>', methods=['GET', 'POST'])
def edit_artikel(id):
    data_artikel = Artikel.query.get(id)

    if request.method == 'POST':
        # Existing image path
        existing_image_path = os.path.join('static', data_artikel.gambar)

        # Update fields
        data_artikel.judul = request.form['judul']
        new_gambar = request.files['gambar']
        data_artikel.isi_artikel = request.form['isi_artikel']
        data_artikel.kategori = request.form['kategori']

        if not data_artikel.judul or not data_artikel.isi_artikel or not data_artikel.kategori:
            flash('Mohon lengkapi semua kolom.', 'danger')
        else:
            # Check if a new image is uploaded
            if new_gambar:
                # Save the new image file
                filename = secure_filename(new_gambar.filename)
                gambar_path = os.path.join('uploads', 'artikel', filename)
                new_gambar.save(os.path.join('static', gambar_path))

                # Remove the existing image file
                if os.path.exists(existing_image_path):
                    os.remove(existing_image_path)

                # Update the gambar field with the new image path
                data_artikel.gambar = gambar_path

            # Commit changes to the database
            db.session.commit()

            flash('Data artikel berhasil diperbarui', 'success')
            return redirect(url_for('datartikel'))

    return render_template('editartikel.html', data_artikel=data_artikel, page='datartikel')


@app.route('/delete_artikel/<int:artikel_id>', methods=['GET'])
def delete_artikel(artikel_id):
    artikel = Artikel.query.get(artikel_id)

    if artikel:
        db.session.delete(artikel)
        db.session.commit()
        flash('Data artikel berhasil dihapus', 'success')
    else:
        flash('Data artikel tidak ditemukan', 'danger')

    return redirect(url_for('datartikel'))



###route data Produk
@app.route('/dataproduk', methods=['GET', 'POST'])
def dataproduk():
    if request.method == 'POST':
        nama_produk = request.form.get('nama_produk')
        link_video = request.form.get('link_video')

        gambar_produk = request.files['gambar_produk']
        if gambar_produk:
            filename = secure_filename(gambar_produk.filename)
            gambar_path = os.path.join('uploads', 'produk', filename)  # Use os.path.join for path construction
            gambar_produk.save(os.path.join('static', gambar_path))

        if not nama_produk or not gambar_produk or not link_video:
            flash('Mohon lengkapi semua kolom.', 'danger')
            # Handle validation error, e.g., redirect or render_template with an error message

        data_produk = Produk(
            nama_produk=nama_produk,
            gambar_produk=gambar_path,
            link_video=link_video
        )
        db.session.add(data_produk)
        db.session.commit()
        flash('Produk berhasil ditambahkan!', 'success')

    data_produk = Produk.query.all()
    return render_template('dataproduk.html', data_produk=data_produk, page='dataproduk')


@app.route('/editproduk/<int:id>', methods=['GET', 'POST'])
def edit_produk(id):
    data_produk = Produk.query.get(id)

    if request.method == 'POST':
        # Existing image path
        existing_image_path = os.path.join('static', data_produk.gambar_produk)

        # Update fields
        data_produk.nama_produk = request.form['nama_produk']
        new_gambar_produk = request.files['gambar_produk']
        data_produk.link_video = request.form['link_video']

        if not data_produk.nama_produk or not data_produk.link_video:
            flash('Mohon lengkapi semua kolom.', 'danger')
        else:
            # Check if a new image is uploaded
            if new_gambar_produk:
                # Save the new image file
                filename = secure_filename(new_gambar_produk.filename)
                gambar_path = os.path.join('uploads', 'produk', filename)
                new_gambar_produk.save(os.path.join('static', gambar_path))

                # Remove the existing image file
                if os.path.exists(existing_image_path):
                    os.remove(existing_image_path)

                # Update the gambar field with the new image path
                data_produk.gambar_produk = gambar_path

            # Commit changes to the database
            db.session.commit()

            flash('Data produk berhasil diperbarui', 'success')
            return redirect(url_for('dataproduk'))

    return render_template('editproduk.html', data_produk=data_produk, page='dataproduk')


@app.route('/delete_produk/<int:produk_id>', methods=['GET'])
def delete_produk(produk_id):
    produk = Produk.query.get(produk_id)

    if produk:
        db.session.delete(produk)
        db.session.commit()
        flash('Data produk berhasil dihapus', 'success')
    else:
        flash('Data produk tidak ditemukan', 'danger')

    return redirect(url_for('dataproduk'))
    

### route data sentmen
@app.route('/datasentimen', methods=['GET','POST'])
def datasentimen():
    data_sentimen = Hasil_model.query.all()
    return render_template('datasentimen.html', data_sentimen=data_sentimen ,page='datasentimen')

@app.route('/deletesentimen/<int:id>', methods=['GET'])
def delete_sentimen(id):
    
    datasentimen = Hasil_model.query.get(id)

    if datasentimen:
        db.session.delete(datasentimen)
        db.session.commit()
        flash('sentimen berhasil dihapus', 'success')
    else:
        flash('sentimen tidak ditemukan', 'danger')

    return redirect(url_for('datasentimen'))

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
