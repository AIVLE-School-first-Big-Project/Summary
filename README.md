<br>

# 📑 SOWS : Summary of Web Service
> 2022.04.11 ~ 2022.05.12 [17조] KT AIVLE AI 전남/전북1반 1조 빅프로젝트<br>
>  *'SOWS'는 복잡한 문서를 간단하게 요약해주는 서비스입니다.*

<br>

### 조원 소개
> 임채걸(조장) 김경준 박민지 안지예 조훈근

<br>

[1. 개발 배경 및 목적](#1-개발-배경-및-목적)

[2. 서비스 플로우](#2-서비스-플로우)

[3. DB 설계](#3-db-설계)

[4. 기능](#4-기능)

[5. 개발 환경](#5-개발-환경)

<br>

***

<br>

## 1. 개발 배경 및 목적
> 🤔 학부 전공 시험이나 자격증 시험을 앞두고 방대한 공부 양에 시작도 하기 전부터 맥이 빠졌던 경험<br> 🤔 기사는 읽고 싶은데 잘 읽히지 않았던 경험 <br> 🤔 영문 논문에 난처했던 경험 <br> 🤔 회의 내용을 일일이 타이핑하기 귀찮았던 경험 <br> 🤔 다른 사람들과 소통하면서 공부하고 싶었던 경험 <br>이러한 경험들을 바탕으로 **SOWS**를 개발하게 되었습니다.

<br>

💡 요약, 번역, 검색, 음성 기록을 한 사이트에서 제공하는 서비스

<!-- 문서 파일을 읽어 요약해주는 서비스 -->

<!-- - KT AIVLE 강의를 진행하면서 실습 하나하나에 여러가지 에러 발생 -->

<br>

- `기존 문서 요약 서비스`
  - 텍스트나 링크를 입력 받아 요약해주는 서비스는 有
  <br>⇒ 업로드한 문서를 요약해주는 서비스는 無
  - 텍스트 수와 문장 수 제한 有

 
<br>

- `SOWS`
  - 문서 파일을 업로드하고, 해당 문서의 텍스트를 읽어 들임
    - pdf 파일 뿐만 아니라 docx, txt, image(jpeg, png) 파일도 가능
  - 한국어에 특화된 요약 결과를 제공
  - 영문 파일은 국문으로 번역 가능

<br>

## 2. 서비스 플로우
<img src="https://velog.velcdn.com/images/jiyeah3108/post/3d88ab53-f995-44eb-9668-2740b239f900/image.png" width="740" height="400">

<br>


## 3. DB 설계
  - `ERD`
  <img src="https://velog.velcdn.com/images/jiyeah3108/post/c40b3c20-8376-4062-81ae-f5a0301c92d8/image.png" width="740" height="350">



<br>

## 4. 기능
<details>
  <summary>메인 화면</summary>
   <div markdown="1">       
     <br>
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/d7288e97-9225-401e-a85e-8f2d1b06325d/image.PNG" width="740" height="400">
     <br>
     <text>⇒ 로그인, 요약, 검색, 게시판, 음성 기록을 한 눈에 확인하고 이동할 수 있는 페이지</text>
   </div>
 </details>

 <details>
    <summary><strong>1) 회원가입 및 로그인</strong></summary>
        <div markdown="1">  
            <h3>📝 회원가입</h3>
            <img src="https://velog.velcdn.com/images/jiyeah3108/post/a255f4b2-894d-4363-844d-c01821549450/image.PNG" width="740" height="400">
            <h3>🔓 로그인</h3>
            <img src="https://velog.velcdn.com/images/jiyeah3108/post/6d02986d-15b3-49ba-a3e4-2f44e8d67f5c/image.PNG" width="740" height="400">
            <br>
            <text>⇒ django 내장 모듈을 사용하여 회원가입, 로그인, 로그아웃 구현</text>
        </div>
</details>
 
 <details>
  <summary><strong>2) 요약 및 번역</strong></summary>
   <div markdown="1"> 
    <br>
     <h3>파일 업로드</h3>
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/10a2e55c-e0db-4a2d-8de7-3000159504d4/image.PNG" width="740" height="400">
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/cf6f8322-eb06-4f67-b57b-5a86b343c4ef/image.PNG" width="740" height="400">
    <br>
     <text>⇒ 파일 업로드 : Drag & Drop이나 업로드 버튼을 눌러 파일 업로드 가능<br>업로드 가능 파일 : PDF, Word, txt, img</text>
     <h3>파일 텍스트</h3>
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/4533711f-154f-41dc-b66a-c60451d978bd/image.PNG" width="740" height="400">
    <br> 
    <text>⇒ 사용자가 업로드한 파일의 텍스트 전문 / 번역하거나 요약 가능 <br> KoBERT로 요약 기능을 구현했기 때문에 영문 파일인 경우 한글 번역을 한 후 요약하는 것을 권장</text>
     <h3>번역</h3>
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/37036603-d159-478e-af20-93c15dc2de7a/image.PNG" width="740" height="400">
    <br> 
    <text>⇒ 영문을 국문으로 번역한 텍스트 전문(Google Translate API 이용) <br> 요약 버튼을 눌러 요약 가능</text>
     <h3>요약</h3>
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/9379616f-5dbc-4ab7-9560-3f4d8bcd4909/image.PNG" width="740" height="400">
     <br>
     <text>⇒ 요약한 결과물<br>다운로드 버튼을 눌러 요약한 결과물을 txt 파일로 다운로드 가능</text>
   </div>
 </details>
 
 <details>
  <summary><strong>3) 검색(논문 / 도서)</strong></summary>
   <div markdown="1">
     <h3>검색 카테고리</h3> 
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/98338dea-f993-453f-afd9-a8a54ecc0fdc/image.PNG" width="740" height="400">
    <br>
     <text>⇒ 메인 화면에서 검색 버튼을 누르면 이동하는 페이지<br>논문 검색과 도서 검색을 할 수 있음</text>
     <h3>🔎 논문 검색</h3> 
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/3e5c2300-78cd-4007-98be-d50b4bc29640/image.PNG" width="740" height="400">
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/e0c53e8f-de97-4e13-ad8d-e1368e1b052d/image.PNG" width="740" height="400">
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/69bffbc6-2a9e-4c8e-99a0-80d2644452f6/image.PNG" width="740" height="400">
    <br>
     <text>⇒ Selenium을 이용하여 RISS 크롤링<br>검색된 논문 결과와 각 논문의 초록을 확인할 수 있음</text>
     <h3>🔎 도서 검색</h3> 
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/c0ce3371-601f-46be-ab25-af3d7d6760f2/image.PNG" width="740" height="400">
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/498dae76-5d14-477a-9db8-41979bd057ea/image.PNG" width="740" height="400">
    <br>
     <text>⇒ 교보문고를 크롤링한 결과를 확인할 수 있으며 바로가기를 통해 서점 링크로 이동 가능</text>
   </div>
 </details>
 
 <details>
  <summary><strong>4) 음성 기록</strong></summary>
   <div markdown="1">  
   <br>     
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/65ba59a3-3cb7-47d9-835f-c99699db083f/image.PNG" width="740" height="400">
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/5bd5dfa9-97b2-473d-afb2-bb4fdcd010f5/image.png" width="740" height="400">
     <br>
     <text>⇒ Kakao STT를 이용한 음성이 기록되고, 기록된 결과 텍스트 파일로 다운로드 가능</text>
   </div>
 </details>
 
 <details>
  <summary><strong>5) 게시판</strong></summary>
   <div markdown="1">
   <br>
     <h3>글 목록</h3> 
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/c5c574b5-11c8-450a-8c45-1725dc7c48d7/image.PNG" width="740" height="400">
    <br>
     <text>⇒ Paginator로 9개의 글을 한 페이지에서 확인 가능</text>
     <h3>글 쓰기</h3>
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/3ee276a1-c013-4518-ad09-7a71acec007c/image.PNG" width="740" height="400">
    <br>
     <text>⇒ Summernote Editor 사용</text>
     <h3>게시글</h3> 
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/6346d9c9-9550-4ba5-bbbc-e0f87ab3371a/image.PNG" width="740" height="400">
     <h3>글 검색</h3> 
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/93f568ac-51c7-42bb-ab66-9f3a4fe30088/image.PNG" width="740" height="400">
    <br>
     <text>⇒ 게시글 내 작성자, 글 내용, 글 제목을 기준으로 검색어와 관련된 게시글 출력</text>
   </div>
 </details>
 
 <details>
  <summary><strong>6) 마이페이지</strong></summary>
   <div markdown="1">    
     <br>
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/9d611d45-f91c-4645-a0aa-c74b1a84e854/image.PNG" width="740" height="400">
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/bf78ce58-6003-4a0a-85c7-ff865a412296/image.PNG" width="740" height="400">
     <br>
     <text>⇒ 사용자가 게시판에서 작성한 글, 댓글 단 글을 확인 가능</text>
     <h3>✏ 닉네임 수정</h3>
     <img src="https://velog.velcdn.com/images/jiyeah3108/post/75518efc-c223-4f87-ac6d-6891ebd2a773/image.PNG" width="740" height="400">
     <br>
   </div>
 </details>
