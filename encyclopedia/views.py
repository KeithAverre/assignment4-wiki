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

                util.replace_entry(TITLE, entry_title, entry_content)
                context = {"title": TITLE, "content": entry_content}
                return render(request, "encyclopedia/entry_page.html", context)
    else:
        page = util.get_entry(TITLE)
        print(TITLE)
        if page is not None:
            #markdown magic for the win
            markdowner = Markdown()
            content = markdowner.convert(page)
            return render(request, "encyclopedia/entry_page.html", {"content": content})
        else:
            return render(request, "encyclopedia/error_page.html", {"errormsg" : f'Could not find page {TITLE}'})#fix so that when entering it
def edit_page(request,page):
    return render(request, "encyclopedia/entry_page.html", {"form" : NewTaskForm(request), "TITLE": page})
def edit_page(request):
    title = request.GET["page"]
    return render(request, "encyclopedia/entry_page.html", {"form" : NewTaskForm(request), "TITLE" : title})
def create_page(request):

    #add a new newtaskform
    #
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["entryTitle"]
            entry_content = form.cleaned_data["entryContent"]
            page = util.get_entry(entry_title)
            if page is not None:
                return render(request, "encyclopedia/error_page.html", {"errormsg" : f"Page {entry_title} was not found"})
            else:
                util.save_entry(entry_title,entry_content)
                return redirect(entry_title)
    else:
        return render(request, "encyclopedia/create_page.html", {"form": NewTaskForm()})
    return -1