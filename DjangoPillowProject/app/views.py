"""
Definition of views.
"""

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
import numpy as np


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Harlen Hobbs',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
