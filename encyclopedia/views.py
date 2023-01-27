from django import forms
from django.shortcuts import render, redirect
from django.core.files import File

from random import choice

from . import util


class NewPageForm(forms.Form):
    title = forms.CharField(label="Page Title", max_length=24)
    content = forms.CharField(label="Page Content",  widget=forms.Textarea(attrs={'rows': 1, 'cols': 1}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page(request, page_name):
    return render(request, "encyclopedia/page.html", {
        "page_name": page_name,
        "page_content": util.convert_to_html(util.get_entry(page_name))
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


def new(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if title.upper() in (entry.upper() for entry in util.list_entries()):
                return render(request, 'encyclopedia/new.html', {
                    "form": form,
                    "error": 'article already exist'
                })
            else:
                with open(f'entries/{title}.md', 'w') as f:
                    file = File(f)
                    file.write(content)
                return redirect("page", page_name=title)

        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })

    return render(request, "encyclopedia/new.html", {
        "form": NewPageForm()
    })


def edit(request, name):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data['content']
            with open(f'entries/{name}.md', 'w') as f:
                file = File(f)
                file.write(new_content)
            return redirect("page", page_name=name)
    else:
        existing_content = util.get_entry(name)
        form = NewPageForm({
            'title': name,
            'content': existing_content,
        })
    return render(request, 'encyclopedia/edit.html', {
        'form': form,
        'title': name
    })


def random(request):
    rand = choice(util.list_entries())
    return redirect("page", page_name=rand)
