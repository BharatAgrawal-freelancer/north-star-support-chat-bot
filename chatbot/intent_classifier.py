import pickle
import numpy as np
import tensorflow as tf

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# Load SavedModel
model = tf.saved_model.load("model/saved_model")
infer = model.signatures["serving_default"]

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

    return np.array(bag, dtype=np.float32)


def predict_intent(message):

    bow = bag_of_words(message)

    outputs = infer(
        tf.constant(np.array([bow]), dtype=tf.float32)
    )

    # SavedModel generally has a single output tensor
    result = list(outputs.values())[0].numpy()[0]

    index = np.argmax(result)

    confidence = result[index]

    if confidence < 0.5:
        return None

    return classes[index]