from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserForm, CustomUserChangeForm
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

def profile_update(request):
    username = request.user.first_name
    
    if request.method == 'GET':
        context = {'currentname': username}
        return render(request, 'Main/profile_update.html', context)
    elif request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            u = form.save(commit=False)
            current = User.objects.get(id=request.user.id)
            
            user = request.POST.get('first_name')
            if user:
                u.first_name = user
            else:
                u.first_name = current.first_name
            
            u.save()
            
            return redirect('Mainapp:mypage')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'Main/profile_update.html')