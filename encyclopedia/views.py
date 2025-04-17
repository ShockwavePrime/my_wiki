import difflib
import random

from django import forms
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from . import util
from .markdown_extras import convert_markdown_to_html


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def view_entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return Http404("Entry not found")

    html_content = convert_markdown_to_html(content)
    return render(
        request, "encyclopedia/entries.html", {"title": title, "content": html_content}
    )


def search_view(request):
    query = request.GET.get("q", "").strip().lower()
    entries = util.list_entries()

    # Exact match (case-insensitive)
    for entry in entries:
        if entry.lower() == query:
            return redirect("entry", title=entry)

    # Fuzzy matches (case-insensitive)
    entry_map = {entry.lower(): entry for entry in entries}
    matches = difflib.get_close_matches(query, entry_map.keys(), n=5, cutoff=0.5)
    match_titles = [entry_map[match] for match in matches]

    return render(
        request, "encyclopedia/search.html", {"query": query, "matches": match_titles}
    )


class EditForm(forms.Form):
    title = forms.CharField(
        label="Page Title", widget=forms.TextInput(attrs={"name": "title"})
    )
    body = forms.CharField(
        label="Page Content",
        widget=forms.Textarea(attrs={"name": "body", "rows": 8, "cols": 30}),
    )


def new(request):
    return render(
        request,
        "encyclopedia/new.html",
        {"title": "Create New Page", "edit": False, "editpage": EditForm()},
    )


def save(request):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]

            # checking if entry already exists
            if util.get_entry(title):
                return render(
                    request,
                    "encyclopedia/new.html",
                    {
                        "title": "Create New Page",
                        "edit": False,
                        "editpage": form,
                        "error": f"An entry with the title '{title}' already exists.",
                    },
                )

            util.save_entry(title, body)
            return HttpResponseRedirect(reverse("entry", args=[title]))
    else:
        return HttpResponseRedirect(reverse("new"))


def random_entry(request):
    entries = util.list_entries()
    if entries:
        random_title = random.choice(entries)
        return redirect("entry", title=random_title)
    else:
        return render(request, "no_entries.html")


def edit_entry(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["body"]
            util.save_entry(title, content)
            messages.success(request, f"'{title}' has been updated successfully!")
            return redirect("entry", title=title)
    else:
        content = util.get_entry(title)
        if content is None:
            return render(
                request,
                "encyclopedia/error.html",
                {"message": f"The page '{title}' does not exist."},
            )
        form = EditForm(initial={"title": title, "body": content})
        return render(request, "encyclopedia/edit.html", {"form": form, "title": title})
