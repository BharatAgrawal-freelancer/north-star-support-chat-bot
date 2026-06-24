import pickle
import numpy as np
import tensorflow as tf

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# Load model
model = tf.keras.models.load_model("model/chatbot_model.keras")

# Load vocabulary and classes
with open("model/words.pkl", "rb") as f:
    words = pickle.load(f)

with open("model/classes.pkl", "rb") as f:
    classes = pickle.load(f)


def bag_of_words(sentence):
    sentence_words = word_tokenize(sentence.lower())

    sentence_words = [
        lemmatizer.lemmatize(word)
        for word in sentence_words
    ]

    bag = [0] * len(words)

    for sw in sentence_words:
        for i, w in enumerate(words):
            if w == sw:
                bag[i] = 1

    return np.array(bag)


def predict_intent(message):
    bow = bag_of_words(message)

    result = model.predict(
        np.array([bow]),
        verbose=0
    )[0]

    index = np.argmax(result)

    confidence = result[index]

    if confidence < 0.5:
        return None

    return classes[index]