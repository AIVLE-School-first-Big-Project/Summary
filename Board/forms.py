from django import forms
from matplotlib import widgets
from .models import Board
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

class BoardWriteForm(forms.ModelForm):
    class BoardWriteForm(forms.ModelForm):
        title= forms.CharField(
            lable='글 제목',
            widget=forms.TextInput(
                attrs={
                    'placeholder' : '게시글 제목'
                }),
            required=True,
        )

        contents = SummernoteTextField()

        field_order = [
            'b_title',
            'b_contents',
        ]
    class Meta:
        model=Board
        fields=[
            'b_title',
            'b_contents',

        ]
        widgets={
            'b_contents' : SummernoteWidget()
        }
    def clean(self):
        cleaned_data=super.clean()
        title = cleaned_data.get('b_title','')
        contents = cleaned_data.get('b_contents','')

        if title == '':
            self.add_error('b_title','글 제목을 입력하세요.')
        elif contents == '':
            self.add_error('b_contents','글 내용을 입력하세요.')

        else:
            self.title = title
            self.contents = contents
