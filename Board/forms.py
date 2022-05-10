from django import forms
from Mainapp.models import Board
from django_summernote.widgets import SummernoteWidget

class BoardWriteForm(forms.ModelForm):
    b_title = forms.CharField(
        label='글 제목',
        widget=forms.TextInput(
            attrs={
                'placeholder': '글 제목',
            }),
    )

    b_contents = forms.CharField(widget=SummernoteWidget())
    filed_order=['b_title','b_contents']
    
    class Meta:
        model=Board
        fields = [
            'b_title','b_contents'
        ]
        widgets={
            'b_contents' : SummernoteWidget()
        }
        
    def clean(self):
        cleaned_data = super().clean()

        b_title= cleaned_data.get('b_title','')
        b_contents=cleaned_data.get('b_contents','')

        if b_title == '':
            self.add_error('b_title','글 제목을 입력하세요.')
        elif b_contents == '':
            self.add_error('b_contents','글 내용을 입력하세요.')
        else:
            self.b_title=b_title
            self.b_contents=b_contents
