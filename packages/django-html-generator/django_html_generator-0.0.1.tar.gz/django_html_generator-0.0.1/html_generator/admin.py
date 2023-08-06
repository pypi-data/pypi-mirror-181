from django.contrib import admin
from .models import MarkdownModel, HtmlModel

admin.site.register(MarkdownModel)
admin.site.register(HtmlModel)
