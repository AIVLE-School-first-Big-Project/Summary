from django.http import HttpResponse
from django.shortcuts import render
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
def summary(request):
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
    
    files = File.objects.all()
    
    return render(request, 'Summary/summary.html', context={'files':files})

def text(request):
    return render(request, 'Summary/text.html')

def textsummary(request):
    text = request.POST.get('content')
    
    sum_text = sentence(text)
    
    keyword = textrank(text)
    
    return render(request, 'Summary/textsummary.html', {'sum_text' : sum_text, 'keyword' : keyword })

def upload1(request):
    if request.method == 'POST':
        
        upload_file = request.FILES.get('file')
        name = upload_file.name
        
        if(name.find("txt") > 0):
            with open(name, 'wb') as file:
                for chunk in upload_file.chunks():
                    file.write(chunk)
                
            with open(name, encoding = 'utf-8') as file:
                text = file.readlines()
        
            text = [line.rstrip('\n') for line in text]
            text = text[0]
            
            os.remove(name)
            
            # sum_text = sentence(text)
            
            # keyword = textrank(text)
            
            # keyword = " ".join(result)
            
            # return HttpResponse('파일 이름 : %s<br>파일 크기 : %s<br><br>파일 전문 : %s<br><br>파일 요약본 : %s<br><br>핵심어 10개 : %s' % (name, size, text, sum_text, keyword))
            return HttpResponse('전문<br> %s' % (text))
            
        elif(name.find("pdf") > 0):
            with open(name, 'wb') as file:
                for chunk in upload_file.chunks():
                    file.write(chunk)
                    
            text = extract_text(name)
            text = text.replace('\n', ' ')
            
            # PDF 전문추출 및 요약
            # max = 500
            # result = []
            # if len(text) > 500:
            #    for i in range(len(text) // max):
            #         result.append(sentence(text[i*max:(i+1)*max]))
            #         result.append('\n')
            #     result.append(sentence(text[(i+1)*max :]))
            # else:
            #     result.append(sentence(text))
            # result = "\n".join(result)
            
            # return HttpResponse('전문 <br>%s<br><br><br><br>요약본<br>%s' %(text, result))
            
            os.remove(name)
            
            return HttpResponse('전문<br> %s' %(text))
        
        elif(name.find("docx") > 0):
            with open(name, 'wb') as file:
                for chunk in upload_file.chunks():
                    file.write(chunk)
            
            doc = Document(name)
            text = []
            
            for p in doc.paragraphs:
                text.append(p.text)
            
            text = "\n".join(text)
            
            os.remove(name)
            
            return HttpResponse('전문<br>%s' %(text))
        
        elif(name.find("png") > 0 or name.find("PNG") or name.find("ipg") or name.find("JPG")):
            with open(name, 'wb') as file:
                for chunk in upload_file.chunks():
                    file.write(chunk)
            
            text = pytesseract.image_to_string(name, lang = 'kor+eng', config = '-c perserve_interword_spaces=1 --psm 4')
            text = text.replace('\n', ' ')
            text.strip()
            
            os.remove(name)
            
            return HttpResponse('이미지 추출<br>%s' %(text))
                
        else:
            message = "파일형식이 잘못되었습니다."
            return HttpResponse('%s' % (message) )
        
    return render(request, 'Summary/upload1.html')

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
