from __future__ import division, print_function
# coding=utf-8
import numpy as np
# Keras
from keras.applications.imagenet_utils import preprocess_input
from keras.models import load_model
from keras.preprocessing import image
# Path tempat model disimpan
MODEL_PATH = 'model/ecogreenq2fix.h5'
model_detec = load_model(MODEL_PATH)
# Label kategori sampah yang dapat diprediksi
label = [
    "Aluminium",
    "Botol Plastik",
    "Bungkus Plastik",
    "Cup Gelas",
    "Galon",
    "Kaca",
    "Kardus",
    "Kertas",
    "Sampah Elektronik",
    "Sampah Organik"
]
# Fungsi untuk memprediksi kategori sampah dari gambar
def model_predict(img):
    # Preprocessing gambar dan mengubah ukuran menjadi 224x224
    i = np.asarray(img.resize((224, 224))) / 255.0
    i = i.reshape(1, 224, 224, 3)
    # Melakukan prediksi menggunakan model
    pred = model_detec.predict(i)
    # Mendapatkan label kategori sampah dengan nilai probabilitas tertinggi
    result_label = label[np.argmax(pred)]
    # Menghitung akurasi prediksi dalam persentase
    result_accuracy = np.max(pred) * 100
    return result_label, result_accuracy
