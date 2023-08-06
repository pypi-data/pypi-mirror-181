from django import forms
from . import models

class MarkdownForm(forms.ModelForm):

    class Meta:
        model = models.MarkdownModel
        fields = "__all__"
        widgets = {
            "body": forms.Textarea(attrs={"cols": 80, "rows": 30}),
        }
        