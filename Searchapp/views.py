from django.shortcuts import render
import requests
# from django.http import HttpResponse
# import urllib.request as req
from bs4 import BeautifulSoup
from selenium import webdriver

# Create your views here.
def category(request):
    return render(request, 'Search/search_category.html', {})

def booksearch(request):
    return render(request, 'Search/booksearch.html')

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

def document(request):
    return render(request, 'Search/document.html')

def documentsearch(request):
    QUERY = request.POST['query']
    page = 0
    BASE_URL = f'http://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&query={QUERY}&queryText=&iStartCount={page}&iGroupView=5&icate=all&colName=bib_t&exQuery=&exQueryText=&order=/DESC&onHanja=false&strSort=RANK&pageScale=10&orderBy=&fsearchMethod=search&isFDetailSearch=N&sflag=1&searchQuery={QUERY}&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&resultKeyword={QUERY}&pageNumber=1&p_year1=&p_year2=&dorg_storage=&mat_type=&mat_subtype=&fulltext_kind=&t_gubun=&learning_type=&language_code=&ccl_code=&language=&inside_outside=&fric_yn=&image_yn=&regnm=&gubun=&kdc=&ttsUseYn='

    datas = []
    
    driver = webdriver.Chrome('Searchapp\\chromedriver.exe')
    
    response = requests.get(BASE_URL)
    dom = BeautifulSoup(response.text, "html.parser")

    for i in range(len(dom.select('li > div.cont > p.title > a'))):
        link = dom.select('li > div.cont > p.title > a')[i]['href']
        paper_url = "http://riss.or.kr" + link
        
        driver.get(paper_url)
        
        html = driver.page_source
        dom2 = BeautifulSoup(html, "html.parser")

        title = dom2.find("h3", "title")
        title_txt = title.get_text("", strip = True).split("=")
        title_kor = str(title_txt[0]).strip()
        if len(title_txt) >= 2:
            title_eng = str(title_txt[1]).strip()

        txt_box = []
        for text in dom2.find_all("div", "text"):
            txt = text.get_text("", strip = True)
            txt_box.append(txt)
            
        if dom2.select("#additionalInfoDiv > div > div:nth-child(1)")[0].text.strip()[:3] == "다국어":
            txt_kor = txt_box[3]
        else:
            txt_kor = txt_box[1]

        detail_box = []
        detail_info = dom2.select("#soptionview > div > div.thesisInfo > div.infoDetail.on > div.infoDetailL > ul > li > div > p")
        
        for detail in detail_info:
            detail_content = detail.get_text("", strip = True)
            detail_wrap = []
            detail_wrap.append(detail_content)
            detail_box.append(detail_wrap)
        
        for i in range(len(detail_box)):
            if dom2.select(f"#thesisInfoDiv > div.infoDetail.on > div.infoDetailL > ul > li:nth-child({i+1})")[0].text.strip()[:3] == "발행국":
                country = ",".join(detail_box[i]) 

        author = ",".join(detail_box[0])
        year = ",".join(detail_box[3])
        language = ",".join(detail_box[4])
            
        if len(title_txt) >= 2:
            datas.append({
                "국문 제목" : title_kor,
                "영문 제목" : title_eng,
                "저자" : author,
                "발행연도" : year,
                "작성언어" : language,
                "발행국(도시)" : country,
                "국문 초록" : txt_kor,
                "링크" : paper_url,
                
            })
        else:
            datas.append({
                "국문 제목" : title_kor,
                "영문 제목" : "",
                "저자" : author,
                "발행연도" : year,
                "작성언어" : language,
                "발행국(도시)" : country,
                "국문 초록" : txt_kor,
                "링크" : paper_url,
            })
      
    driver.quit()
    
    doc_1 = []
    doc_2 = []
    doc_3 = []
    doc_4 = []
    doc_5 = []
    doc_6 = []
    doc_7 = []
    doc_8 = []
    
    for i in range(len(datas)):
        doc_1.append(datas[i]['국문 제목'])
        doc_2.append(datas[i]['영문 제목'])
        doc_3.append(datas[i]['저자'])
        doc_4.append(datas[i]['발행연도'])
        doc_5.append(datas[i]['작성언어'])
        doc_6.append(datas[i]['발행국(도시)'])
        doc_7.append(datas[i]['국문 초록'])
        doc_8.append(datas[i]['링크'])
        
    df = {'doc1' : doc_1[:10],
          'doc2' : doc_2[:10],
          'doc3' : doc_3[:10],
          'doc4' : doc_4[:10],
          'doc5' : doc_5[:10],
          'doc6' : doc_6[:10],
          'doc7' : doc_7[:10],
          'doc8' : doc_8[:10]}
    
    return render(request, 'Search/documentsearch.html', df)