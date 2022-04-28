from django.http import HttpResponse
from django.shortcuts import render
from .summary import sentence
from .textrank import textrank
from Mainapp.models import File
from django.contrib.auth.models import User

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
        size = upload_file.size
        
        if(name.find("txt") > 0):
            with open(name, 'wb') as file:
                for chunk in upload_file.chunks():
                    file.write(chunk)
                
            with open(name, encoding = 'utf-8') as file:
                text = file.readlines()
        
            text = [line.rstrip('\n') for line in text]
            text = text[0]
            
            sum_text = sentence(text)
            
            keyword = textrank(text)
            
            return HttpResponse('파일 이름 : %s<br>파일 크기 : %s<br><br>파일 전문 : %s<br><br>파일 요약본 : %s<br><br>핵심어 10개 : %s, %s, %s, %s, %s, %s, %s, %s, %s, %s'
                                % (name, size, text, sum_text, keyword[0], keyword[1], keyword[2], keyword[3], keyword[4], keyword[5], keyword[6], keyword[7], keyword[8], keyword[9]))
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
        if uploadedFile:  
            with open('media/Uploaded Files/%s' % fileTitle, 'wb') as file:
                for chunk in uploadedFile.chunks():
                    file.write(chunk)
        
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