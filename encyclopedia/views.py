from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .forms import NewTaskForm
from django.contrib import messages
from . import util
from markdown2 import Markdown
import random

def index(request):

    return render(request, "encyclopedia/index.html", {
    "entries": util.list_entries()
    })

@csrf_exempt
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
        if page is not None:
            #markdown magic for the win
            markdowner = Markdown()
            content = markdowner.convert(page)
            return render(request, "encyclopedia/entry_page.html", {"content": content, "TITLE":TITLE})
        else:
            return render(request, "encyclopedia/error_page.html", {"errormsg" : f'Could not find page {TITLE}'})#fix so that when entering it


def edit_page(request,page):
    return render(request, "encyclopedia/entry_page.html", {"form" : NewTaskForm(initial={'entryTitle':page, 'entryContent': util.get_entry(page)}), "TITLE": page})

@csrf_exempt
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
                return render(request, "encyclopedia/create_page.html", {"errormsg" : f"Page {entry_title} already exists", "form": NewTaskForm()})
            else:
                util.save_entry(entry_title,entry_content)
                return redirect('index')
    else:
        return render(request, "encyclopedia/create_page.html", {"form": NewTaskForm()})
    return -1

def entry(request):
    re = request.GET["q"]
    return redirect(reverse('entry_page', kwargs = {"TITLE":re}))#huge credit to an ideas from https://www.youtube.com/watch?v=obRENgwHS7A
def random_page(request):
    entries = util.list_entries()
    entries = entries[random.randint(0,len(entries)-1)]
    return redirect(reverse('entry_page', kwargs = {"TITLE":entries}))#huge credit to an ideas from https://www.youtube.com/watch?v=obRENgwHS7A