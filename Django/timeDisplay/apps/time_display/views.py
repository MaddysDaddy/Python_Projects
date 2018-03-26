# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
import time
import datetime

# Create your views here.


def index(request):
    now = datetime.datetime.now()
    print now
    context = {
        'time': time.strftime("%I:%M %p", time.localtime()),
        'date': time.strftime("%B %d, %Y", time.localtime())
    }
    return render(request, 'time_display/index.html', context)
