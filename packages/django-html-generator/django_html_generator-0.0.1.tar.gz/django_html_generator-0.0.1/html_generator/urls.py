from django.urls import path
from . import views

app_name = "html_generator"
urlpatterns = [
    path("", views.markdown_form_view, name="html_gen"),
    path("<int:page_id>/", views.page_view, name="page"),
]