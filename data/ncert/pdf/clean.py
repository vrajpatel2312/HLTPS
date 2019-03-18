from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO
import re
import os
import sys
import subprocess
import shutil

path = '.'
 
if len(sys.argv) == 2:
    path = sys.argv[1]

def pdf_to_text(path):
    manager = PDFResourceManager()
    retstr = BytesIO()
    layout = LAParams(all_texts=True)
    device = TextConverter(manager, retstr, laparams=layout)
    filepath = open(path, 'rb')
    interpreter = PDFPageInterpreter(manager, device)

    for page in PDFPage.get_pages(filepath, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    filepath.close()
    os.remove(path)
    device.close()
    retstr.close()
    return text


if __name__ == "__main__":
    print(path)
    vra = os.listdir(path)
    for x in vra:
        status = re.findall('[0-9]{3}', x)
        if len(status)!=1:
            x=path+x
            os.remove(x)
    subject=str(input("Name of subject"))
    grade=str(input("Name of class"))
    print(path)
    vra = os.listdir(path)
    i=0
    for x in vra:
        i=i+1
        j=str(i)
        filename=path+"/"+subject+grade+j+".txt"
        filepath = path+x
        text = pdf_to_text(filepath)
        f = open( filename, 'w' )
        text1=str(text, 'utf-8')
        text1 = re.sub('[^a-zA-Z0-9\s\.\,]', '', text1)
        text1 = re.sub(r'[A-Z]+(?![a-z])', '', text1)
        text1 = text1.replace('\n',' ')
        text1 = text1.replace('Fig. \u0031','').replace('Fig. \u0032','').replace('Fig. \u0033','').replace('Fig. \u0034','').replace('Fig. \u0035','').replace('Fig. \u0036','').replace('Fig. \u0037','').replace('Fig. \u0038','').replace('Fig. \u0039','').replace('Fig. \u0030','')
        head, sep, tail = text1.partition('Fill in the blanks')
        text1 = head
        head, sep, tail = text1.partition('Exercises')
        text1 = head
        text1 = text1.replace('\"','')
        text1 = text1.replace('\'','')
        text1 = text1.replace('  ',' ')
        text1 = re.sub(' +', ' ',text1)
        text1 = text1.strip()
        text1 = text1.replace('\s+','')
        text1 = text1.replace(u'\u000C',r'\n\n')
        f.write("{\"id\": \"" + filename+"\", \"text\": \"" + text1 + "\"}")
        f.close()
    #subprocess.call(['/home/vraj/DrQA/scripts/retriever/build_db.py',path ,path+".db"])
    #python /home/vraj/DrQA/scripts/retriever/build_db.py  /home/vraj/DrQA/data/ncert/data.db
