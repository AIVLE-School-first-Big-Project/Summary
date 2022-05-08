from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate
from .forms import UserForm, CustomUserChangeForm
# from django.contrib.auth.models import User
from Mainapp.models import Board, Review
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

# Create your views here.
def main(request):
    return render(request, 'Main/main.html', {})

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        # print('d')
        if form.is_valid():
            u = form.save(commit=False)
            # id
            # username = form.cleaned_data.get('username')
            form.cleaned_data.get('username')
            # 비밀번호
            # raw_password = form.cleaned_data.get('password1')
            form.cleaned_data.get('password1')
            # 닉네임
            # nickname = form.cleaned_data.get('first_name')
            form.cleaned_data.get('first_name')
            
            u.save()
            # user = authenticate(username=username, password=raw_password, first_name=nickname)
            # login(request, user)
            return redirect('Mainapp:login')
    else:
        form = UserForm()
    return render(request, 'Main/signup.html', {'form': form})

def mypage(request):
    return redirect('Mainapp:my_category', table='article')
    
def profile_update(request):
    username = request.user.first_name
    context = {'currentname': username}
    
    if request.method == 'GET':
        return render(request, 'Main/profile_update.html', context)
    elif request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            u = form.save(commit=False)
            # current = User.objects.get(id=request.user.id)
            
            user = request.POST.get('first_name')
            if user:
                u.first_name = user
            else:
                messages.warning(request, '변경할 닉네임을 입력해 주세요.')
                return render(request, 'Main/profile_update.html', context)
            
            u.save()
            return redirect('Mainapp:mypage')
            
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'Main/profile_update.html')

def my_category(request, table):
    # user 고유 id
    user = request.user.id
    
    # 작성한 글
    if table == 'article':
        my_list = Board.objects.filter(user_id=user).order_by('-b_date')
    elif table == 'comment':
        # 본인이 쓴 댓글의 게시글 번호 뽑아오기
        comments_set = Review.objects.filter(user_id=user).values('b_no')

        # 쿼리셋 => 리스트(딕셔너리)
        comments = list(comments_set)
        
        # 각 게시글 번호를 리스트에 넣기
        boards = []
        for com in comments:
            boards.append(list(com.values()))
            
        # 2차원 리스트를 1차원 리스트로 변환
        boards = sum(boards, [])
        
        # b_no에 맞는 조건 & 게시글 뽑기
        q = Q()
        for b in boards:
            q.add(Q(b_no=b), q.OR)
        
        my_list = Board.objects.filter(q).order_by('-b_date')
    
    paginator = Paginator(my_list, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    return render(request, 'Main/mypage.html', {'articles' : my_list, 'posts': posts, 'category': table})

def search(request):
    print('실행')
    user = request.user.id
    search_boards = Board.objects.filter(user_id=user).order_by('-b_date')
    q=request.GET.get('q','')
    print('------------------',q)
    
    if q:
        print('if실행')
        list_board=search_boards.filter(
            Q(b_title__icontains = q) | # 제목
            Q(b_contents__icontains = q) | # 내용
            Q(writer__icontains = q) # 글쓴이
        )

        paginator=Paginator(list_board,9)
        page=request.GET.get('page')
        search_posts=paginator.get_page(page)
        return render(request,'Main/mypage.html', {'posts' : search_posts, 'q' : q, 'category': 'article'})

    else:
        print('else실행')
        messages.warning(request, '검색할 텍스트를 입력해 주세요.')
        return redirect('Mainapp:my_category', table='article')