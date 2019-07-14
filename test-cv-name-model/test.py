import spacy

nlp = spacy.load('name-cv-bn')

d = nlp("Md. Shahidul islam is a ml engineer. his number is +8801748303363. mail him at shawon08@gmail.com")
for e in d.ents:
    print(e.text, e.label_)