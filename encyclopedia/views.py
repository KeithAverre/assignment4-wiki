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

def entry_page(request, title):
    page = util.get_entry(title)
    if page is not None:
        #markdown magic for the win
        markdowner = Markdown()
        content = markdowner.convert(page)
        return render(request, "encyclopedia/entry_page.html", {"content": content, "title":title})
    else:
        redirect("index")


def edit_page(request, title):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["entryTitle"]
            entry_content = form.cleaned_data["entryContent"]
            page = util.get_entry(entry_title)
            if page is not None:
                util.save_entry(entry_title, entry_content)
                return redirect("entry_page", title=entry_title)
            else:
                util.replace_entry(title, entry_title, entry_content)
                context = {"title": title, "content": entry_content}
                return redirect("entry_page", title=entry_title)
    return render(request, "encyclopedia/edit_page.html", 
    {"form" : NewTaskForm(initial={'entryTitle':title, 'entryContent': util.get_entry(title)}), "title": title})

def create_page(request):
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
        return render(request, "encyclopedia/create_page.html", {"form": NewTaskForm(initial={})})

def search(request):
    re = request.GET.get("q", "")
    if len(re) == 0:
        return redirect("index")
    if util.get_entry(re) != None:
        return redirect("entry_page", title=re)
    all_entries = util.list_entries()
    partial_matches = [
        entry for entry in all_entries if entry.casefold().find(re.casefold()) != -1]
    context={
        "errormsg": f'Could not find the entry {re}',
        "found":partial_matches,
        "title":re,
    }
    return render(request, "encyclopedia/search_results.html", context)

def random_page(request):
    entries = util.list_entries()
    random_entry = entries[random.randint(0,len(entries)-1)]
    # bad practice to change the type of the variable! you are changing entries from a list to a string
    #return redirect(reverse('entry_page', kwargs = {"TITLE":entries}))#huge credit to an ideas from https://www.youtube.com/watch?v=obRENgwHS7A
    return redirect('entry_page', title=random_entry)