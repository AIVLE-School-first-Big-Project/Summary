from contextlib import redirect_stdout
import re
from urllib import request
from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse, JsonResponse
import requests
import json
import speech_recognition as sr
from .models import Meeting


def meetingstart(request):
    
    return render(request,'meetingstart.html')

def audio(request):
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
    # meetings = Meeting.objects

    return HttpResponse(str(result['value']))   


# def meetingstart(request):
#     return render(request , 'meeting/meetingstart.html')

