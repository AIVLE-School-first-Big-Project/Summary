from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserForm
from django.contrib.auth.models import User

# Create your views here.
def main(request):
    return render(request, 'Main/main.html', {})

# def search_category(request):
#     return render(request, 'Main/search_category.html', {})

# def login(request):
#     return render(request, 'Main/login.html', {})

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        # print('d')
        if form.is_valid():
            u = form.save(commit=False)
            # id
            username = form.cleaned_data.get('username')
            # 비밀번호
            raw_password = form.cleaned_data.get('password1')
            # 닉네임
            nickname = form.cleaned_data.get('first_name')
            
            u.save()
            user = authenticate(username=username, password=raw_password, first_name=nickname)
            # login(request, user)
            return redirect('Mainapp:login')
    else:
        form = UserForm()
    return render(request, 'Main/signup.html', {'form': form})

def mypage(request):
    return render(request, 'Main/mypage.html', {})