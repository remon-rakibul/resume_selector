from io import StringIO
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
import spacy
import re

nlp = spacy.load('en_core_web_sm')

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
    doc = nlp(u'{}'.format(data))
    tokens = [token.text for token in doc if not token.is_stop]
    tokens = [token.text for token in doc if not len(token.text) <= 2]
    data = ' '.join(tokens)
    data = re.sub(r'\s+[a-z]\s+', ' ', data)
    data = re.sub(r'^[a-z]\s+', ' ', data)
    data = re.sub(r'\W', ' ', data)
    data = re.sub(r'\d', ' ', data)
    data = re.sub(r'\s+', ' ', data)
    return data

def get_names(data):
    data = preprocess(data)
    doc = nlp(data)
    persons = []
    for t in doc.ents:
        if t.label_ == 'PERSON':
            persons.append(t.text)
    return persons

def get_email_addresses(data):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(data)

def get_mobile_numbers(data):
    r = re.compile(r"\(?\+?[8]{2}?0?\)?\0?-?0?[0-9]{3}-?[0-9]{3}-?[0-9]{4}|[0-9]{4}-?[0-9]{3}-?[0-9]{4}|[0-9]{5}-[0-9]{6}")
    found_numbers = r.findall(data)
    return found_numbers

data = pdfparser('pdf/cv.pdf')

names = get_names(data)
emails = get_email_addresses(data)
numbers = get_mobile_numbers(data)