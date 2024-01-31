from keras.models import load_model
import json
import random
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
# Memuat model dan data training dari file
model = load_model('model/chatbot_model.h5')
with open('model/sampah.json', 'r', encoding='utf-8') as file:
    intents = json.load(file)
# Memuat data yang telah diproses sebelumnya
words = pickle.load(open('model/words.pkl', 'rb'))
classes = pickle.load(open('model/classes.pkl', 'rb'))
lemmatizer = WordNetLemmatizer()
# Fungsi untuk membersihkan kalimat
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words
# Fungsi Bag-of-Words: mengembalikan array 0 atau 1 untuk setiap kata di bag yang ada dalam kalimat
def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))
# Fungsi untuk memprediksi kelas atau intent dari kalimat
def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list
# Fungsi untuk mendapatkan respons dari intent yang diprediksi
def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result
# Fungsi utama untuk merespons pesan dari pengguna
def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res