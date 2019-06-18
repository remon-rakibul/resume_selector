'''
from io import StringIO
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter

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

data = pdfparser('pdf/cv.pdf')
'''
import io
import os
from io import StringIO
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter

def pdfparser(data_dir):
    files = os.listdir(data_dir)
    try:
        os.mkdir(data_dir+'txt')
    except:
        pass  
    for file in files:
        fp = open(data_dir+file, 'rb')
        resource_manager = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(resource_manager,retstr, codec=codec, laparams=laparams)
        interpreter =PDFPageInterpreter(resource_manager, device)
        txt = ''
        # Process each page contained in thedocument.
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
            data = retstr.getvalue()
            txt += data
        with io.open(data_dir+'txt/'+file[:-4]+'.txt', "w", encoding="utf-8") as f:
            f.write(txt)
        
pdfparser('resumes/pdf/')
