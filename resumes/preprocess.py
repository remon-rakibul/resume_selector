import os
import re
import spacy
nlp = spacy.load('en_core_web_sm')

files = os.listdir('text')

try:
    os.mkdir('processed')
except:
    pass

for file in files:
    with open('text/'+file, encoding='utf8') as f:
        data = f.read()
        data = re.sub(r'\W+', ' ', data)
        data = data.lower()
        data = re.sub(r'\\t+|\\r+', ' ', data)
        data = re.sub(r'â+', ' ', data)
        data = re.sub(r'ï+', ' ', data)
        data = re.sub(r'\d+', ' ', data)
        data = re.sub(r'\s+', ' ', data)
        doc = nlp(u'{}'.format(data))
        tokens = [token.text for token in doc if not token.is_stop]
        data = ' '.join(tokens)
        with open('processed/'+file, 'w', encoding='utf8') as ff:
            ff.write(data)
            print('preprocessing '+ file)