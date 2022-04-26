from django.shortcuts import render
import requests
from django.http import HttpResponse
import urllib.request as req
from bs4 import BeautifulSoup
# Create your views here.
def category(request):
    return render(request, 'Search/search_category.html', {})

def index(request):
    return render(request, 'Search/index.html')

def book(request):
    search = request.POST.get('search')
    response = requests.get(f'https://search.kyobobook.co.kr/web/search?vPstrKeyWord={search}')
    
    dom = BeautifulSoup(response.text, 'html.parser')
    
    elements = dom.select("td.detail > div.title > a > strong")
    prices = dom.select("td.price > div.org_price")
    imgs = dom.select("td.image > div.cover > a > img")
    authors = dom.select("td.detail > div.author > a:nth-child(1)")
    sources = dom.select("td.detail > div.title > a ")
    
    elementlists=[]
    pricelists=[]
    imglists=[]
    authorlists=[]
    sourcelists=[]

    for i in range(len(elements)):
        elementlists.append(elements[i].text.strip())


    for j in range(len(prices)):
        pricelists.append(prices[j].text.strip())

    for k in range(len(imgs)):
        imglists.append(imgs[k].get("src"))
    
    for a in range(len(authors)):
        authorlists.append(authors[a].text.strip())
    
    for b in range(len(sources)):
        sourcelists.append(sources[b].get("href"))

    
    
    df={'title': elementlists[:10],
         'price': pricelists[:10],
         'img': imglists[:10],
         'author': authorlists[:10],
         "source": sourcelists[:10]}
    
    
    return render(request, 'Search/book.html', df)