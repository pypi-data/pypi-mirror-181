punctuations = ['(', ')', ';', ':', '[', ']', ',']
stop_words = ['', ' ']


def get_words(text):
    tokens = text.split(" ")
    keywords = [word for word in tokens if word not in stop_words and word not in punctuations]
    return keywords