<br>


<br>

## 5. 개발 환경

- `Front-End`

  |HTML|CSS|JS|Bootstrap|
  |:---:|:---:|:---:|:---:|
  |![html](https://user-images.githubusercontent.com/68097036/151471705-99458ff8-186c-435b-ac5c-f348fd836e40.png)|![css](https://user-images.githubusercontent.com/68097036/151471805-14e89a94-59e8-468f-8192-c10746b93896.png)|![js](https://user-images.githubusercontent.com/68097036/151471854-e0134a79-b7ef-4a0f-99fd-53e8ee5baf50.png)|![bootstrap](https://user-images.githubusercontent.com/68097036/151480381-2b23a8af-c6b4-43a6-96a6-ea69e0b953e0.png)|


- `Back-End`

  |Python|Django|MySQL|HeidiSQL|
  |:---:|:---:|:---:|:---:|
  |![pngwing com](https://user-images.githubusercontent.com/68097036/151479684-a85d26d4-e79e-47c9-9023-bf6d92f57536.png)|![pngwing com (1)](https://user-images.githubusercontent.com/68097036/151466729-9cad0405-85ad-454e-815a-1a4fd065f8b7.png)|![pngwing com (2)](https://user-images.githubusercontent.com/68097036/151466853-2b56fd0f-3aa9-424e-b17b-1c7cd991ffbf.png)|<img src="https://user-images.githubusercontent.com/68097036/151467351-5a359330-8d81-47b9-a33f-f7a5e0d69319.png" width="120" height="120">|

- `API`
  |Selenium|Google Translate|Kakao STT|Summernote|
  |:---:|:---:|:---:|:---:|
  |<img src="https://velog.velcdn.com/images/jiyeah3108/post/0483b261-99c6-4916-b7da-d19b8146d856/image.png" width="100" height="100">|<img src="https://velog.velcdn.com/images/jiyeah3108/post/042ab470-1c8d-4e98-922d-6853c0fdc063/image.png" width="100" height="100">|<img src="https://velog.velcdn.com/images/jiyeah3108/post/5756edcc-d4ef-43f3-8129-1ae40b9465da/image.png" width="180" height="60">|![brand_summernote_icon_157332](https://user-images.githubusercontent.com/68097036/151470431-2b196263-3c3f-425d-8fd0-0d6cf440e3d1.png)|


- `Etc`

  |VS Code|Microsoft Teams|GitHub|Notion|
  |:---:|:---:|:---:|:---:|
  |<img src="https://user-images.githubusercontent.com/68097036/151479933-01785e34-1283-4fca-a407-9fe284b50fa8.png" width="220" height="100">|![pngwing com (4)](https://user-images.githubusercontent.com/68097036/151467837-2cd89acd-2a92-45dd-b06b-e08e316b7695.png)|<img src="https://user-images.githubusercontent.com/68097036/151467910-0fda00cd-c08b-4869-a21e-a66d1d133ff5.png" width="230" height="100">|<img src="https://user-images.githubusercontent.com/68097036/151468186-82e630d3-8c3c-4c75-8243-e1efcba34926.png" width="220" height="110">|

<br>
