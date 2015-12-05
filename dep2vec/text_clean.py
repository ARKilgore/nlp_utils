import string

def rem_punc(text):
    out = text.translate(string.maketrans("",""), string.punctuation)
    return out

def clean(text):
    return rem_punc(text).lower().rstrip()

def list_clean(text):
    res = []
    for doc in text:
        res.append(clean(text))
    return res
