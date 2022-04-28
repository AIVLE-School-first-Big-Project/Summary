from certifi import contents
from django.shortcuts import render,redirect
from . forms import BoardWriteForm
from Mainapp.models import Board, Review
from datetime import date, datetime, timedelta
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User

# Create your views here.
# def board_list(request):
#     login_session = request.session.get('login_session','')
#     context={'login_session': login_session}

#     return render(request,'Board/board_list.html',context)

def board_write(request):
    login_session = request.session.get('login_session','')
    context={'login_session': login_session}

    if request.method=='GET':
        write_form = BoardWriteForm()
        context['forms']= write_form
        return render(request,'Board/board_write.html',context)

    elif request.method == 'POST':
        write_form = BoardWriteForm(request.POST)

        if write_form.is_valid():
            writer=request.user.first_name
            user_id = request.user.id
            me = User.objects.get(id = user_id)
            # print(me)
            # board = Board.objects.create(username=me, b_title=write_form.b_title, b_contents=write_form.b_contents, writer=writer)
            board = Board(
                b_title=write_form.b_title,
                b_contents=write_form.b_contents,
                writer=writer,
                user_id = me,
            )
            board.save()
            return redirect('Board:board_list')
        else :
            context['forms']= write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error']=value
            return render(request, 'Board/board_write.html',context)

    # return render(request,'Board/board_write.html',context)

def detail_board(request,b_no):
    board_detail=Board.objects.get(b_no=b_no)
    comment_list=Review.objects.filter(b_no=b_no)
    comment_cnt=len(comment_list)

   

    context={
        'board_detail' : board_detail,
        'comment_list' : comment_list,
        'comment_cnt' : comment_cnt,

    }
    response = render(request,'Board/detail_board.html',context)
    #조회수
    expire_date, now = datetime.now(),datetime.now()
    expire_date+=timedelta(days=1)
    expire_date=expire_date.replace(hour=0,minute=0,second=0,microsecond=0)
    expire_date-=now
    max_age=expire_date.total_seconds()

    cookie_value=request.COOKIES.get('hitboard','_')

    if f'_{b_no}_' not in cookie_value:
        cookie_value+=f'{b_no}_'
        response.set_cookie('hitboard',value=cookie_value,max_age=max_age,httponly=True)
        board_detail.view +=1
        board_detail.save()

    return response


def board_list(request):
    boards=Board.objects.all()
    #모든 글들을 대상으로
    tb_list=Board.objects.all().order_by('-b_date')
    #블로그 객체 9개를 한페이지로 자르기
    paginator= Paginator(tb_list,9)
    #request된 페이지가 뭔지를 알아내고 (request페이지를 변수에 담아냄)
    page=request.GET.get('page')
    #request된 페이지를 얻어온 뒤 return 
    posts= paginator.get_page(page)
    return render(request , 'Board/board_list.html',{'boards':boards,'posts':posts})


def comment(request):
    if request.method=='POST':
        r_contents=request.POST.get('r_contents')
        b_no=request.POST.get('b_no')
        print(b_no)
        if r_contents:
            try:
                print(r_contents)
                writer=request.user.first_name

                print(writer)
                
                comment=Review.objects.create(b_no=b_no,r_contents=r_contents,writer=writer)
                comment.save()

                print(comment)

                board=Board.objects.get(b_no=b_no)
                board.comment_cnt=board.comment_cnt+1
                board.save()

                print(board.comment_cnt)

                return redirect('Board:detail_board',b_no)
            except:
                return redirect('Board:board_list',b_no)
        else:
            return redirect('Board:detail_board',b_no)
    else:
        return redirect('Board:detail_board',b_no)

def comment_delete(request,b_no,r_no):
    try:
        comment=Review.objects.get(r_no=r_no)
        comment.delete()

        board=Board.objects.get(b_no=b_no)
        board.comment_cnt=board.comment_cnt-1
        board.save()

        return redirect('Board:detail_board',b_no)

    except:
        return redirect('Board:detail_board',b_no)

def comment_updateurl(request,b_no,r_no):
    request.session['update_r_no']= r_no
    print(request.session['update_r_no'])

    return redirect('Board:detail_board',b_no)

def comment_update(request,r_no):
    if request.method == 'POST':
        comment=Review.objects.get(r_no=r_no)

        r_contents= request.POST.get('r_contents')
        b_no=request.POST.get('b_no')
        r_date=datetime.now()

        if r_contents:
            try:
                comment.r_contents=r_contents
                comment.r_date=r_date
                comment.save()

                del request.session['update_r_no']
                return redirect('Board:detail_board',b_no)
            except:
                return redirect('Board:detail_board',b_no)
        else:
            return redirect('Board:detail_board',b_no)