from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import NewTaskForm
from django.contrib import messages
from . import util
from markdown2 import Markdown

def index(request):

    return render(request, "encyclopedia/index.html", {
    "entries": util.list_entries()
    })
def entry_page(request, TITLE):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["entryTitle"]
            entry_content = form.cleaned_data["entryContent"]
            page = util.get_entry(entry_title)
            if page is not None:
                util.save_entry(entry_title, entry_content)
                context = {"title": TITLE}
                return render(request, "encyclopedia/entry_page.html", context)
            else:
                context = {"title": TITLE,
                           "errormsg": "Page to edit not found"}
                return render(request, "encyclopedia/error_page.html", context)
            return render(request, "encyclopedia/entry_page.html", context)

    page = util.get_entry(TITLE)
    print(TITLE)
    if page is not None:
        #markdown magic for the win
        markdowner = Markdown()
        content = markdowner.convert(page)
        return render(request, "encyclopedia/entry_page.html", {"content": content})
    else:
        return render(request, "encyclopedia/index.html")#fix so that when entering it
def edit_page(request):
    return render(request, "encyclopedia/index.html")
def create_page(request):
    return -1