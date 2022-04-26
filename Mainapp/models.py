from django.db import models

# Create your models here.
class Board(models.Model):
    b_no=models.AutoField(primary_key=True)
    b_date=models.DateTimeField(null=False,auto_now_add=True)
    b_contents=models.TextField(null=False)
    b_title=models.CharField(max_length=100,null=False)
    view=models.IntegerField(null=False,default=0)
    writer=models.CharField(max_length=50,null=False)
    comment_cnt=models.IntegerField(null=False,default=0)
    username=models.CharField(max_length=50,null=False)

    class Meta:
        db_table='Board'
        managed=False

class Review(models.Model):
    r_no=models.AutoField(primary_key=True)
    b_no=models.ForeignKey('Board',on_delete=models.CASCADE,db_column='b_no')
    r_date=models.DateTimeField(null=False,auto_now_add=True)
    r_contents=models.TextField(null=False)
    writer=models.CharField(max_length=50,null=False)

    class Meta:
        db_table='Review'
        managed=False

class Pile(models.Model):
    p_no=models.AutoField(primary_key=True)
    p_content=models.TextField(null=False)
    p_date=models.DateTimeField(null=False,auto_now_add=True)
    writer=models.CharField(max_length=50,null=False)

    class Meta:
        db_table='Pile'
        managed=False

class Image(models.Model):
    i_no=models.AutoField(primary_key=True)
    image_contents=models.TextField(null=False)
    image_name=models.CharField(max_length=100,null=False)

    class Meta:
        db_table='Image'
        managed=False