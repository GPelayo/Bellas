from django.shortcuts import render, redirect
from .contexts import IndexContextBuilder, GridContextBuilder


def index(request):
    bldr = IndexContextBuilder()
    bldr.sync_wth_db()
    return render(request, 'index.html', bldr.context)


def grid(request, url_id):
    bldr = GridContextBuilder(url_id)
    bldr.sync_wth_db()
    return render(request, 'gallery.html', bldr.context)


def gallery_index_redirect(request):
    return redirect('/gallery/index')