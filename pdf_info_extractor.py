from io import StringIO
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from nltk.corpus import stopwords
import nltk
import re

def pdfparser(data):
    fp = open(data, 'rb')
    resource_manager = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(resource_manager,retstr, codec=codec, laparams=laparams)
    interpreter =PDFPageInterpreter(resource_manager, device)
 
    # Process each page contained in thedocument.
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data = retstr.getvalue()
    return data

def preprocess(data):
    sentences = nltk.sent_tokenize(data)
    tagged_sentences = []
    for i in range(len(sentences)):
        text = re.sub(r'\s+[a-z]\s+', ' ', sentences[i])
        text = re.sub(r'^[a-z]\s+', ' ', text)
        text = re.sub(r'\W', ' ', text)
        text = re.sub(r'\d', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        words = nltk.word_tokenize(text)
        words = [word for word in words if word.lower() not in stopwords.words('english')]
        tagged_words = nltk.pos_tag(words)
        tagged_sentences.append(tagged_words)
    return tagged_sentences

def get_email_addresses(data):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(data)

def get_names(data):
    tagged_sentences = preprocess(data)
    names = []
    for tagged_sentence in tagged_sentences:
        for tagged_word in nltk.ne_chunk(tagged_sentence):
            if type(tagged_word) == nltk.tree.Tree:
                if tagged_word.label() == 'PERSON':
                    names.append(' '.join([word[0] for word in tagged_word]))
    return names

def get_mobile_numbers(data):
    r = re.compile(r"\(?\+?[8]{2}?0?\)?\0?-?0?[0-9]{3}-?[0-9]{3}-?[0-9]{4}|[0-9]{4}-?[0-9]{3}-?[0-9]{4}|[0-9]{5}-[0-9]{6}")
    found_numbers = r.findall(data)
    return found_numbers

data = pdfparser('pdf/cv.pdf')

names = get_names(data)
emails = get_email_addresses(data)
numbers = get_mobile_numbers(data)