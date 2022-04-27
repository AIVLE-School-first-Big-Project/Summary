from django.http import HttpResponse
from django.shortcuts import render
from .summary import sentence
from .textrank import textrank

# Create your views here.
def summary(request):
    return render(request, 'Summary/summary.html', {})

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