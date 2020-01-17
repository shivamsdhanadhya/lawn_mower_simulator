# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
#from .models import SimulatorDriver
from .models import SimulatorDriver
from django.http import JsonResponse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
import json
from django.core.files.storage import FileSystemStorage

import os
from django.conf import settings

simd = None

# Create your views here.
# This is def to resturn back HTML
def simulation(request):
        
        return render(request, 'simulations/simulation.html')

def ensure_initialized():

        global simd
        if simd == None:
                print "initializing"
                simd = SimulatorDriver(os.path.join(settings.BASE_DIR, "simulations", "src", "test.csv"))

def restart(request):

        global simd
        simd = None
        return JsonResponse(1, safe=False)

def getInfo(request):
        ensure_initialized()

        global simd
        return JsonResponse(simd.get_data(), safe=False)

def nextMove(request):
        ensure_initialized()

        global simd
        simd.next_move()
        return JsonResponse(simd.get_data(), safe=False)

def fastForward(request):
        ensure_initialized()

        global simd
        simd.fast_forward()
        return JsonResponse(simd.get_data(), safe=False)

def stop(request):
        ensure_initialized()
        
        global simd
        simd.stop()
        return JsonResponse(1, safe=False)

def redirectToSimulation(request):
        return HttpResponsePermanentRedirect("/simulation/")

def uploadFile(request):

        # stop simulation if it's initialized (safe to call if already stopped)
        global simd
        if simd != None:
                simd.stop()

        dir_path = os.path.join(settings.BASE_DIR, "simulations", "src") + "/"
        fs = FileSystemStorage(location=dir_path)
        file_name = "test.csv"

        # overwrite existing file
        full_file_name = os.path.join(dir_path, file_name)
        if os.path.isfile(full_file_name):
                os.remove(full_file_name)

        fs.save(file_name, request.FILES['file'])

        # reset state
        global simd
        simd = None

        global simd
        ensure_initialized()
        return HttpResponseRedirect("/simulation/")

