from django.http import FileResponse
from django.http import HttpResponse
from django.shortcuts import render
from pkg_resources import set_extraction_path
from .summary import sentence
from Mainapp.models import File
from django.contrib.auth.models import User
from django.contrib import messages
import pdfminer
from pdfminer.high_level import extract_text
from docx import Document
import pytesseract
import os
import googletrans
from googletrans import Translator
import json
import torch
import pandas as pd
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration
from django.core.files.storage import FileSystemStorage
import urllib


# Create your views here.

global stext
global title
global encode_title
global totals


def summary(request):

    global stext
    global title

    if request.method == 'POST':
        # Fetching the form data
        uploadedFile = request.FILES.get('uploadedFile')
        if uploadedFile:
            fileTitle = uploadedFile.name
            writer = request.user.first_name
            user_id = request.user.id
            me = User.objects.get(id=user_id)

            if(fileTitle.find("txt") > 0) or fileTitle.find("TXT") > 0:
                with open(fileTitle, 'wb') as file:
                    for chunk in uploadedFile.chunks():
                        file.write(chunk)

                with open(fileTitle, encoding='utf-8') as file:
                    text = file.readlines()

                text = [line.rstrip('\n') for line in text]
                s = "".join(text)

                os.remove(fileTitle)
                stext = s

            elif(fileTitle.find("pdf") > 0) or fileTitle.find("PDF") > 0:
                with open(fileTitle, 'wb') as file:
                    for chunk in uploadedFile.chunks():
                        file.write(chunk)

                text = extract_text(fileTitle)
                text = text.replace('\n', ' ')

                os.remove(fileTitle)
                stext = text

            elif(fileTitle.find("docx") > 0) or fileTitle.find("DOCS") > 0:
                with open(fileTitle, 'wb') as file:
                    for chunk in uploadedFile.chunks():
                        file.write(chunk)

                doc = Document(fileTitle)
                text = []

                for p in doc.paragraphs:
                    text.append(p.text)

                text = "\n".join(text)

                os.remove(fileTitle)
                stext = text

            elif(fileTitle.find("png") > 0 or
                 fileTitle.find("PNG") or
                 fileTitle.find("ipg") or
                 fileTitle.find("JPG")):
                with open(fileTitle, 'wb') as file:
                    for chunk in uploadedFile.chunks():
                        file.write(chunk)

                text = pytesseract.image_to_string(
                    fileTitle, lang='kor+eng',
                    config='-c perserve_interword_spaces=1 --psm 4')
                text = text.replace('\n', ' ')
                text.strip()

                os.remove(fileTitle)
                stext = text

            else:
                # message = "파일형식이 잘못되었습니다."
                # return HttpResponse('%s' % (message) )
                messages.warning(request, '파일 형식이 잘못되었습니다.')
                return render(request, 'Summary/summary.html')

            # Save File
            # Saving the information in the database
            file = File(
                f_title=fileTitle,
                uploadedFile=uploadedFile,
                f_writer=writer,
                user_id=me,
            )

            file.save()
            title = fileTitle.split('.')[0]

            return render(request, 'Summary/result.html', {'text': stext})

        # 업로드 파일 없을 때 예외 처리
        else:
            messages.warning(request, '파일을 업로드해 주세요.')

    return render(request, 'Summary/summary.html')


def result2(request):
    global stext
    global title
    global encode_title

    text = stext

    max = 500
    result = []
    if len(text) > 500:
        for i in range(len(text) // max):
            result.append(sentence(text[i*max:(i+1)*max]))
            result.append(' ')
        result.append(sentence(text[(i+1)*max:]))
        result = "".join(result)

    else:
        result.append(sentence(text))
        result = "".join(result)

    encode_title = urllib.parse.quote(string=f'{title}_summary.txt')

    file = open(f'media/{encode_title}', 'w', encoding="UTF-8")
    file.write(result)                # 파일에 문자열 저장
    file.close()                      # 파일 객체 닫기

    return render(request, 'Summary/result2.html', {'result': result})


def downloadFile(request):
    global title
    global encode_title

    file_path = os.path.abspath('media/')
    file_name = encode_title
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_name, 'rb'),
                            content_type='text/plain')
    response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s'% file_name

    return response
