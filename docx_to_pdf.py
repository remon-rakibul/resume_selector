from docx import Document
import io
import shutil
import os

def convertDocxToText(path):
    for d in os.listdir(path):
        fileExtension=d.split(".")[-1]
        if fileExtension =="docx":
            docxFilename = path + d
            print(docxFilename)
            document = Document(docxFilename)
            textFilename = path + d.split(".")[0] + ".txt"
            with io.open(textFilename,"w", encoding="utf-8") as textFile:
                for para in document.paragraphs: 
                    textFile.write(para.text)

path= "dx/"
convertDocxToText(path)

from pylab import *
import urllib2
import twill
from twill.commands import *
import re
import os
import magic
import sys
from docx import *
 
# Set up dummy non-existent file to suppress twill output
f = open(os.devnull,'w')
twill.set_output(f)
 
# Navigate to the website and authenticate
url = 'http://linguistlist.org/confservices/EasyAbs/login.cfm'
go(url)
fv('2','emailaddress','[INSERT EMAIL]')
fv('2','password','[INSERT PASSWORD]')
submit(0)
follow('View/Assign Abstracts')
 
# Grab the paper IDs (6 digit numbers)
pagetext = show()
allIDs = [pagetext[num.start()+1:num.start()+7] for num in list(re.finditer('t19',pagetext))]
 
# Grab all the paper links
links = list(showlinks())
links = links[169:-5:3]     # The first paper link will always be 169. Then go by 3s.
 
print "There are %i paper IDs." % len(allIDs)
print "There are %i papers." % len(links)
 
# Double check that there are equal numbers for papers and paper IDs
if len(allIDs)!=len(links):
    print "There is something wrong!"
else:
    problem_papers = []
    for i,link in enumerate(links):
        item = str(link)
 
        # Just double check (for redundancy) that it's not the delete button
        if item.find('?deleteabstract')==-1:
 
            # Grabbing the file
            try:
                start = item.find(" url='") + 6
                stop= item[start:].find("', ") + start
                pdfpage = item[start:stop]
                go(pdfpage)
                save_html(allIDs[i])
            except:
                problem_papers.append(allIDs[i])
    print "Problem Papers:n"
    for paper in problem_papers:
        print paper
 
# Then you need to manually download the problem papers - something wrong with weblink
# There should be only a few of them
 
# Now, loop through files in folder and create new text files
files = sort(os.listdir('.'))
badfiles = []
for i,filename in enumerate(files):
    # Determine what sort of file it is and then strip out text accordingly:
    ms = magic.open(magic.MAGIC_NONE)
    ms.load()
    ftype = ms.file(filename)
 
    # PDFs
    if ftype.find('PDF')!=-1:
        if filename[-4:]!='.pdf':
            os.rename(filename,filename+'.pdf')
            filename = filename+'.pdf'
 
        # Different pdf to text methods for reference:
        #os.system('pdf2txt -o' + filename[:-4]+'.txt' + ' ' + filename)
        #os.system('pdftotext ' + filename + ' ' + filename[:-4]+'.txt'
        #os.system('pdf2ps ' + filename + ' ' + filename[:-4]+'.ps')
        #os.system('ps2txt ' + filename+'.ps' + ' ' + filename[:-4]+'.txt')
 
        # Check to see if it was a strange pdf format (either from a certain mac version
        # or perhaps from a font type)
        # If it is, keep it and remove the tabs
        # If not, convert with other method
        os.system('ebook-convert ' + filename + ' ' + filename[:-4]+'.txt')
        tmp = open(filename[:-4]+'.txt','r')
        text = tmp.read()
        alltabs = len([rtrn.start() for rtrn in list(re.finditer('t',text))])
        if alltabs>10:
            tmp2 = open(filename[:-4]+'.txt.tmp','w')
            tmp2.write(text.replace('t',''))
            tmp.close()
            tmp2.close()
            os.system('rm ' + filename[:-4]+'.txt')
            os.system('mv ' + filename[:-4]+'.txt.tmp' + ' ' + filename[:-4]+'.txt')
        else:
            os.system('rm ' + filename[:-4]+'.txt')
            os.system('pdf2txt -o' + filename[:-4]+'.txt' + ' ' + filename)
 
    # Word Documents
    elif ftype.find('Composite Document File')!=-1:
        os.system('antiword ' + filename + ' > ' + filename+'.txt')
 
    # Open Office files
    elif ftype.find('OpenDocument')!=-1:
        os.system('odt2txt ' + filename + ' > ' + filename+'.txt')
 
    # Microsoft 2007 .docx files
    elif ftype.find('Microsoft Word 2007+')!=-1:
        newfile = open(filename+'.txt','w')
        document = opendocx(filename)
        txt = getdocumenttext(document)
        for line in txt:
            newfile.write(line.encode('ascii','ignore')+'nn')
        newfile.close()
    else:
        badfiles.append(filename)
        print filename + " is an unrecognized file type!"
 
# Combine them into one long file
all_textfiles = [f for f in sort(os.listdir('.')) if f[-4:]=='.txt']
abstracts = open('abstracts.txt','w')
print len(all_textfiles)
for textfile in all_textfiles:
    tmp = open(textfile,'r')
    text = tmp.read()
    abstracts.write(textfile+'nn')
    abstracts.write(text)
    abstracts.write('n'*20)
    tmp.close()
abstracts.close()
 
print "Problem Files:n"
for fl in badfiles:
    print fl