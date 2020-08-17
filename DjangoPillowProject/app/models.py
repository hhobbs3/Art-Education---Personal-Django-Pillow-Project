"""
Definition of models.
"""

from django.db import models
from django.shortcuts import render
from django.http import HttpRequest
from django.views.generic import TemplateView
from django.template import RequestContext
from datetime import datetime
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from json import *
import os
import os.path
from os import path
from pathlib import Path
from PIL import Image
from PIL import ImageFilter
import PIL
import numpy as np
import matplotlib.pyplot as plt
from skimage import data, filters
#from transforms import RGBTransform


def upload(request):
    print("%% HERE %%")
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document'] #document refers to upload.html name="document"
        fs = FileSystemStorage()

        print("%%Uploaded File%%: " + uploaded_file.name)

        urlSplit = uploaded_file.name.split('.')
        testUrl = urlSplit[0] + '_m4n1p__.' + urlSplit[1]
        print('test1: ' + testUrl)
        print('test2: ' + uploaded_file.name)
        name = fs.save(testUrl, uploaded_file)
        url = fs.url(name)
        print(url)
        context['url'] = url

    return render(request, 'app/upload.html', context)

def undo(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['document']
        print('URL: ' + url)

        #naming convention
        urlTest = url.replace('m4n1p_x', 'm4n1p_')
        print('t1: ' + url)
        print('t2: ' + urlTest)
        context['url'] = urlTest

    return render(request, 'app/upload.html', context)

def redo(request):
    context = {}
    if request.method == 'POST':

        url = request.POST['document']
        print('URL: ' + url)

        #naming convention
        urlTest = url.replace('m4n1p_', 'm4n1p_x')
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print('t1: ' + url + ' ' + str(path.exists(BASE_DIR + url)))
        print('t2: ' + urlTest + ' ' + str(path.exists(BASE_DIR + urlTest)))
        if path.exists(BASE_DIR + urlTest):
            context['url'] = urlTest
        else:
            context['url'] = url

    return render(request, 'app/upload.html', context)

def save(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['document']
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print('baseDir: ' + BASE_DIR)
        im = Image.open(BASE_DIR + url)

        #https://stackoverflow.com/questions/35851281/python-finding-the-users-downloads-folder

        if os.name == 'nt':
            import winreg
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]
            DOWNLOADS_DIR = location
        else:
            DOWNLOADS_DIR = os.path.join(os.path.expanduser('~'), 'downloads')
        
        urlTest = url.replace('/media', '')
        print('usrPath: ' + DOWNLOADS_DIR + urlTest)
        im.save(DOWNLOADS_DIR + urlTest) 

        context['url'] = url

    return render(request, 'app/upload.html', context)

def crispyWhite(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['document']

        #Crispy White Filter
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print('BASE_DIR: ' + BASE_DIR)

        #im = Image.open('..' + url)
        im = Image.open(BASE_DIR + url)
        im = im.convert('RGBA')
        data = np.array(im)   # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
        white_areas = (red >= 155) & (blue >= 155) & (green >= 155)
        data[..., :-1][white_areas.T] = (255, 255, 255) # Transpose back needed
        imX = Image.fromarray(data)
        
        #naming convention to help with undo
        urlTest = url.replace('m4n1p_', 'm4n1p_x')
        imX.save(BASE_DIR + urlTest) 
        context['url'] = urlTest

    return render(request, 'app/upload.html', context)

def composition(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['document']

        #Posterize Filter
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print('BASE_DIR: ' + BASE_DIR)

        #White
        im = Image.open(BASE_DIR + url)
        im = im.convert('RGBA')
        data = np.array(im)   # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
        white_areas = (red >= 155) & (blue >= 155) & (green >= 155)
        data[..., :-1][white_areas.T] = (255, 255, 255) # Transpose back needed
        im = Image.fromarray(data)
        urlTest = url.replace('m4n1p_', 'm4n1p_x')
        im.save(BASE_DIR + urlTest)

        #Black
        im = Image.open(BASE_DIR + urlTest)
        im = im.convert('RGBA')
        data = np.array(im)   # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
        black_areas = (red <= 90) & (blue <= 90) & (green <= 90)
        data[..., :-1][black_areas.T] = (0, 0, 0) # Transpose back needed
        im = Image.fromarray(data)
        im.save(BASE_DIR + urlTest)

        #Grey
        im = Image.open(BASE_DIR + urlTest)
        im = im.convert('RGBA')
        data = np.array(im)   # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
        grey_areas = (red != 0) & (red != 255) 
        data[..., :-1][grey_areas.T] = (128, 128, 128) # Transpose back needed
        im = Image.fromarray(data)
        im.save(BASE_DIR + urlTest)

        context['url'] = urlTest

    return render(request, 'app/upload.html', context)

def lightConcentration(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['document']

        #Posterize Filter
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print('BASE_DIR: ' + BASE_DIR)

        #red
        im = Image.open(BASE_DIR + url)
        im = im.convert('RGBA')
        data = np.array(im)   # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
        red_areas = (red > blue) & (red > green) 
        data[..., :-1][red_areas.T] = (255, 0, 0) # Transpose back needed
        im = Image.fromarray(data)
        urlTest = url.replace('m4n1p_', 'm4n1p_x')
        im.save(BASE_DIR + urlTest)

         #green
        im = Image.open(BASE_DIR + urlTest)
        im = im.convert('RGBA')
        data = np.array(im)   # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
        green_areas = (green > blue) & (green > red) 
        data[..., :-1][green_areas.T] = (0, 255, 0) # Transpose back needed
        im = Image.fromarray(data)
        im.save(BASE_DIR + urlTest)

        #blue
        im = Image.open(BASE_DIR + urlTest)
        im = im.convert('RGBA')
        data = np.array(im)   # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
        blue_areas = (blue > red) & (blue > green)
        data[..., :-1][blue_areas.T] = (0, 0, 255) # Transpose back needed
        im = Image.fromarray(data)
        im.save(BASE_DIR + urlTest)

        context['url'] = urlTest

    return render(request, 'app/upload.html', context)

def contour(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['document']
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print('BASE_DIR: ' + BASE_DIR)
        im = Image.open(BASE_DIR + url)
        im = im.convert('RGB')
        im = im.filter(ImageFilter.CONTOUR)   
        urlTest = url.replace('m4n1p_', 'm4n1p_x')
        im.save(BASE_DIR + urlTest)
        context['url'] = urlTest

    return render(request, 'app/upload.html', context)

def detail(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['document']
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print('BASE_DIR: ' + BASE_DIR)
        im = Image.open(BASE_DIR + url)
        im = im.convert('RGB')
        im = im.filter(ImageFilter.DETAIL)   
        urlTest = url.replace('m4n1p_', 'm4n1p_x')
        im.save(BASE_DIR + urlTest)
        context['url'] = urlTest

    return render(request, 'app/upload.html', context)

def edgeEnhanceMore(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['document']
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print('BASE_DIR: ' + BASE_DIR)
        im = Image.open(BASE_DIR + url)
        im = im.convert('RGB')
        im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)   
        urlTest = url.replace('m4n1p_', 'm4n1p_x')
        im.save(BASE_DIR + urlTest)
        context['url'] = urlTest

    return render(request, 'app/upload.html', context)

def emboss(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['document']
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print('BASE_DIR: ' + BASE_DIR)
        im = Image.open(BASE_DIR + url)
        im = im.convert('RGB')
        im = im.filter(ImageFilter.EMBOSS)   
        urlTest = url.replace('m4n1p_', 'm4n1p_x')
        im.save(BASE_DIR + urlTest)
        context['url'] = urlTest

    return render(request, 'app/upload.html', context)

def findEdges(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['document']
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print('BASE_DIR: ' + BASE_DIR)
        im = Image.open(BASE_DIR + url)
        im = im.convert('RGB')
        im = im.filter(ImageFilter.FIND_EDGES)   
        urlTest = url.replace('m4n1p_', 'm4n1p_x')
        im.save(BASE_DIR + urlTest)
        context['url'] = urlTest

    return render(request, 'app/upload.html', context)

def smoothMore(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['document']
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print('BASE_DIR: ' + BASE_DIR)
        im = Image.open(BASE_DIR + url)
        im = im.convert('RGB')
        im = im.filter(ImageFilter.SMOOTH_MORE)   
        urlTest = url.replace('m4n1p_', 'm4n1p_x')
        im.save(BASE_DIR + urlTest)
        context['url'] = urlTest

    return render(request, 'app/upload.html', context)

def detectRed(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['document']

        #Posterize Filter
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print('BASE_DIR: ' + BASE_DIR)

        #red000
        im = Image.open(BASE_DIR + url)
        im = im.convert('RGBA')
        data = np.array(im)   # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
        red_area = (red <= 0)
        data[..., :-1][red_area.T] = (0, 0, 0) # Transpose back needed
        im = Image.fromarray(data)
        urlTest = url.replace('m4n1p_', 'm4n1p_x')
        im.save(BASE_DIR + urlTest)

        colorH = 15
        colorL = 0
        for x in range(16):
            im = Image.open(BASE_DIR + urlTest)
            im = im.convert('RGBA')
            data = np.array(im)   # "data" is a height x width x 4 numpy array
            red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
            red_area = (red > colorL) & (red <= colorH)
            data[..., :-1][red_area.T] = (colorH, 0, 0) # Transpose back needed
            im = Image.fromarray(data)
            im.save(BASE_DIR + urlTest)
            colorH += 15
            colorL += 15

        context['url'] = urlTest

    return render(request, 'app/upload.html', context)

def detectGreen(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['document']

        #Posterize Filter
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print('BASE_DIR: ' + BASE_DIR)

        #red000
        im = Image.open(BASE_DIR + url)
        im = im.convert('RGBA')
        data = np.array(im)   # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
        green_area = (green <= 0)
        data[..., :-1][green_area.T] = (0, 0, 0) # Transpose back needed
        im = Image.fromarray(data)
        urlTest = url.replace('m4n1p_', 'm4n1p_x')
        im.save(BASE_DIR + urlTest)

        colorH = 15
        colorL = 0
        for x in range(16):
            im = Image.open(BASE_DIR + urlTest)
            im = im.convert('RGBA')
            data = np.array(im)   # "data" is a height x width x 4 numpy array
            red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
            green_area = (green > colorL) & (green <= colorH)
            data[..., :-1][green_area.T] = (0, colorH, 0) # Transpose back needed
            im = Image.fromarray(data)
            im.save(BASE_DIR + urlTest)
            colorH += 15
            colorL += 15

        context['url'] = urlTest

    return render(request, 'app/upload.html', context)

def detectBlue(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['document']

        #Posterize Filter
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print('BASE_DIR: ' + BASE_DIR)

        #red000
        im = Image.open(BASE_DIR + url)
        im = im.convert('RGBA')
        data = np.array(im)   # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
        blue_area = (blue <= 0)
        data[..., :-1][blue_area.T] = (0, 0, 0) # Transpose back needed
        im = Image.fromarray(data)
        urlTest = url.replace('m4n1p_', 'm4n1p_x')
        im.save(BASE_DIR + urlTest)

        colorH = 15
        colorL = 0
        for x in range(16):
            im = Image.open(BASE_DIR + urlTest)
            im = im.convert('RGBA')
            data = np.array(im)   # "data" is a height x width x 4 numpy array
            red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
            blue_area = (blue > colorL) & (blue <= colorH)
            data[..., :-1][blue_area.T] = (0, 0, colorH) # Transpose back needed
            im = Image.fromarray(data)
            im.save(BASE_DIR + urlTest)
            colorH += 15
            colorL += 15

        context['url'] = urlTest

    return render(request, 'app/upload.html', context)



def sharpen(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['document']

        #find image
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        im = Image.open(BASE_DIR + url)

        # Edit photo here https://www.blog.pythonlibrary.org/2016/10/07/an-intro-to-the-python-imaging-library-pillow/
        im = im.filter(ImageFilter.SHARPEN)

        #save with naming convention to help with undo
        urlTest = url.replace('m4n1p_', 'm4n1p_x')
        im.save(BASE_DIR + urlTest) #need to figure out how to save still...
        context['url'] = urlTest

        return render(request, 'app/upload.html', context)

def blackAndWhite(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['document']
        print('URL: ' + url)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print('BASE_DIR: ' + BASE_DIR)

        #im = Image.open('..' + url)
        im = Image.open(BASE_DIR + url)

        im = im.convert('1') # convert image to black and white
        
        #naming convention to help with undo
        urlTest = url.replace('m4n1p_', 'm4n1p_x')
        print('t1: ' + url)
        print('t2: ' + urlTest)
        im.save(BASE_DIR + urlTest) #need to figure out how to save still...
        context['url'] = urlTest

    return render(request, 'app/upload.html', context)

def blur(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['document']
        print('URL: ' + url)

        #Crispy White Filter
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print('BASE_DIR: ' + BASE_DIR)
        im = Image.open(BASE_DIR + url)

        # Blur
        im = im.filter(ImageFilter.BLUR)
        im = im.filter(ImageFilter.BLUR)
        im = im.filter(ImageFilter.BLUR)
        im = im.filter(ImageFilter.BLUR)
        im = im.filter(ImageFilter.BLUR)
        im = im.filter(ImageFilter.BLUR)

        #naming convention to help with undo
        urlTest = url.replace('m4n1p_', 'm4n1p_x')
        print('t1: ' + url)
        print('t2: ' + urlTest)
        im.save(BASE_DIR + urlTest) #need to figure out how to save still...
        context['url'] = urlTest

    return render(request, 'app/upload.html', context)

def test1(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['document']

        #find image
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        im = Image.open(BASE_DIR + url)

        # Edit photo here
        np_im = np.array(im) #convert to numpy array
        #np_im = np.asarray(PIL.Image.open(im))
        edges = filters.sobel(new_im)
        plt.imshow(edges, cmap='gray')
        #np_im = np.array(im) #convert to numpy array
        #print('np_im: ' + np_im)
        #np_im = filters.sobel(np_im) #filter numpy array
        #im = Image.fromarray(np_im) #convert back to image


        #save with naming convention to help with undo
        urlTest = url.replace('m4n1p_', 'm4n1p_x')
        im.save(BASE_DIR + urlTest)
        context['url'] = urlTest

    return render(request, 'app/upload.html', context)

def filterTemplate(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['document']


        #find image
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        im = Image.open(BASE_DIR + url)

        # Edit photo here

        #save with naming convention to help with undo
        urlTest = url.replace('m4n1p_', 'm4n1p_x')
        im.save(BASE_DIR + urlTest) #need to figure out how to save still...
        context['url'] = urlTest

    return render(request, 'app/upload.html', context)