######################
translator = Translator()

    

def slice_1(request):
    global stext

    text=stext
    # global slice_text

    a = divmod(len(text),1)
    if a[0] > 5000:
        slice_text = text[:5000]
    else:
        slice_text = text[:a[0]]

    def slice1(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(),dest='ko')
          
            return translations.text
    result = str(slice1(slice_text))
    return result

def slice_2(text):
    global stext
    text=stext

    a = divmod(len(text[5000:]),1)
    if a[0] > 5000:
        slice_text=text[5000:10000]
    else:
        slice_text = text[5000:5000+a[0]]

    def slice2(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice2(slice_text)
    return result

def slice_3(text):
    global stext
    text=stext
    a = divmod(len(text[10000:]),1)
    if a[0] > 5000:
        slice_text=text[10000:15000]
    else:
        slice_text = text[10000:10000+a[0]]

    def slice3(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice3(slice_text)
    return result

def slice_4(text):
    global stext
    text=stext

    a = divmod(len(text[15000:]),1)
    if a[0] > 5000:
        slice_text=text[15000:20000]
    else:
        slice_text = text[15000:15000+a[0]]

    def slice4(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice4(slice_text)
    return result

def slice_5(text):

    global stext
    text=stext

    a = divmod(len(text[20000:]),1)
    if a[0] > 5000:
        slice_text=text[20000:25000]
    else:
        slice_text = text[15000:15000+a[0]]

    def slice5(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice5(slice_text)
    return result

def slice_6(text):

    global stext
    text=stext
    a = divmod(len(text[25000:]),1)
    if a[0] > 5000:
        slice_text=text[25000:30000]
    else:
        slice_text = text[25000:25000+a[0]]

    def slice6(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice6(slice_text)
    return result

def slice_7(text):
    global stext
    text=stext
    a = divmod(len(text[30000:]),1)
    if a[0] > 5000:
        slice_text=text[30000:35000]
    else:
        slice_text = text[30000:30000+a[0]]

    def slice7(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice7(slice_text)
    return result

def slice_8(text):
    global stext
    text=stext
    a = divmod(len(text[35000:]),1)
    if a[0] > 5000:
        slice_text=text[35000:40000]
    else:
        slice_text = text[35000:35000+a[0]]

    def slice8(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice8(slice_text)
    return result

def slice_9(text):
    global stext
    text=stext
    a = divmod(len(text[40000:]),1)
    if a[0] > 5000:
        slice_text=text[40000:45000]
    else:
        slice_text = text[40000:40000+a[0]]

    def slice9(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice9(slice_text)
    return result

def slice_10(text):
    global stext
    text=stext
    a = divmod(len(text[45000:]),1)
    if a[0] > 5000:
        slice_text=text[45000:50000]
    else:
        slice_text = text[45000:45000+a[0]]

    def slice10(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice10(slice_text)
    return result

def slice_11(text):
    global stext
    text=stext
    a = divmod(len(text[50000:]),1)
    if a[0] > 5000:
        slice_text=text[50000:55000]
    else:
        slice_text = text[50000:50000+a[0]]

    def slice11(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice11(slice_text)
    return result


def slice_12(text):
    global stext
    text=stext
    a = divmod(len(text[55000:]),1)
    if a[0] > 5000:
        slice_text=text[55000:60000]
    else:
        slice_text = text[55000:55000+a[0]]

    def slice12(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice12(slice_text)
    return result

def slice_13(text):
    global stext
    text=stext
    a = divmod(len(text[60000:]),1)
    if a[0] > 5000:
        slice_text=text[60000:65000]
    else:
        slice_text = text[60000:60000+a[0]]

    def slice13(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice13(slice_text)
    return result

def slice_14(text):
    global stext
    text=stext
    a = divmod(len(text[65000:]),1)
    if a[0] > 5000:
        slice_text=text[65000:70000]
    else:
        slice_text = text[65000:65000+a[0]]

    def slice14(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice14(slice_text)
    return result

def slice_15(text):
    global stext
    text=stext
    a = divmod(len(text[70000:]),1)
    if a[0] > 5000:
        slice_text=text[70000:75000]
    else:
        slice_text = text[70000:70000+a[0]]

    def slice15(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice15(slice_text)
    return result

def slice_16(text):
    global stext
    text=stext
    a = divmod(len(text[75000:]),1)
    if a[0] > 5000:
        slice_text=text[75000:80000]
    else:
        slice_text = text[75000:75000+a[0]]

    def slice16(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice16(slice_text)
    return result

def slice_17(text):
    global stext
    text=stext
    a = divmod(len(text[80000:]),1)
    if a[0] > 5000:
        slice_text=text[80000:85000]
    else:
        slice_text = text[80000:80000+a[0]]

    def slice17(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice17(slice_text)
    return result

def slice_18(text):
    global stext
    text=stext
    a = divmod(len(text[85000:]),1)
    if a[0] > 5000:
        slice_text=text[85000:90000]
    else:
        slice_text = text[85000:85000+a[0]]

    def slice18(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice18(slice_text)
    return result

def slice_19(text):
    global stext
    text=stext
    a = divmod(len(text[90000:]),1)
    if a[0] > 5000:
        slice_text=text[90000:95000]
    else:
        slice_text = text[90000:90000+a[0]]

    def slice19(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice19(slice_text)
    return result

def slice_20(text):
    global stext
    text=stext
    a = divmod(len(text[95000:]),1)
    if a[0] > 5000:
        slice_text=text[95000:100000]
    else:
        slice_text = text[95000:95000+a[0]]

    def slice20(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice20(slice_text)
    return result

def slice_21(text):
    global stext
    text=stext
    a = divmod(len(text[100000:]),1)
    if a[0] > 5000:
        slice_text=text[100000:105000]
    else:
        slice_text = text[100000:100000+a[0]]

    def slice21(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice21(slice_text)
    return result

def slice_22(text):
    global stext
    text=stext
    a = divmod(len(text[105000:]),1)
    if a[0] > 5000:
        slice_text=text[105000:110000]
    else:
        slice_text = text[105000:105000+a[0]]

    def slice22(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice22(slice_text)
    return result

def slice_23(text):
    global stext
    text=stext
    a = divmod(len(text[110000:]),1)
    if a[0] > 5000:
        slice_text=text[110000:115000]
    else:
        slice_text = text[110000:110000+a[0]]

    def slice23(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice23(slice_text)
    return result

def slice_24(text):
    global stext
    text=stext
    a = divmod(len(text[115000:]),1)
    if a[0] > 5000:
        slice_text=text[115000:120000]
    else:
        slice_text = text[115000:115000+a[0]]

    def slice24(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice24(slice_text)
    return result

def slice_25(text):
    global stext
    text=stext
    a = divmod(len(text[120000:]),1)
    if a[0] > 5000:
        slice_text=text[120000:125000]
    else:
        slice_text = text[120000:120000+a[0]]

    def slice25(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice25(slice_text)
    return result

def slice_26(text):
    global stext
    text=stext
    a = divmod(len(text[125000:]),1)
    if a[0] > 5000:
        slice_text=text[125000:130000]
    else:
        slice_text = text[125000:125000+a[0]]

    def slice26(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice26(slice_text)
    return result

def slice_27(text):
    global stext
    text=stext
    a = divmod(len(text[130000:]),1)
    if a[0] > 5000:
        slice_text=text[130000:135000]
    else:
        slice_text = text[130000:130000+a[0]]

    def slice27(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice27(slice_text)
    return result

def slice_28(text):
    global stext
    text=stext
    a = divmod(len(text[135000:]),1)
    if a[0] > 5000:
        slice_text=text[135000:140000]
    else:
        slice_text = text[135000:135000+a[0]]

    def slice28(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice28(slice_text)
    return result

def slice_29(text):
    global stext
    text=stext
    a = divmod(len(text[140000:]),1)
    if a[0] > 5000:
        slice_text=text[140000:145000]
    else:
        slice_text = text[140000:140000+a[0]]

    def slice29(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice29(slice_text)
    return result

def slice_30(text):
    global stext
    text=stext
    a = divmod(len(text[145000:]),1)
    if a[0] > 5000:
        slice_text=text[145000:150000]
    else:
        slice_text = text[145000:145000+a[0]]

    def slice30(slice_text):
            slice_text = slice_text.replace('\n','')
            encoded_string = slice_text.encode()
            byte_array = bytearray(encoded_string)
            translator = Translator(service_urls=[
                                        'translate.google.com',
                                        'translate.google.co.kr',
                                        ])
            translations = translator.translate(byte_array.decode(), dest='ko')
            return translations.text
    result = slice30(slice_text)
    return result

def total(request):
    global stext
    text= stext
    
    while True:
        if len(text[0:]) <= len(text) <= len(text[:5001]):
            return (slice_1(request))

        elif len(text[0:]) <= len(text) <= len(text[:10001]):
            return (slice_1(text),slice_2(text))
        
        elif len(text[0:]) <= len(text) <= len(text[:15001]):
            return (slice_1(text),slice_2(text),slice_3(text))
        
        elif len(text[0:]) <= len(text) <= len(text[:20001]):
            return (slice_1(text),slice_2(text),slice_3(text),slice_4(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:25001]):
            return (slice_1(text),slice_2(text),slice_3(text),slice_4(text),slice_5(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:30001]):
            return (slice_1(text),slice_2(text),slice_3(text),slice_4(text),slice_5(text),slice_6(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:35001]):
            return (slice_1(text),slice_2(text),slice_3(text),slice_4(text),slice_5(text),slice_6(text),slice_7(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:40001]):
            return (slice_1(text),slice_2(text),slice_3(text),slice_4(text),slice_5(text),slice_6(text),
                    slice_7(text),slice_8(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:45001]):
            return (slice_1(text),slice_2(text),slice_3(text),slice_4(text),slice_5(text),slice_6(text),
                    slice_7(text),slice_8(text),slice_9(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:50001]):
            return (slice_1(text),slice_2(text),slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),slice_10(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:55001]):
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),slice_10(text),slice_11(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:60001]):
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),
                    slice_10(text),slice_11(text),slice_12(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:65001]):
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),
                    slice_10(text),slice_11(text),slice_12(text),slice_13(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:70001]):
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),
                    slice_10(text),slice_11(text),slice_12(text),slice_13(text),slice_14(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:75001]):
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),
                    slice_10(text),slice_11(text),slice_12(text),slice_13(text),slice_14(text),slice_15(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:80001]):
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),
                    slice_10(text),slice_11(text),slice_12(text),slice_13(text),slice_14(text),slice_15(text),slice_16(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:85001]):
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),
                    slice_10(text),slice_11(text),slice_12(text),slice_13(text),slice_14(text),slice_15(text),slice_16(text),slice_17(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:90001]):
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),
                    slice_10(text),slice_11(text),slice_12(text),slice_13(text),
                    slice_14(text),slice_15(text),slice_16(text),slice_17(text),slice_18(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:95001]):
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),
                    slice_10(text),slice_11(text),slice_12(text),slice_13(text),
                    slice_14(text),slice_15(text),slice_16(text),slice_17(text),slice_18(text),slice_19(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:100001]):
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),
                    slice_10(text),slice_11(text),slice_12(text),slice_13(text),
                    slice_14(text),slice_15(text),slice_16(text),slice_17(text),slice_18(text),slice_19(text),slice_20(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:105001]):
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),slice_10(text),slice_11(text),slice_12(text),slice_13(text),
                    slice_14(text),slice_15(text),slice_16(text),slice_17(text),slice_18(text),
                    slice_19(text),slice_20(text),slice_21(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:110001]):
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),
                    slice_10(text),slice_11(text),slice_12(text),slice_13(text),
                    slice_14(text),slice_15(text),slice_16(text),slice_17(text),slice_18(text),
                    slice_19(text),slice_20(text),slice_21(text),slice_22(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:115001]):
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),
                    slice_10(text),slice_11(text),slice_12(text),slice_13(text),
                    slice_14(text),slice_15(text),slice_16(text),slice_17(text),slice_18(text),
                    slice_19(text),slice_20(text),slice_21(text),slice_22(text),slice_23(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:120001]):
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),
                    slice_10(text),slice_11(text),slice_12(text),slice_13(text),
                    slice_14(text),slice_15(text),slice_16(text),slice_17(text),slice_18(text),
                    slice_19(text),slice_20(text),slice_21(text),slice_22(text),slice_23(text),slice_24(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:125001]):
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),
                    slice_10(text),slice_11(text),slice_12(text),slice_13(text),
                    slice_14(text),slice_15(text),slice_16(text),slice_17(text),slice_18(text),
                    slice_19(text),slice_20(text),slice_21(text),slice_22(text),slice_23(text),slice_24(text),slice_25(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:130001]):
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),
                    slice_10(text),slice_11(text),slice_12(text),slice_13(text),
                    slice_14(text),slice_15(text),slice_16(text),slice_17(text),slice_18(text),
                    slice_19(text),slice_20(text),slice_21(text),slice_22(text),slice_23(text),slice_24(text),slice_25(text),
                    slice_26(text))
            
        elif len(text[0:]) <= len(text) <= len(text[:135001]):
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),
                    slice_10(text),slice_11(text),slice_12(text),slice_13(text),
                    slice_14(text),slice_15(text),slice_16(text),slice_17(text),slice_18(text),
                    slice_19(text),slice_20(text),slice_21(text),slice_22(text),slice_23(text),slice_24(text),slice_25(text),
                    slice_26(text),slice_27(text))
            
        elif len(text[0:])<= len(text) <= len( text[:140001]):
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),
                    slice_10(text),slice_11(text),slice_12(text),slice_13(text),
                    slice_14(text),slice_15(text),slice_16(text),slice_17(text),slice_18(text),
                    slice_19(text),slice_20(text),slice_21(text),slice_22(text),slice_23(text),slice_24(text),slice_25(text),
                    slice_26(text),slice_27(text),slice_28(text))
            
        elif len(text[0:])<= len(text) <= len(text[:145001]):
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),
                    slice_10(text),slice_11(text),slice_12(text),slice_13(text),
                    slice_14(text),slice_15(text),slice_16(text),slice_17(text),slice_18(text),
                    slice_19(text),slice_20(text),slice_21(text),slice_22(text),slice_23(text),slice_24(text),slice_25(text),
                    slice_26(text),slice_27(text),slice_28(text),slice_29(text))
            
        else :
            return (slice_1(text),slice_2(text),
                    slice_3(text),slice_4(text),slice_5(text),
                    slice_6(text),slice_7(text),slice_8(text),slice_9(text),
                    slice_10(text),slice_11(text),slice_12(text),slice_13(text),
                    slice_14(text),slice_15(text),slice_16(text),slice_17(text),slice_18(text),
                    slice_19(text),slice_20(text),slice_21(text),slice_22(text),slice_23(text),slice_24(text),
                    slice_25(text),slice_26(text),slice_27(text),slice_28(text),slice_29(text),slice_30(text))
    

def translate(request):
    global stext
    global totals
    text=stext
    if request=='GET':
        totals = total(text)
    else:
        totals = total(text)
           
    return render(request,'Summary/translate.html',{'totals':totals })





def enkr(request):
    global totals
    
    text = totals
    max = 500
    result = []
    if len(text) > 500:
        for i in range(len(text) // max):
            result.append(sentence(text[i*max:(i+1)*max]))
            result.append(' ')
        result.append(sentence(text[(i+1)*max:]))
        result = "".join(result)

    else:
        result.append(sentence(text))
        result = "".join(result)

    encode_title = urllib.parse.quote(string=f'{title}_summary.txt')

    file = open(f'media/{encode_title}', 'w', encoding="UTF-8")
    file.write(result)                # 파일에 문자열 저장
    file.close()                      # 파일 객체 닫기

    return render(request, 'Summary/result2.html', {'result': result})
    