from django.shortcuts import render
from django.http import HttpResponse
from collections import OrderedDict
import json

def coupon(request):
    if 'code' in request.GET:
        code = request.GET['code']
        if code == '0001':
            benefit = '1'
            deadline = '1'
            message = '001'
        elif code == '0002':
            benefit = '2'
            deadline = '2'
            message = '002'
        else:
            benefit = 'NA'
            deadline = 'NA'
            message = 'not found'
        params = {
            'code':code,
            'coupon_benefits':benefit,
            'coupon_deadline':deadline,
            'message':message,
        }
        #json形式の文字列を生成
        json_str = json.dumps(params, ensure_ascii=False, indent=2) 
        return HttpResponse(json_str)