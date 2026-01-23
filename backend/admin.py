from django.contrib import admin
from django.urls import path
from django.utils.html import format_html
from django.utils import timezone
from datetime import timedelta
from django.template.response import TemplateResponse
from .models import *
from django.contrib.admin import AdminSite

