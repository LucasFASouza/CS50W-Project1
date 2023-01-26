from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, page_name):
    return render(request, "encyclopedia/page.html", {
        "page_name": page_name,
        "page_content": util.get_entry(page_name)
    })