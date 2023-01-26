from django.shortcuts import render, redirect

from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def search(request):
    searched = request.GET['q']
    if searched.upper() in (name.upper() for name in util.list_entries()):
        return redirect("page", page_name=searched)
    else:
        results = [i for i in util.list_entries() if searched.upper() in i.upper()]
        return render(request, "encyclopedia/search.html", {
            "results": results
        })


def page(request, page_name):
    return render(request, "encyclopedia/page.html", {
        "page_name": page_name,
        "page_content": util.get_entry(page_name)
    })


def random(request):
    rand = choice(util.list_entries())
    return redirect("page", page_name=rand)
