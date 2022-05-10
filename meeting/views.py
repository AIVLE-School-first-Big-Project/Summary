from django.shortcuts import render
import requests
import json
import speech_recognition as sr
import os
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
import urllib

global encode_title

def meetingstart(request):
    return render(request,'meetingstart.html')

def audio(request):
    global encode_title

    url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
    rest_api_key = '8a6c86f867f58229747408ae4accab0b'
    header = {"Content-Type": "application/octet-stream", 
            "Content-Length": "chunked",
            "Authorization": "KakaoAK " + rest_api_key,
              }
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=16000) as source:
        print("기록을 시작하겠습니다!")
        audio = r.listen(source)
    res = requests.post(url, headers=header, data=audio.get_raw_data())
    result_json_string = res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1]
    result = json.loads(result_json_string)
    print(result)
    voice = result['value']

    title = 'meeting'
    encode_title = urllib.parse.quote(string=f'{title}.txt')

    file = open(f'media/{encode_title}', 'w', encoding="UTF-8")
    file.write(voice)                # 파일에 문자열 저장
    file.close()

    return render(request,'voice.html', {'voice' : voice})


def downloadFile(request):
    global encode_title

    file_path = os.path.abspath('media/')
    file_name = encode_title
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_name, 'rb'),
                            content_type='text/plain')
    response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s'% file_name

    return response
