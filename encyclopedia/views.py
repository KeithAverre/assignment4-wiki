from django.shortcuts import render

from . import util
from markdown2 import Markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry_page(request, TITLE):
    page = util.get_entry(TITLE)
    if page is not None:
        #markdown magic for the win
        markdowner = Markdown()
        content = markdowner.convert(page)
        return render(request, "encyclopedia/entry_page.html", {"content": content})
    else:
        return render(request, "encyclopedia/index.html")

def create_page(request):
    return -1