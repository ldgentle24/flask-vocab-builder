import nltk
import os

nltk_data_path = os.path.join(os.path.dirname(__file__), "nltk_data")
nltk.data.path.append(nltk_data_path)

from flask import Flask, render_template, request
from nltk.corpus import wordnet as wn, words


def get_derivational_forms(input_word):
    forms = set()
    for lemma in wn.lemmas(input_word):
        forms.add(lemma.name())
        for related_lemma in lemma.derivationally_related_forms():
            forms.add(related_lemma.name())
    return forms


def check_prefix_suffix(input_word):
    english_words = set(words.words())
    return [
        w
        for w in english_words
        if (w.endswith(input_word) or w.startswith(input_word))
        and len(wn.synsets(w)) > 0
    ]


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check_word", methods=["POST"])
def check_word():
    word = request.form["word"]
    derivational_forms = get_derivational_forms(word)
    all_forms = []
    
    for w in derivational_forms:
        ls_of_w = check_prefix_suffix(w)
        all_forms.extend(ls_of_w)

    return (
        ", ".join(all_forms)
        if all_forms
        else "No derivational forms found for '{}'.".format(word)
    )


if __name__ == "__main__":
    app.run(debug=True)
