import pymorphy3

morph = pymorphy3.MorphAnalyzer()

def lemmatize_text(text):
    # print(text)
    text_prepared = text.split(" ")
    # print(text_prepared)
    lemmas = [morph.parse(token)[0].normal_form for token in text_prepared]
    lemmas = " ".join(lemmas)
    # print("lemmas", lemmas)
    return lemmas