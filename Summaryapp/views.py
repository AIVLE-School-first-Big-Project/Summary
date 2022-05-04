from base64 import encode
from urllib import response
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from pkg_resources import set_extraction_path
from .summary import sentence
from .textrank import textrank
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

def summary(request):
    
    global stext
    global title

    if request.method == 'POST':
        # Fetching the form data
        uploadedFile = request.FILES.get('uploadedFile')
        if uploadedFile:
            fileTitle = uploadedFile.name
            writer=request.user.first_name
            user_id = request.user.id
            me = User.objects.get(id = user_id)
            
            if(fileTitle.find("txt") > 0) or fileTitle.find("TXT") > 0:
                with open(fileTitle, 'wb') as file:
                    for chunk in uploadedFile.chunks():
                        file.write(chunk)
                    
                with open(fileTitle, encoding = 'utf-8') as file:
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
                
            elif(fileTitle.find("png") > 0 or fileTitle.find("PNG") or fileTitle.find("ipg") or fileTitle.find("JPG")):
                with open(fileTitle, 'wb') as file:
                    for chunk in uploadedFile.chunks():
                        file.write(chunk)
                    
                text = pytesseract.image_to_string(fileTitle, lang = 'kor+eng', config = '-c perserve_interword_spaces=1 --psm 4')
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
                f_title = fileTitle,
                uploadedFile = uploadedFile,
                f_writer=writer,
                user_id = me,
            )
            
            file.save()
            title = fileTitle.split('.')[0]
            
            return render(request, 'Summary/result.html', {'text' : stext})
        
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
        result.append(sentence(text[(i+1)*max :]))
        result = "".join(result)
        
    else:
        result.append(sentence(text))
        result = "".join(result)
    
    encode_title = urllib.parse.quote(string=f'{title}_summary.txt')
    
    file = open(f'media/{encode_title}', 'w', encoding="UTF-8")
    file.write(result)                # 파일에 문자열 저장
    file.close()                      # 파일 객체 닫기
    
    return render(request, 'Summary/result2.html', {'result' : result})

def downloadFile(request):
    global title
    global encode_title
    
    file_path = os.path.abspath('media/')
    file_name = encode_title
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_name, 'rb'),
                            content_type='text/plain')
    response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % file_name
    
    return response