from django.shortcuts import render, get_object_or_404
from .forms import MarkdownForm
from .models import HtmlModel
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown


def markdown_form_view(request):
    if str(request.method).upper() == "POST":
        form = MarkdownForm(request.POST)
        context = { "form": form }
    
        if form.is_valid():
            form.save()
            
            

            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            page = f"# {title}\n{body}"

            html = markdown.markdown(page)

            if request.user.is_authenticated:
                html_object = HtmlModel.objects.create(user=request.user, title=title, page=html)
                html_object.save()
                html_object.refresh_from_db()

                return HttpResponseRedirect(reverse("html_generator:page", args=[html_object.id]))


    else:
        form = MarkdownForm()
        context = { "form": form }
        return render(request, "index.html", context)

def page_view(request, page_id):
    html_object = get_object_or_404(HtmlModel,pk=page_id)
    context = { "html_page": html_object.page }
    return render(request, "page.html", context)