from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'Main/main.html', {})

# def search_category(request):
#     return render(request, 'Main/search_category.html', {})

def login(request):
    return render(request, 'Main/login.html', {})

def signup(request):
    return render(request, 'Main/signup.html', {})

def mypage(request):
    return render(request, 'Main/mypage.html', {})