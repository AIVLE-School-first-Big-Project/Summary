from django.contrib import admin
from .models import Board
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Board)
class BoardAdmin(SummernoteModelAdmin):
    summernote_fields = ('b_contents',)
    list_display =(
        'b_no',
        'b_title',
        'b_date',
        'view',
        'writer',

    )
    list_display_links = list_display

# Register your models here.
