from django.shortcuts import render

# Create your views here.
def summary(request):
    return render(request, 'Summary/summary.html', {})