from certifi import contents
from django.shortcuts import render,redirect
from . forms import BoardWriteForm
from Mainapp.models import Board

# Create your views here.
def board_list(request):
    login_session = request.session.get('login_session','')
    context={'login_session': login_session}

    return render(request,'Board/board_list.html',context)

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
            board=Board(
                b_title=write_form.b_title,
                b_contents=write_form.b_contents,
                writer=writer,
            )
            board.save()
            return redirect('mypage/')
        else :
            context['forms']= write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error']=value
            return render(request, 'Board/board_write.html',context)

    return render(request,'Board/board_write.html',context)
