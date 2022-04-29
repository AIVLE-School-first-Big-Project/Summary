from django.http import HttpResponse
from django.shortcuts import render
from pkg_resources import set_extraction_path
from .summary import sentence
from .textrank import textrank
from Mainapp.models import File
from django.contrib.auth.models import User
import pdfminer
from pdfminer.high_level import extract_text
from docx import Document
import pytesseract
import os

# Create your views here.

global stext

def summary(request):
    
    global stext
    
    if request.method == 'POST':
        # Fetching the form data
        uploadedFile = request.FILES['uploadedFile']
        fileTitle = uploadedFile.name
        writer=request.user.first_name
        user_id = request.user.id
        me = User.objects.get(id = user_id)
        
        # Saving the information in the database
        file = File(
            f_title = fileTitle,
            uploadedFile = uploadedFile,
            f_writer=writer,
            user_id = me,
        )
        
        file.save()
        
        if(fileTitle.find("txt") > 0) or fileTitle.find("TXT") > 0:
            with open(fileTitle, 'wb') as file:
                for chunk in uploadedFile.chunks():
                    file.write(chunk)
                
            with open(fileTitle, encoding = 'utf-8') as file:
                text = file.readlines()
        
            text = [line.rstrip('\n') for line in text]
            text = text[0]
            
            os.remove(fileTitle)
            stext = text
            return render(request, 'Summary/result.html', {'text' : text})            
            
        elif(fileTitle.find("pdf") > 0) or fileTitle.find("PDF") > 0:
            with open(fileTitle, 'wb') as file:
                for chunk in uploadedFile.chunks():
                    file.write(chunk)
                        
            text = extract_text(fileTitle)
            text = text.replace('\n', ' ')
                
            os.remove(fileTitle)
            stext = text
            
            return render(request, 'Summary/result.html', {'text' : text})
        
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
            return render(request, 'Summary/result.html', {'text' : text})        
            
        elif(fileTitle.find("png") > 0 or fileTitle.find("PNG") or fileTitle.find("ipg") or fileTitle.find("JPG")):
            with open(fileTitle, 'wb') as file:
                for chunk in uploadedFile.chunks():
                    file.write(chunk)
                
            text = pytesseract.image_to_string(fileTitle, lang = 'kor+eng', config = '-c perserve_interword_spaces=1 --psm 4')
            text = text.replace('\n', ' ')
            text.strip()
                
            os.remove(fileTitle)
            stext = text
            return render(request, 'Summary/result.html', {'text' : text})
                    
        else:
            message = "파일형식이 잘못되었습니다."
            return HttpResponse('%s' % (message) )
    
    files = File.objects.all()
    
    return render(request, 'Summary/summary.html', context={'files':files})

def result2(request):
    
    global stext
    
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
    
    return render(request, 'Summary/result2.html', {'result' : result})

def text(request):
    return render(request, 'Summary/text.html')

def textsummary(request):
    text = request.POST.get('content')
    
    sum_text = sentence(text)
    
    keyword = textrank(text)
    
    return render(request, 'Summary/textsummary.html', {'sum_text' : sum_text, 'keyword' : keyword })

def uploadFile(request):
    if request.method == 'POST':
        # Fetching the form data
        # fileTitle = request.POST['fileTitle']
        uploadedFile = request.FILES['uploadedFile']
        fileTitle = uploadedFile.name
        writer=request.user.first_name
        user_id = request.user.id
        me = User.objects.get(id = user_id)
        
        # Save File
        # if uploadedFile:  
        #     with open('media/Uploaded Files/%s' % fileTitle, 'wb') as file:
        #         for chunk in uploadedFile.chunks():
        #             file.write(chunk)
        
        # Saving the information in the database
        file = File(
            f_title = fileTitle,
            uploadedFile = uploadedFile,
            f_writer=writer,
            user_id = me,
        )
        
        file.save()
    
    # files = File.objects.all()
    
    return render(request, 'Summary/summary.html')

def ajax_upload(request):
    if request.method == 'POST':
        # uploadedFile = request.POST.get('uploadedFile')
        # fileTitle = request.POST.get('fileTitle')
        # # fileTitle = uploadedFile.name
        # writer=request.user.first_name
        # user_id = request.user.id
        # me = User.objects.get(id = user_id)
        file = request.POST.get('file')
    
    return render(request, 'Summary/summary.html', context={'file':file})
